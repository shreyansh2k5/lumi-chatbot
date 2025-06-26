import os
import discord
import replicate
from dotenv import load_dotenv
import config

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Current personality in memory
current_personality = config.DEFAULT_PERSONALITY

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_message(message):
    global current_personality

    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        content = message.clean_content.replace(f"@{client.user.display_name}", "").strip()

        # Personality switcher
        if content.lower().startswith("personality:"):
            new_personality = content.split(":", 1)[1].strip().lower()
            if config.is_valid_personality(new_personality):
                current_personality = new_personality
                await message.reply(f"🔄 Personality set to **{new_personality}**.")
            else:
                valid = ", ".join(config.PERSONALITIES.keys())
                await message.reply(f"❌ Invalid personality. Choose from: {valid}")
            return

        # Normal AI response
        if content:
            await message.channel.typing()
            prompt = config.build_prompt(content, current_personality)

            try:
                response = replicate_client.run(
                    config.REPLICATE_MODEL,
                    input={
                        "prompt": prompt,
                        **config.get_model_params(current_personality)
                    }
                )
                answer = "".join(response).strip()
                await message.reply(f"🧠 {answer}")
            except Exception as e:
                await message.reply(f"⚠️ Error: {str(e)}")
        else:
            await message.reply("🧠 Please say something after mentioning me.")

client.run(DISCORD_TOKEN)

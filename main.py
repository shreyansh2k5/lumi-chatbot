import os
import discord
import replicate
from dotenv import load_dotenv
import config  # ← import personality/config

# Load .env vars
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Initialize Replicate
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# Discord client setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        await message.channel.typing()

        user_input = message.clean_content.replace(f"@{client.user.display_name}", "").strip()
        if not user_input:
            await message.reply("🧠 Please ask something after mentioning me.")
            return

        prompt = config.build_prompt(user_input)

        try:
            output = replicate_client.run(
                config.REPLICATE_MODEL,
                input={
                    "prompt": prompt,
                    "temperature": config.TEMPERATURE,
                }
            )
            answer = "".join(output).strip()
            await message.reply(f"🧠 {answer}")
        except Exception as e:
            await message.reply(f"⚠️ Error: {str(e)}")

client.run(DISCORD_TOKEN)

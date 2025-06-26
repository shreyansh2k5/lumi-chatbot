import discord
import os
import replicate
from dotenv import load_dotenv
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 🧠 Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# ⚙️ Required for Render to stay alive
os.environ["RENDER"] = "true"

def keep_alive():
    server = HTTPServer(("0.0.0.0", 8080), SimpleHTTPRequestHandler)
    server.serve_forever()

Thread(target=keep_alive).start()

# 🛠️ Set Replicate API token
replicate.Client(api_token=REPLICATE_API_TOKEN)

# 🤖 Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# 💬 Chat function using Replicate
def ask_llama(prompt):
    try:
        output = replicate.run(
            "meta/meta-llama-3-8b-instruct",
            input={"prompt": prompt, "max_new_tokens": 200}
        )
        return "".join(output)
    except Exception as e:
        return f"⚠️ Error: {e}"

@bot.event
async def on_ready():
    print(f"🤖 Lumi is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
        reply = ask_llama(prompt)
        await message.channel.send(reply)

# 🚀 Start the bot
bot.run(DISCORD_TOKEN)

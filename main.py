import os
import discord
import requests
from dotenv import load_dotenv
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 🌐 Keep Render Web Service alive
os.environ["RENDER"] = "true"
def keep_alive():
    server = HTTPServer(("0.0.0.0", 8080), SimpleHTTPRequestHandler)
    server.serve_forever()
Thread(target=keep_alive).start()

# 🔐 Load environment
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# 🤖 Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

def query_replicate(prompt):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "your-model-version-id-here",  # We’ll help get this
        "input": {"prompt": prompt}
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["output"]
    else:
        return f"⚠️ Error: {response.text}"

@bot.event
async def on_ready():
    print(f"💖 Lumi is online as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.listening, name="your sweet secrets 💬")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
        reply = query_replicate(prompt)
        await message.channel.send(reply)

bot.run(DISCORD_TOKEN)

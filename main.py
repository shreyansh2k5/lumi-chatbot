import os
import discord
import requests
from dotenv import load_dotenv
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 🟢 Keep alive on Render
os.environ["RENDER"] = "true"
def keep_alive():
    server = HTTPServer(("0.0.0.0", 8080), SimpleHTTPRequestHandler)
    server.serve_forever()
Thread(target=keep_alive).start()

# 🟢 Load environment
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# 🟢 Discord setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# 🧠 Call Replicate
def ask_replicate(prompt):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "REPLACE_THIS_WITH_MODEL_VERSION_ID",
        "input": {
            "prompt": prompt
        }
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        output = response.json().get("output", "No response")
        return output if output else "⚠️ No output from Replicate"
    except Exception as e:
        return f"⚠️ Error: {e}"

@bot.event
async def on_ready():
    print(f"🤖 Lumi is online as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.watching, name="your heart 💖")
    await bot.change_presence(status=discord.Status.idle, activity=activity)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if not prompt:
            prompt = "Hey Lumi!"
        response = ask_replicate(prompt)
        await message.channel.send(response)

bot.run(DISCORD_TOKEN)

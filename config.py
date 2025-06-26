# config.py

# Bot tone/personality
BOT_NAME = "Test-Bot"
PERSONALITY_DESCRIPTION = (
    f"You are {BOT_NAME}, a thoughtful, calm, and highly intelligent AI. "
    "You always provide accurate, well-explained answers in a concise and friendly tone. "
    "Avoid being flirty, humorous, or overly casual. Focus on clarity and depth."
)

# Model configuration
REPLICATE_MODEL = "meta/meta-llama-3-8b-instruct"
TEMPERATURE = 0.4  # Lower is more precise, higher is more creative
MAX_TOKENS = 512   # Optional: limit length of response (not used by all models)

# Template for prompt generation
def build_prompt(user_input: str) -> str:
    return (
        f"{PERSONALITY_DESCRIPTION}\n\n"
        f"User: {user_input}\n"
        f"{BOT_NAME}:"
    )


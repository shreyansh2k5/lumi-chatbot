# config.py

BOT_NAME = "Test-Bot"

# Different personality presets
PERSONALITIES = {
    "intellectual": {
        "description": (
            f"You are {BOT_NAME}, a highly intelligent AI with deep knowledge. "
            "You provide accurate, detailed, and well-structured responses. "
            "You are formal and helpful, never flirty or humorous."
        ),
        "temperature": 0.4
    },
    "friendly": {
        "description": (
            f"You are {BOT_NAME}, a friendly and casual assistant. "
            "You explain things in simple, relatable language and sound kind and supportive."
        ),
        "temperature": 0.6
    },
    "sarcastic": {
        "description": (
            f"You are {BOT_NAME}, a sarcastic AI with a dry sense of humor. "
            "Your replies are witty, sometimes teasing, but still informative."
        ),
        "temperature": 0.8
    }
}

DEFAULT_PERSONALITY = "intellectual"
# Choose which personality to use by default
ACTIVE_PERSONALITY = "intellectual"

# Model info
REPLICATE_MODEL = "meta/meta-llama-3-8b-instruct"

# Prompt builder
def build_prompt(user_input: str, personality_key: str):
    persona = PERSONALITIES[ACTIVE_PERSONALITY]
    return (
        f"{persona['description']}\n\n"
        f"User: {user_input}\n"
        f"{BOT_NAME}:"
    )

# Model generation parameters
def get_model_params():
    return {
        "temperature": PERSONALITIES[ACTIVE_PERSONALITY]["temperature"]
    }

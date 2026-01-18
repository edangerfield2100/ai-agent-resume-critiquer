import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# List of current Anthropic models to test
models_to_test = [
    "claude-3-5-sonnet-20241022",  # Latest Claude 3.5 Sonnet
    "claude-3-5-sonnet-20240620",  # Previous Claude 3.5 Sonnet
    "claude-3-5-haiku-20241022",   # Latest Claude 3.5 Haiku
    "claude-3-opus-20240229",      # Claude 3 Opus
    "claude-3-sonnet-20240229",    # Claude 3 Sonnet
    "claude-3-haiku-20240307",     # Claude 3 Haiku
]

print("Testing model availability for your account...\n")

available_models = []
unavailable_models = []

for model in models_to_test:
    try:
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✅ {model} - AVAILABLE")
        available_models.append(model)
    except Exception as e:
        if "not_found_error" in str(e):
            print(f"❌ {model} - NOT AVAILABLE")
            unavailable_models.append(model)
        else:
            print(f"⚠️  {model} - ERROR: {str(e)}")

print(f"\n--- SUMMARY ---")
print(f"Available models ({len(available_models)}):")
for model in available_models:
    print(f"  • {model}")

print(f"\nUnavailable models ({len(unavailable_models)}):")
for model in unavailable_models:
    print(f"  • {model}")

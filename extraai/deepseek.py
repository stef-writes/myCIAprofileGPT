import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize the DeepSeek client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def generate_story():
    """Generate a simple story using the DeepSeek API."""
    try:
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "user",
                    "content": "Write a one-sentence bedtime story about a unicorn."
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    print("Generating a story using DeepSeek...")
    story = generate_story()
    print("\nYour story:")
    print(story)

if __name__ == "__main__":
    main() 
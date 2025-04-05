import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

def generate_story():
    """Generate a simple story using the OpenAI API."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
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
    print("Generating a story...")
    story = generate_story()
    print("\nYour story:")
    print(story)

if __name__ == "__main__":
    main() 
import os
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

# ===== STRUCTURED OUTPUTS =====

class Person(BaseModel):
    """A person with basic information."""
    name: str
    age: int
    occupation: str
    hobbies: List[str] = Field(default_factory=list)

class Event(BaseModel):
    """A calendar event with details."""
    title: str
    date: str
    location: Optional[str] = None
    participants: List[str] = Field(default_factory=list)
    description: Optional[str] = None

def extract_person_info(text: str) -> Person:
    """
    Extract person information from unstructured text using structured outputs.
    
    Args:
        text: Unstructured text containing information about a person
        
    Returns:
        Person object with extracted information
    """
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract person information from the text."},
                {"role": "user", "content": text},
            ],
            response_format=Person,
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error extracting person info: {str(e)}")
        return None

def extract_event_info(text: str) -> Event:
    """
    Extract event information from unstructured text using structured outputs.
    
    Args:
        text: Unstructured text containing information about an event
        
    Returns:
        Event object with extracted information
    """
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract event information from the text."},
                {"role": "user", "content": text},
            ],
            response_format=Event,
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error extracting event info: {str(e)}")
        return None

# ===== PROMPT GENERATION =====

def generate_prompt(task_description: str) -> str:
    """
    Generate an effective prompt based on a task description.
    
    Args:
        task_description: Description of the task to create a prompt for
        
    Returns:
        Generated prompt as a string
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    Given a task description, produce a detailed system prompt to guide a language model in completing the task effectively.
                    
                    Guidelines:
                    - Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
                    - Reasoning Before Conclusions: Encourage reasoning steps before any conclusions are reached.
                    - Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.
                    - Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions.
                    - Formatting: Use markdown features for readability.
                    - Output Format: Explicitly specify the most appropriate output format, in detail.
                    
                    The final prompt should start with a concise instruction describing the task.
                    """
                },
                {"role": "user", "content": task_description},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating prompt: {str(e)}")
        return None

def generate_function_schema(task_description: str) -> Dict[str, Any]:
    """
    Generate a function schema based on a task description.
    
    Args:
        task_description: Description of the task to create a function schema for
        
    Returns:
        Function schema as a dictionary
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    Given a task description, produce a function schema that can be used with OpenAI's function calling feature.
                    
                    The schema should include:
                    - name: A descriptive name for the function
                    - description: A clear description of what the function does
                    - parameters: A JSON schema object describing the parameters
                    
                    Return only the JSON schema, no additional text.
                    """
                },
                {"role": "user", "content": task_description},
            ],
        )
        # Parse the response as JSON
        import json
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error generating function schema: {str(e)}")
        return None

# ===== REASONING =====

def solve_with_reasoning(prompt: str, effort: str = "medium") -> str:
    """
    Solve a complex problem using a reasoning model.
    
    Args:
        prompt: The problem or question to solve
        effort: Reasoning effort level ("low", "medium", or "high")
        
    Returns:
        Solution to the problem
    """
    try:
        response = client.chat.completions.create(
            model="o3-mini",
            reasoning_effort=effort,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error solving with reasoning: {str(e)}")
        return None

def solve_coding_problem(problem_description: str) -> str:
    """
    Solve a coding problem using a reasoning model.
    
    Args:
        problem_description: Description of the coding problem
        
    Returns:
        Solution to the coding problem
    """
    return solve_with_reasoning(problem_description, "high")

# ===== EXAMPLE USAGE =====

def main():
    # Example 1: Structured Outputs
    print("=== Structured Outputs Example ===")
    person_text = "John is a 32-year-old software engineer who enjoys hiking, reading, and playing chess."
    person = extract_person_info(person_text)
    if person:
        print(f"Extracted person: {person.model_dump_json(indent=2)}")
    
    event_text = "Team meeting on Monday at 10am in the conference room. Alice, Bob, and Charlie will attend."
    event = extract_event_info(event_text)
    if event:
        print(f"Extracted event: {event.model_dump_json(indent=2)}")
    
    # Example 2: Prompt Generation
    print("\n=== Prompt Generation Example ===")
    task = "Create a prompt that helps a language model write engaging product descriptions for an e-commerce website."
    prompt = generate_prompt(task)
    if prompt:
        print(f"Generated prompt:\n{prompt}")
    
    # Example 3: Reasoning
    print("\n=== Reasoning Example ===")
    problem = """
    Write a Python function that takes a list of integers and returns the longest increasing subsequence.
    For example, given [10, 22, 9, 33, 21, 50, 41, 60], the function should return [10, 22, 33, 50, 60].
    """
    solution = solve_coding_problem(problem)
    if solution:
        print(f"Solution:\n{solution}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test script for prompt_utils.py
This script demonstrates how to use the functions in prompt_utils.py
"""

from src.utils.prompt_utils import (
    extract_person_info,
    extract_event_info,
    generate_prompt,
    generate_function_schema,
    solve_with_reasoning,
    solve_coding_problem
)

def test_structured_outputs():
    """Test the structured outputs functionality."""
    print("\n=== Testing Structured Outputs ===")
    
    # Test person extraction
    person_text = "Sarah is a 28-year-old graphic designer who loves photography, painting, and traveling."
    print(f"\nExtracting person info from: '{person_text}'")
    person = extract_person_info(person_text)
    if person:
        print(f"Extracted person: {person.model_dump_json(indent=2)}")
    
    # Test event extraction
    event_text = "Birthday party for Michael on Saturday at 7pm at Central Park. Emma, James, and Lisa are invited."
    print(f"\nExtracting event info from: '{event_text}'")
    event = extract_event_info(event_text)
    if event:
        print(f"Extracted event: {event.model_dump_json(indent=2)}")

def test_prompt_generation():
    """Test the prompt generation functionality."""
    print("\n=== Testing Prompt Generation ===")
    
    # Test prompt generation
    task = "Create a prompt that helps a language model write engaging blog post titles."
    print(f"\nGenerating prompt for task: '{task}'")
    prompt = generate_prompt(task)
    if prompt:
        print(f"Generated prompt:\n{prompt}")
    
    # Test function schema generation
    task = "Create a function that validates email addresses"
    print(f"\nGenerating function schema for task: '{task}'")
    schema = generate_function_schema(task)
    if schema:
        print(f"Generated schema: {schema}")

def test_reasoning():
    """Test the reasoning functionality."""
    print("\n=== Testing Reasoning ===")
    
    # Test solving a complex problem
    problem = "What are the best practices for securing a web application?"
    print(f"\nSolving problem: '{problem}'")
    solution = solve_with_reasoning(problem, effort="medium")
    if solution:
        print(f"Solution:\n{solution}")
    
    # Test solving a coding problem
    coding_problem = """
    Write a Python function that checks if a string is a palindrome.
    For example, "radar" is a palindrome, but "hello" is not.
    """
    print(f"\nSolving coding problem: '{coding_problem.strip()}'")
    solution = solve_coding_problem(coding_problem)
    if solution:
        print(f"Solution:\n{solution}")

def main():
    """Run all tests."""
    print("Testing prompt_utils.py functionality")
    
    # Test structured outputs
    test_structured_outputs()
    
    # Test prompt generation
    test_prompt_generation()
    
    # Test reasoning
    test_reasoning()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main() 
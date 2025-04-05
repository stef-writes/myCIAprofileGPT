#!/usr/bin/env python3
"""
Repository Organization Script

This script organizes the files in the repository into a proper structure for GitHub.
It creates the necessary directories and moves files to their appropriate locations.
"""

import os
import shutil
import subprocess

def create_directory(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def move_file(source, destination):
    """Move a file from source to destination."""
    if os.path.exists(source):
        # If source and destination are the same, skip
        if os.path.abspath(source) == os.path.abspath(destination):
            print(f"File {source} is already in the correct location")
            return
            
        # Create the destination directory if it doesn't exist
        dest_dir = os.path.dirname(destination)
        if dest_dir:  # Only create directory if there is a path component
            os.makedirs(dest_dir, exist_ok=True)
        
        # Copy the file to the destination
        shutil.copy2(source, destination)
        print(f"Moved {source} to {destination}")
    else:
        print(f"Warning: Source file {source} does not exist")

def main():
    """Organize the repository files."""
    # Create directory structure
    create_directory("src")
    create_directory("src/core")
    create_directory("src/utils")
    create_directory("src/templates")
    create_directory("src/examples")
    create_directory("src/reports")
    create_directory("tests")
    create_directory("docs")
    
    # Move core files
    move_file("ciaprofile.py", "src/core/ciaprofile.py")
    move_file("profile_templates.py", "src/templates/profile_templates.py")
    
    # Move utility files
    move_file("generate_profile_report.py", "src/utils/report_generator.py")
    
    # Move example files
    move_file("example_profile.py", "src/examples/example_profile.py")
    
    # Move test files
    move_file("test_ciaprofile.py", "tests/test_ciaprofile.py")
    move_file("test_prompt_utils.py", "tests/test_prompt_utils.py")
    
    # Move report files
    move_file("profile_report.md", "src/reports/profile_report.md")
    
    # Move configuration files
    move_file("requirements.txt", "requirements.txt")
    move_file(".gitignore", ".gitignore")
    
    # Create a new README.md in the root directory
    with open("README.md", "w") as f:
        f.write("""# CIA Profile Generator

A sophisticated psychological profiling system that analyzes text to produce detailed psychological profiles in a CIA intelligence report style.

## Features

- **Comprehensive Psychological Analysis**: Personality traits, emotional states, cognitive patterns
- **Neurolinguistic Analysis**: Syntactic complexity, pronoun ratios, temporal orientation
- **Dark Triad Assessment**: Narcissism, machiavellianism, and psychopathy analysis
- **Behavioral Predictions**: Scenario-based predictions with confidence levels
- **Quantitative Metrics**: Persuasion susceptibility, deception capacity, risk tolerance
- **Security Profile**: Operational security risks, detectable patterns, and countermeasures

## Repository Structure

- `src/core/`: Core functionality for psychological profiling
- `src/templates/`: Templates for different analysis tones
- `src/utils/`: Utility functions for report generation
- `src/examples/`: Example scripts demonstrating usage
- `src/reports/`: Generated profile reports
- `tests/`: Test files for the codebase
- `docs/`: Documentation

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/stef-writes/myCIAprofileGPT.git
   cd myCIAprofileGPT
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Basic Usage

```python
from src.core.ciaprofile import generate_structured_profile

# Generate a structured profile
profile = generate_structured_profile("Your text here", tone="balanced")
print(profile)
```

### Generating a Comprehensive Report

```python
from src.utils.report_generator import generate_profile_report

# Generate a comprehensive profile report
generate_profile_report("Your text here", output_filename="profile_report.md")
```

## License

MIT
""")
    
    print("\nRepository organization complete!")
    print("\nNext steps:")
    print("1. Initialize git repository (if not already done):")
    print("   git init")
    print("2. Add all files to git:")
    print("   git add .")
    print("3. Commit the changes:")
    print("   git commit -m 'Initial commit'")
    print("4. Add the remote repository:")
    print("   git remote add origin https://github.com/stef-writes/myCIAprofileGPT.git")
    print("5. Push to GitHub:")
    print("   git push -u origin main")

if __name__ == "__main__":
    main() 
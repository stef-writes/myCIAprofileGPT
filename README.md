# CIA Profile Generator

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

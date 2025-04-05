# CIA Profile Generator

A Python-based tool for generating psychological profiles and intelligence reports from text input.

## Overview

The CIA Profile Generator is a sophisticated text analysis tool that can:
- Generate psychological profiles from text
- Analyze text with reasoning
- Create detailed reports
- Generate intelligence reports
- Calculate behavioral metrics
- Create security profiles

## Project Structure

```
CIABot/
├── src/
│   └── core/
│       └── ciaprofile.py      # Core implementation
├── output/                    # Generated output files
├── analyze_author.py         # Example script for author analysis
├── author_sample.txt         # Sample text for analysis
├── setup.py                  # Package setup file
└── README.md                 # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CIABot.git
cd CIABot
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Basic Usage

```python
from src.core.ciaprofile import (
    generate_profile_prompt,
    analyze_text_with_reasoning,
    generate_structured_profile,
    generate_detailed_report,
    generate_intelligence_report,
    calculate_metrics,
    generate_security_profile
)

# Your text to analyze
text = "Your text here..."

# Generate a profile
profile = generate_structured_profile(text)

# Generate a detailed report
report = generate_detailed_report(profile)

# Calculate metrics
metrics = calculate_metrics(profile)
```

### Example Script

The repository includes an example script `analyze_author.py` that demonstrates how to use the CIA Profile Generator to analyze a text file. The script:

1. Reads text from a file
2. Generates various reports and profiles
3. Saves all outputs to the `output` directory with unique timestamps

To run the example:
```bash
python analyze_author.py
```

## Output Files

The generator creates several types of output files:
- `*_prompt.txt`: The generated profile prompt
- `*_reasoning.txt`: Text analysis with reasoning
- `*_profile.json`: Structured profile data
- `*_detailed_report.md`: Detailed analysis report
- `*_intelligence_report.md`: Intelligence report
- `*_metrics.json`: Calculated behavioral metrics
- `*_security_profile.json`: Security profile data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

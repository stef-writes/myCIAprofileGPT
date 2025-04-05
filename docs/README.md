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
- Assess communication styles
- Evaluate decision-making patterns
- Profile stress responses
- Analyze leadership potential
- Assess team dynamics

## Project Structure

```
CIABot/
├── src/
│   └── ciabot/
│       ├── core/
│       │   ├── ciaprofile.py    # Core profile generation
│       │   └── __init__.py
│       └── __init__.py          # Package initialization
├── docs/                        # Documentation
│   └── README.md               # This file
├── config/                     # Configuration files
│   ├── .env.example
│   └── requirements.txt
├── examples/                   # Example scripts
│   └── example_usage.py
├── scripts/                    # Utility scripts
├── output/                     # Generated output files
└── setup.py                    # Package setup file
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
from ciabot.core.ciaprofile import (
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

The repository includes an example script `analyze_text.py` that demonstrates how to use the CIA Profile Generator to analyze a text file. The script:

1. Reads text from a file
2. Generates various reports and profiles
3. Saves all outputs to the `output` directory with unique timestamps

To run the example:
```bash
python src/examples/analyze_text.py
```

## Analysis Dimensions

The CIA Profile Generator analyzes text across multiple dimensions:

1. **Core Psychological Analysis**
   - Personality traits
   - Emotional states
   - Cognitive patterns
   - Writing style
   - Linguistic markers

2. **Behavioral Analysis**
   - Neurolinguistic features
   - Dark triad traits
   - Behavioral predictions
   - Cognitive biases
   - Cultural lexicons

3. **Communication Analysis**
   - Primary and secondary communication styles
   - Communication strengths and challenges
   - Adaptation capacity
   - Information sharing patterns

4. **Decision-Making Assessment**
   - Decision-making approach
   - Risk tolerance
   - Information gathering style
   - Decision quality indicators

5. **Stress Response Profiling**
   - Coping mechanisms
   - Stress thresholds
   - Recovery patterns
   - Behavioral changes under pressure

6. **Leadership Potential**
   - Leadership style
   - Influence capacity
   - Vision development
   - Team building ability

7. **Team Dynamics**
   - Preferred team role
   - Collaboration style
   - Conflict handling
   - Team contribution

8. **Security Profile**
   - OPSEC weaknesses
   - Detectable patterns
   - Predictable behaviors
   - Countermeasures

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

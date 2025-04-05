# CIABot Text Analysis Examples

This directory contains example scripts for using the CIABot system to analyze various types of text.

## Text Analysis Script

The `analyze_text.py` script provides a flexible way to analyze any text file using the CIABot system.

### Usage

```bash
# Basic usage (analyzes author_sample.txt by default)
python src/examples/analyze_text.py

# Analyze a specific text file
python src/examples/analyze_text.py path/to/your/text/file.txt

# Specify output directory
python src/examples/analyze_text.py path/to/your/text/file.txt --output-dir my_reports

# Specify analysis type
python src/examples/analyze_text.py path/to/your/text/file.txt --analysis-type technical
```

### Command-line Arguments

- `file_path`: Path to the text file to analyze (optional, defaults to author_sample.txt)
- `--output-dir`, `-o`: Directory to save output files (default: output)
- `--analysis-type`, `-t`: Type of analysis to perform (choices: general, technical, social; default: general)

### Output Files

The script generates several output files in the specified output directory:

- `{unique_id}_prompt.txt`: The prompt used for analysis
- `{unique_id}_reasoning.txt`: The reasoning behind the analysis
- `{unique_id}_profile.json`: The structured psychological profile
- `{unique_id}_detailed_report.md`: A detailed markdown report
- `{unique_id}_intelligence_report.md`: An intelligence-focused report
- `{unique_id}_metrics.json`: Quantitative metrics about the text
- `{unique_id}_security_profile.json`: Security-related analysis

## Example Files

- `author_sample.txt`: A sample autobiographical text
- `example_profile.py`: Example of using the CIABot API directly
- `example_usage.py`: Basic usage examples 
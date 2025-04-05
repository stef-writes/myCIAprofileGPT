#!/usr/bin/env python3
"""
Analyze text using the CIA Profile Generator.
This script can analyze any text file, not just autobiographical content.
"""

import os
import json
import datetime
import argparse
from pathlib import Path
from dotenv import load_dotenv
from ciabot.core.ciaprofile import (
    generate_profile_prompt,
    analyze_text_with_reasoning,
    generate_structured_profile,
    generate_detailed_report,
    generate_intelligence_report,
    calculate_metrics,
    generate_security_profile
)
from ciabot.core.text_processor import TextProcessor

# Load environment variables
load_dotenv()

def main():
    """Run the analysis on the provided text file."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze text using the CIA Profile Generator')
    parser.add_argument('file_path', nargs='?', default=None, 
                        help='Path to the text file to analyze. If not provided, will use author_sample.txt')
    parser.add_argument('--output-dir', '-o', default='output',
                        help='Directory to save output files (default: output)')
    parser.add_argument('--analysis-type', '-t', default='general',
                        choices=['general', 'technical', 'social'],
                        help='Type of analysis to perform (default: general)')
    args = parser.parse_args()
    
    print("=== CIA Profile Generator: Text Analysis ===")
    
    # Create output directory if it doesn't exist
    output_dir = args.output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate unique identifier based on timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = f"profile_{timestamp}"

    # Get the path to the input file
    if args.file_path:
        # Use the provided file path
        input_file = Path(args.file_path)
        if not input_file.exists():
            print(f"Error: File not found: {input_file}")
            return
    else:
        # Default to author_sample.txt in the examples directory
        current_dir = Path(__file__).parent
        input_file = current_dir / "author_sample.txt"
        if not input_file.exists():
            print(f"Error: Default file not found: {input_file}")
            return

    # Process the text input using TextProcessor
    text_input = TextProcessor.from_file(str(input_file))
    print(f"Processing text from {text_input.source} with format {text_input.format}")
    print(f"Text length: {text_input.metadata['length']} characters")
    print(f"Analysis type: {args.analysis_type}")

    print(f"\nAnalyzing text with unique ID: {unique_id}")
    
    # Generate profile prompt
    print("\n1. Generating Profile Prompt...")
    prompt = generate_profile_prompt(text_input.content, analysis_type=args.analysis_type)
    with open(f"{output_dir}/{unique_id}_prompt.txt", "w") as f:
        f.write(prompt)
    print(f"Prompt saved to: {output_dir}/{unique_id}_prompt.txt")
    
    # Analyze text with reasoning
    print("\n2. Analyzing Text with Reasoning...")
    reasoning = analyze_text_with_reasoning(text_input.content, prompt)
    with open(f"{output_dir}/{unique_id}_reasoning.txt", "w") as f:
        f.write(reasoning)
    print(f"Reasoning analysis saved to: {output_dir}/{unique_id}_reasoning.txt")
    
    # Generate structured profile
    print("\n3. Generating Structured Profile...")
    profile = generate_structured_profile(text_input.content)
    if profile:
        # Convert profile to dictionary for JSON serialization
        profile_dict = profile.model_dump()
        with open(f"{output_dir}/{unique_id}_profile.json", "w") as f:
            json.dump(profile_dict, f, indent=2)
        print(f"Structured profile saved to: {output_dir}/{unique_id}_profile.json")
        
        # Generate detailed report
        print("\n4. Generating Detailed Report...")
        report = generate_detailed_report(profile)
        with open(f"{output_dir}/{unique_id}_detailed_report.md", "w") as f:
            f.write(report)
        print(f"Detailed report saved to: {output_dir}/{unique_id}_detailed_report.md")
        
        # Generate intelligence report
        print("\n5. Generating Intelligence Report...")
        intel_report = generate_intelligence_report(text_input.content)
        with open(f"{output_dir}/{unique_id}_intelligence_report.md", "w") as f:
            f.write(intel_report)
        print(f"Intelligence report saved to: {output_dir}/{unique_id}_intelligence_report.md")
        
        # Calculate metrics
        print("\n6. Calculating Metrics...")
        metrics = calculate_metrics(text_input.content)
        if metrics:
            # Convert metrics to dictionary for JSON serialization
            metrics_dict = metrics.model_dump()
            with open(f"{output_dir}/{unique_id}_metrics.json", "w") as f:
                json.dump(metrics_dict, f, indent=2)
            print(f"Metrics saved to: {output_dir}/{unique_id}_metrics.json")
        
        # Generate security profile
        print("\n7. Generating Security Profile...")
        security_profile = generate_security_profile(text_input.content)
        if security_profile:
            # Convert security profile to dictionary for JSON serialization
            security_dict = security_profile.model_dump()
            with open(f"{output_dir}/{unique_id}_security_profile.json", "w") as f:
                json.dump(security_dict, f, indent=2)
            print(f"Security profile saved to: {output_dir}/{unique_id}_security_profile.json")
    else:
        print("\nFailed to generate profile.")
    
    print(f"\n=== Analysis Complete: {unique_id} ===")
    print(f"All output files saved to the '{output_dir}' directory with prefix: {unique_id}")

if __name__ == "__main__":
    main() 
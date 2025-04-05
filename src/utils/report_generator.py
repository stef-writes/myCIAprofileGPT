#!/usr/bin/env python3
"""
Profile Report Generator

This script takes the comprehensive_profile.json file and generates a well-formatted,
structured profile report that presents the analysis in a professional, readable format.
"""

import json
import os
from datetime import datetime

def load_comprehensive_profile(filename="comprehensive_profile.json"):
    """Load the comprehensive profile from a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def format_trait(trait):
    """Format a personality trait for display."""
    return f"- **{trait['trait']}** (Confidence: {trait['confidence']})\n  {trait['evidence']}"

def format_emotion(emotion):
    """Format an emotional state for display."""
    return f"- **{emotion['emotion']}** (Intensity: {emotion['intensity']})\n  {emotion['evidence']}"

def format_pattern(pattern):
    """Format a cognitive pattern for display."""
    return f"- **{pattern['pattern']}** (Significance: {pattern['significance']})\n  {pattern['evidence']}"

def format_marker(marker):
    """Format a linguistic marker for display."""
    return f"- **{marker['marker']}**\n  Evidence: {marker['evidence']}\n  Interpretation: {marker['interpretation']}"

def format_prediction(prediction):
    """Format a behavioral prediction for display."""
    return f"- **Scenario**: {prediction['scenario']}\n  **Predicted Behavior**: {prediction['predicted_behavior']}\n  **Confidence**: {prediction['confidence']}\n  **Triggering Conditions**: {', '.join(prediction['triggering_conditions'])}\n  **Mitigation Strategies**: {', '.join(prediction['mitigation_strategies'])}"

def format_countermeasure(countermeasure):
    """Format a countermeasure for display."""
    return f"- {countermeasure}"

def generate_profile_report(profile, output_filename="profile_report.md"):
    """Generate a well-formatted profile report from the comprehensive profile."""
    # Create the report content
    report = f"""# PSYCHOLOGICAL PROFILE REPORT
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## EXECUTIVE SUMMARY

{profile['integrated_report'].split('## Core Assessment')[0]}

---

## CORE ASSESSMENT

{profile['integrated_report'].split('## Core Assessment')[1].split('## Motivation Layer')[0]}

---

## PERSONALITY PROFILE

### Personality Traits
{chr(10).join(format_trait(trait) for trait in profile['core_profile']['personality_traits'])}

### Emotional States
{chr(10).join(format_emotion(emotion) for emotion in profile['core_profile']['emotional_states'])}

### Cognitive Patterns
{chr(10).join(format_pattern(pattern) for pattern in profile['core_profile']['cognitive_patterns'])}

### Linguistic Markers
{chr(10).join(format_marker(marker) for marker in profile['core_profile']['linguistic_markers'])}

### Writing Style
- **Formality**: {profile['core_profile']['writing_style']['formality']}
- **Complexity**: {profile['core_profile']['writing_style']['complexity']}
- **Emotionality**: {profile['core_profile']['writing_style']['emotionality']}
- **Evidence**: {profile['core_profile']['writing_style']['evidence']}

---

## NEUROLINGUISTIC ANALYSIS

### Syntactic Complexity
- **Overall**: {profile['core_profile']['neurolinguistic_features']['syntactic_complexity']}

### Pronoun Usage
- **I/Me/My**: {profile['core_profile']['neurolinguistic_features']['pronoun_ratio']['I']}
- **We/Us/Our**: {profile['core_profile']['neurolinguistic_features']['pronoun_ratio']['we']}
- **You/Your**: {profile['core_profile']['neurolinguistic_features']['pronoun_ratio']['you']}
- **They/Them/Their**: {profile['core_profile']['neurolinguistic_features']['pronoun_ratio']['they']}

### Temporal Orientation
- **Past**: {profile['core_profile']['neurolinguistic_features']['temporal_orientation']['past']}
- **Present**: {profile['core_profile']['neurolinguistic_features']['temporal_orientation']['present']}
- **Future**: {profile['core_profile']['neurolinguistic_features']['temporal_orientation']['future']}

### Language Characteristics
- **Hedge Density**: {profile['core_profile']['neurolinguistic_features']['hedge_density']}
- **Certainty Score**: {profile['core_profile']['neurolinguistic_features']['certainty_score']}

### Evidence
{chr(10).join(f"- {evidence}" for evidence in profile['core_profile']['neurolinguistic_features']['evidence'])}

---

## PSYCHOLOGICAL ANALYSIS

### Dark Triad Assessment
- **Narcissism**: {profile['core_profile']['dark_triad_profile']['narcissism']}
- **Machiavellianism**: {profile['core_profile']['dark_triad_profile']['machiavellianism']}
- **Psychopathy**: {profile['core_profile']['dark_triad_profile']['psychopathy']}

### Behavioral Manifestations
{chr(10).join(f"- {manifestation}" for manifestation in profile['core_profile']['dark_triad_profile']['behavioral_manifestations'])}

### Operational Risks
{chr(10).join(f"- {risk}" for risk in profile['core_profile']['dark_triad_profile']['operational_risks'])}

---

## BEHAVIORAL PREDICTIONS

{chr(10).join(format_prediction(prediction) for prediction in profile['core_profile']['behavioral_predictions'])}

---

## COGNITIVE BIASES

{chr(10).join(f"- {bias}" for bias in profile['core_profile']['cognitive_biases'])}

---

## CULTURAL LEXICONS

{chr(10).join(f"- {lexicon}" for lexicon in profile['core_profile']['cultural_lexicons'])}

---

## BEHAVIORAL METRICS

- **Persuasion Susceptibility**: {profile['metrics']['persuasion_susceptibility']}
- **Deception Capacity**: {profile['metrics']['deception_capacity']}
- **Information Hoarding**: {profile['metrics']['information_hoarding']}
- **Risk Tolerance**: {profile['metrics']['risk_tolerance']}
- **Group Affiliation**: {profile['metrics']['group_affiliation']}
- **Cognitive Rigidity**: {profile['metrics']['cognitive_rigidity']}

---

## SECURITY PROFILE

### OPSEC Weaknesses
{chr(10).join(format_countermeasure(weakness) for weakness in profile['security_analysis']['opsec_weaknesses'])}

### Detectable Patterns
{chr(10).join(format_countermeasure(pattern) for pattern in profile['security_analysis']['detectable_patterns'])}

### Predictable Behaviors
{chr(10).join(format_countermeasure(behavior) for behavior in profile['security_analysis']['predictable_behaviors'])}

### Suggested Countermeasures
{chr(10).join(format_countermeasure(countermeasure) for countermeasure in profile['security_analysis']['suggested_countermeasures'])}

---

## MOTIVATION LAYER

{profile['integrated_report'].split('## Motivation Layer')[1].split('## Psychological & Behavioral Risk Profile')[0]}

---

## PSYCHOLOGICAL & BEHAVIORAL RISK PROFILE

{profile['integrated_report'].split('## Psychological & Behavioral Risk Profile')[1].split('## Strategic Liabilities')[0]}

---

## STRATEGIC LIABILITIES

{profile['integrated_report'].split('## Strategic Liabilities')[1].split('## Unique Operational Hazards')[0]}

---

## UNIQUE OPERATIONAL HAZARDS

{profile['integrated_report'].split('## Unique Operational Hazards')[1].split('## Strengths Worth Leveraging')[0]}

---

## STRENGTHS WORTH LEVERAGING

{profile['integrated_report'].split('## Strengths Worth Leveraging')[1].split('## Structural Recommendations')[0]}

---

## STRUCTURAL RECOMMENDATIONS

{profile['integrated_report'].split('## Structural Recommendations')[1].split('## Intelligence Summary')[0]}

---

## INTELLIGENCE SUMMARY

{profile['integrated_report'].split('## Intelligence Summary')[1].split('## Final Verdict')[0]}

---

## FINAL VERDICT

{profile['integrated_report'].split('## Final Verdict')[1]}

---

## APPENDIX: SAMPLE ANALYSIS

### Sample 1: Emotional Text
```
{profile['integrated_report'].split('## Core Assessment')[0].split('##')[0]}
```

### Sample 2: Analytical Text
```
{profile['integrated_report'].split('## Core Assessment')[0].split('##')[1] if len(profile['integrated_report'].split('## Core Assessment')[0].split('##')) > 1 else "No analytical text sample available."}
```

### Sample 3: Complex Text
```
{profile['integrated_report'].split('## Core Assessment')[0].split('##')[2] if len(profile['integrated_report'].split('## Core Assessment')[0].split('##')) > 2 else "No complex text sample available."}
```
"""
    
    # Write the report to a file
    with open(output_filename, 'w') as f:
        f.write(report)
    
    print(f"Profile report generated and saved to {output_filename}")
    return output_filename

def main():
    """Generate a profile report from the comprehensive profile."""
    # Load the comprehensive profile
    try:
        profile = load_comprehensive_profile()
        print("Comprehensive profile loaded successfully.")
    except FileNotFoundError:
        print("Error: comprehensive_profile.json not found. Please run example_profile.py first.")
        return
    except json.JSONDecodeError:
        print("Error: comprehensive_profile.json is not valid JSON.")
        return
    
    # Generate the profile report
    output_file = generate_profile_report(profile)
    
    # Print instructions for viewing the report
    print("\nTo view the report:")
    print(f"1. Open {output_file} in a Markdown viewer")
    print("2. Or convert it to HTML/PDF using a Markdown converter")
    print("3. Or view it directly in a text editor")

if __name__ == "__main__":
    main() 
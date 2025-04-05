#!/usr/bin/env python3
"""
Example script demonstrating the CIA Profile Generator with a complex text sample.
This script processes various types of text and generates a comprehensive psychological profile
that integrates all analyses into a single consolidated output.
"""

import json
from ciaprofile import (
    generate_structured_profile,
    generate_detailed_report,
    generate_intelligence_report,
    calculate_metrics,
    generate_security_profile
)

def generate_comprehensive_profile(text_samples, tone="balanced"):
    """
    Generate a comprehensive profile that integrates analysis from multiple text samples.
    
    Args:
        text_samples (list): List of text samples to analyze
        tone (str): Analysis tone ("positive", "negative", or "balanced")
    
    Returns:
        dict: Comprehensive profile containing integrated analysis
    """
    print(f"\nGenerating comprehensive profile with {tone} tone...")
    
    # Initialize comprehensive profile
    comprehensive_profile = {
        "core_profile": None,
        "neurolinguistic_analysis": [],
        "psychological_analysis": [],
        "behavioral_analysis": [],
        "security_analysis": None,
        "metrics": None,
        "integrated_report": ""
    }
    
    # Process each text sample
    for i, text in enumerate(text_samples, 1):
        print(f"\nProcessing text sample {i}/{len(text_samples)}...")
        
        # Generate structured profile
        profile = generate_structured_profile(text, tone)
        if profile:
            if not comprehensive_profile["core_profile"]:
                comprehensive_profile["core_profile"] = profile
            else:
                # Merge new findings with existing profile
                comprehensive_profile["core_profile"].personality_traits.extend(
                    [trait for trait in profile.personality_traits 
                     if trait not in comprehensive_profile["core_profile"].personality_traits]
                )
                comprehensive_profile["core_profile"].emotional_states.extend(
                    [state for state in profile.emotional_states 
                     if state not in comprehensive_profile["core_profile"].emotional_states]
                )
                comprehensive_profile["core_profile"].cognitive_patterns.extend(
                    [pattern for pattern in profile.cognitive_patterns 
                     if pattern not in comprehensive_profile["core_profile"].cognitive_patterns]
                )
            
            # Collect neurolinguistic features
            if profile.neurolinguistic_features:
                comprehensive_profile["neurolinguistic_analysis"].append({
                    "text_sample": i,
                    "features": profile.neurolinguistic_features
                })
            
            # Collect psychological analysis
            if profile.dark_triad_profile:
                comprehensive_profile["psychological_analysis"].append({
                    "text_sample": i,
                    "dark_triad": profile.dark_triad_profile
                })
            
            # Collect behavioral analysis
            if profile.behavioral_predictions:
                comprehensive_profile["behavioral_analysis"].append({
                    "text_sample": i,
                    "predictions": profile.behavioral_predictions
                })
    
    # Generate security profile from the most complex text sample
    complex_text = max(text_samples, key=len)
    security_profile = generate_security_profile(complex_text)
    if security_profile:
        comprehensive_profile["security_analysis"] = security_profile
    
    # Calculate metrics from the most complex text sample
    metrics = calculate_metrics(complex_text)
    if metrics:
        comprehensive_profile["metrics"] = metrics
    
    # Generate integrated report
    report = generate_intelligence_report(complex_text, tone)
    if report:
        comprehensive_profile["integrated_report"] = report
    
    return comprehensive_profile

def save_comprehensive_profile(profile, filename="comprehensive_profile.json"):
    """Save the comprehensive profile to a JSON file."""
    # Convert Pydantic models to dictionaries
    serializable_profile = {
        "core_profile": profile["core_profile"].model_dump() if profile["core_profile"] else None,
        "neurolinguistic_analysis": [
            {
                "text_sample": item["text_sample"],
                "features": item["features"].model_dump() if item["features"] else None
            }
            for item in profile["neurolinguistic_analysis"]
        ],
        "psychological_analysis": [
            {
                "text_sample": item["text_sample"],
                "dark_triad": item["dark_triad"].model_dump() if item["dark_triad"] else None
            }
            for item in profile["psychological_analysis"]
        ],
        "behavioral_analysis": [
            {
                "text_sample": item["text_sample"],
                "predictions": item["predictions"].model_dump() if hasattr(item["predictions"], "model_dump") else []
            }
            for item in profile["behavioral_analysis"]
        ],
        "security_analysis": profile["security_analysis"].model_dump() if profile["security_analysis"] else None,
        "metrics": profile["metrics"].model_dump() if profile["metrics"] else None,
        "integrated_report": profile["integrated_report"]
    }
    
    with open(filename, 'w') as f:
        json.dump(serializable_profile, f, indent=2)
    print(f"\nComprehensive profile saved to {filename}")

def main():
    """Run the example profile generator."""
    # Define text samples to analyze
    text_samples = [
        # Emotional text sample
        """I can't believe this is happening again. Every time I try to make progress, 
        something always gets in the way. It's like the universe is conspiring against me. 
        I'm so frustrated and angry, but mostly I'm just tired of fighting.""",
        
        # Analytical text sample
        """After analyzing the data patterns, I've identified several key correlations 
        between user behavior and system performance. The metrics indicate a 23% improvement 
        in response times when implementing the new caching strategy. However, there are 
        still some edge cases we need to address.""",
        
        # Complex text sample
        """I've been analyzing the patterns in our organization's security protocols, and 
        I've noticed some significant vulnerabilities. While I understand the need for 
        efficiency, I believe our current approach is dangerously naive. The way some of 
        my colleagues handle sensitive information is frankly concerning - they seem to 
        think that basic encryption is sufficient, but I know better. I've developed a 
        comprehensive framework for identifying and exploiting these weaknesses, though 
        I haven't shared it with anyone yet. The beauty of my approach is that it's 
        virtually undetectable - I've tested it extensively in my own environment."""
    ]
    
    # Generate comprehensive profile with balanced tone
    profile = generate_comprehensive_profile(text_samples, tone="balanced")
    
    # Save the comprehensive profile
    save_comprehensive_profile(profile)
    
    # Print summary of findings
    print("\nProfile Summary:")
    if profile["core_profile"]:
        print(f"\nCore Profile:")
        print(f"- Personality traits identified: {len(profile['core_profile'].personality_traits)}")
        print(f"- Emotional states detected: {len(profile['core_profile'].emotional_states)}")
        print(f"- Cognitive patterns observed: {len(profile['core_profile'].cognitive_patterns)}")
    
    if profile["neurolinguistic_analysis"]:
        print(f"\nNeurolinguistic Analysis:")
        print(f"- Samples analyzed: {len(profile['neurolinguistic_analysis'])}")
    
    if profile["psychological_analysis"]:
        print(f"\nPsychological Analysis:")
        print(f"- Samples analyzed: {len(profile['psychological_analysis'])}")
    
    if profile["behavioral_analysis"]:
        print(f"\nBehavioral Analysis:")
        print(f"- Samples analyzed: {len(profile['behavioral_analysis'])}")
    
    if profile["metrics"]:
        print(f"\nBehavioral Metrics:")
        print(f"- Persuasion susceptibility: {profile['metrics'].persuasion_susceptibility}")
        print(f"- Deception capacity: {profile['metrics'].deception_capacity}")
        print(f"- Risk tolerance: {profile['metrics'].risk_tolerance}")
    
    if profile["security_analysis"]:
        print(f"\nSecurity Analysis:")
        print(f"- OPSEC weaknesses identified: {len(profile['security_analysis'].opsec_weaknesses)}")
        print(f"- Detectable patterns found: {len(profile['security_analysis'].detectable_patterns)}")
        print(f"- Countermeasures suggested: {len(profile['security_analysis'].suggested_countermeasures)}")

if __name__ == "__main__":
    main() 
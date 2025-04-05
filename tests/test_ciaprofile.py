#!/usr/bin/env python3
"""
Test script for ciaprofile.py
This script demonstrates how to use the CIA Profile Generator.
"""

from src.core.ciaprofile import (
    generate_profile_prompt,
    analyze_text_with_reasoning,
    generate_structured_profile,
    generate_detailed_report,
    generate_intelligence_report,
    calculate_metrics,
    generate_security_profile
)

def test_prompt_generation():
    """Test the prompt generation functionality."""
    print("\n=== Testing Prompt Generation ===")
    
    # Test text for prompt generation
    text = "I can't believe how frustrating this is. Everything keeps going wrong and nobody seems to care. I've tried everything I can think of, but nothing works. Maybe I'm just not good enough."
    print(f"\nGenerating prompt for text: '{text[:50]}...'")
    
    # Test with different tones
    for tone in ["positive", "negative", "balanced"]:
        print(f"\n--- Testing {tone.upper()} tone ---")
        prompt = generate_profile_prompt(text, tone)
        if prompt:
            print(f"Generated prompt ({tone} tone):\n{prompt[:200]}...")
    
    return prompt

def test_reasoning_analysis(prompt):
    """Test the reasoning analysis functionality."""
    print("\n=== Testing Reasoning Analysis ===")
    
    # Test text for reasoning analysis
    text = "I can't believe how frustrating this is. Everything keeps going wrong and nobody seems to care. I've tried everything I can think of, but nothing works. Maybe I'm just not good enough."
    print(f"\nAnalyzing text with reasoning: '{text}'")
    
    analysis = analyze_text_with_reasoning(text, prompt)
    if analysis:
        print(f"Analysis:\n{analysis[:200]}...")
    
    return analysis

def test_structured_profile():
    """Test the structured profile generation functionality."""
    print("\n=== Testing Structured Profile Generation ===")
    
    # Test text for profile generation
    text = """
    I've been working on this project for months now, and I'm really proud of what we've accomplished. 
    The team has been amazing, and we've overcome so many challenges together. 
    I think our approach was innovative, and I'm excited to see how it will be received.
    """
    print(f"\nGenerating structured profile for text: '{text[:50]}...'")
    
    # Test with different tones
    for tone in ["positive", "negative", "balanced"]:
        print(f"\n--- Testing {tone.upper()} tone ---")
        profile = generate_structured_profile(text, tone)
        if profile:
            print(f"Generated profile ({tone} tone): {profile.model_dump_json(indent=2)[:200]}...")
            
            # Check for new features
            if profile.neurolinguistic_features:
                print("\nNeurolinguistic Features:")
                print(f"Syntactic complexity: {profile.neurolinguistic_features.syntactic_complexity}")
                print(f"Pronoun ratio: {profile.neurolinguistic_features.pronoun_ratio}")
                print(f"Temporal orientation: {profile.neurolinguistic_features.temporal_orientation}")
                print(f"Hedge density: {profile.neurolinguistic_features.hedge_density}")
                print(f"Certainty score: {profile.neurolinguistic_features.certainty_score}")
            
            if profile.dark_triad_profile:
                print("\nDark Triad Profile:")
                print(f"Narcissism: {profile.dark_triad_profile.narcissism}")
                print(f"Machiavellianism: {profile.dark_triad_profile.machiavellianism}")
                print(f"Psychopathy: {profile.dark_triad_profile.psychopathy}")
                print("Behavioral manifestations:")
                for manifestation in profile.dark_triad_profile.behavioral_manifestations:
                    print(f"- {manifestation}")
            
            if profile.behavioral_predictions:
                print("\nBehavioral Predictions:")
                for prediction in profile.behavioral_predictions:
                    print(f"Scenario: {prediction.scenario}")
                    print(f"Predicted behavior: {prediction.predicted_behavior}")
                    print(f"Confidence: {prediction.confidence}")
    
    return profile

def test_detailed_report(profile):
    """Test the detailed report generation functionality."""
    print("\n=== Testing Detailed Report Generation ===")
    
    if not profile:
        print("No profile available for report generation.")
        return
    
    # Test with different tones
    for tone in ["positive", "negative", "balanced"]:
        print(f"\n--- Testing {tone.upper()} tone ---")
        report = generate_detailed_report(profile, tone)
        if report:
            print(f"Generated report ({tone} tone):\n{report[:200]}...")
    
    return report

def test_intelligence_report():
    """Test the direct intelligence report generation functionality."""
    print("\n=== Testing Intelligence Report Generation ===")
    
    # Test text for intelligence report
    text = """
    I've been thinking about how to revolutionize the way people interact with information.
    The current systems are so limited and don't capture the full complexity of human thought.
    I want to build something that truly understands the nuances of cognition and can adapt
    to different thinking styles. I've been sketching out some ideas, but I need to find
    the right approach. There's so much potential here, but I'm not sure where to start.
    """
    print(f"\nGenerating intelligence report for text: '{text[:50]}...'")
    
    # Test with different tones
    for tone in ["positive", "negative", "balanced"]:
        print(f"\n--- Testing {tone.upper()} tone ---")
        report = generate_intelligence_report(text, tone)
        if report:
            print(f"Generated intelligence report ({tone} tone):\n{report[:200]}...")
    
    return report

def test_metrics_calculation():
    """Test the metrics calculation functionality."""
    print("\n=== Testing Metrics Calculation ===")
    
    # Test text for metrics calculation
    text = """
    I've been analyzing the patterns in our organization's security protocols, and I've noticed some significant vulnerabilities. 
    While I understand the need for efficiency, I believe our current approach is dangerously naive. The way some of my colleagues 
    handle sensitive information is frankly concerning - they seem to think that basic encryption is sufficient, but I know better.
    
    I've developed a comprehensive framework for identifying and exploiting these weaknesses, though I haven't shared it with anyone yet. 
    The beauty of my approach is that it's virtually undetectable - I've tested it extensively in my own environment. I'm particularly 
    proud of how I've managed to maintain access to systems long after my initial entry points were supposedly closed.
    """
    print(f"\nCalculating metrics for text: '{text[:50]}...'")
    
    metrics = calculate_metrics(text)
    if metrics:
        print("\nCalculated Metrics:")
        print(f"Persuasion susceptibility: {metrics.persuasion_susceptibility}")
        print(f"Deception capacity: {metrics.deception_capacity}")
        print(f"Information hoarding: {metrics.information_hoarding}")
        print(f"Risk tolerance: {metrics.risk_tolerance}")
        print(f"Group affiliation: {metrics.group_affiliation}")
        print(f"Cognitive rigidity: {metrics.cognitive_rigidity}")
    
    return metrics

def test_security_profile():
    """Test the security profile generation functionality."""
    print("\n=== Testing Security Profile Generation ===")
    
    # Test text for security profile
    text = """
    I've been analyzing the patterns in our organization's security protocols, and I've noticed some significant vulnerabilities. 
    While I understand the need for efficiency, I believe our current approach is dangerously naive. The way some of my colleagues 
    handle sensitive information is frankly concerning - they seem to think that basic encryption is sufficient, but I know better.
    
    I've developed a comprehensive framework for identifying and exploiting these weaknesses, though I haven't shared it with anyone yet. 
    The beauty of my approach is that it's virtually undetectable - I've tested it extensively in my own environment. I'm particularly 
    proud of how I've managed to maintain access to systems long after my initial entry points were supposedly closed.
    """
    print(f"\nGenerating security profile for text: '{text[:50]}...'")
    
    security_profile = generate_security_profile(text)
    if security_profile:
        print("\nSecurity Profile:")
        print("OPSEC Weaknesses:")
        for weakness in security_profile.opsec_weaknesses:
            print(f"- {weakness}")
        
        print("\nDetectable Patterns:")
        for pattern in security_profile.detectable_patterns:
            print(f"- {pattern}")
        
        print("\nPredictable Behaviors:")
        for behavior in security_profile.predictable_behaviors:
            print(f"- {behavior}")
        
        print("\nSuggested Countermeasures:")
        for countermeasure in security_profile.suggested_countermeasures:
            print(f"- {countermeasure}")
    
    return security_profile

def main():
    """Run all tests."""
    print("Testing CIA Profile Generator functionality")
    
    # Test prompt generation
    prompt = test_prompt_generation()
    
    # Test reasoning analysis
    if prompt:
        analysis = test_reasoning_analysis(prompt)
    
    # Test structured profile generation
    profile = test_structured_profile()
    
    # Test detailed report generation
    if profile:
        report = test_detailed_report(profile)
    
    # Test intelligence report generation
    intelligence_report = test_intelligence_report()
    
    # Test metrics calculation
    metrics = test_metrics_calculation()
    
    # Test security profile generation
    security_profile = test_security_profile()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main() 
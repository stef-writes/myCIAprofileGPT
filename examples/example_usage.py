#!/usr/bin/env python3
"""
Example script demonstrating how to use the CIA Profile Generator.
"""

from ciabot.core.ciaprofile import (
    generate_profile_prompt,
    analyze_text_with_reasoning,
    generate_structured_profile,
    generate_detailed_report,
    generate_intelligence_report,
    calculate_metrics,
    generate_security_profile
)

def main():
    """Run a comprehensive example."""
    print("=== CIA Profile Generator Example ===")
    
    # Sample text to analyze
    text = """
    I've been analyzing the patterns in our organization's security protocols, and 
    I've noticed some significant vulnerabilities. While I understand the need for 
    efficiency, I believe our current approach is dangerously naive. The way some of 
    my colleagues handle sensitive information is frankly concerning.
    """
    
    print("\n1. Generating Profile Prompt...")
    prompt = generate_profile_prompt(text, tone="balanced")
    print(f"Prompt generated: {len(prompt)} characters")
    
    print("\n2. Analyzing Text with Reasoning...")
    analysis = analyze_text_with_reasoning(text, prompt)
    print(f"Analysis completed: {len(analysis)} characters")
    
    print("\n3. Generating Structured Profile...")
    profile = generate_structured_profile(text, tone="balanced")
    if profile:
        print("\nProfile generated successfully!")
        print(f"Personality traits identified: {len(profile.personality_traits)}")
        print(f"Emotional states detected: {len(profile.emotional_states)}")
        print(f"Cognitive patterns observed: {len(profile.cognitive_patterns)}")
        
        print("\n4. Generating Detailed Report...")
        report = generate_detailed_report(profile)
        print(f"Detailed report generated: {len(report)} characters")
        
        print("\n5. Generating Intelligence Report...")
        intel_report = generate_intelligence_report(text)
        print(f"Intelligence report generated: {len(intel_report)} characters")
        
        print("\n6. Calculating Metrics...")
        metrics = calculate_metrics(text)
        print("Metrics calculated:")
        print(f"- Persuasion susceptibility: {metrics.persuasion_susceptibility}")
        print(f"- Deception capacity: {metrics.deception_capacity}")
        print(f"- Risk tolerance: {metrics.risk_tolerance}")
        
        print("\n7. Generating Security Profile...")
        security_profile = generate_security_profile(text)
        print("Security profile generated:")
        print(f"- OPSEC weaknesses identified: {len(security_profile.opsec_weaknesses)}")
        print(f"- Detectable patterns found: {len(security_profile.detectable_patterns)}")
        print(f"- Countermeasures suggested: {len(security_profile.suggested_countermeasures)}")
    else:
        print("\nFailed to generate profile.")
    
    print("\n=== Example Completed ===")

if __name__ == "__main__":
    main() 
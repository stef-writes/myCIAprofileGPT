#!/usr/bin/env python3
"""
CIA Profile Generator

This module uses OpenAI's ChatGPT API to generate CIA-level psychological profiles
based on text analysis. It leverages structured outputs, prompt generation, and
enhanced reasoning to create comprehensive profiles.
"""

import os
import json
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI
from ..templates.profile_templates import get_profile_template, get_example_profile

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===== STRUCTURED OUTPUTS =====

class PersonalityTrait(BaseModel):
    """A personality trait with evidence and confidence level."""
    trait: str
    evidence: str
    confidence: float = Field(..., ge=0.0, le=1.0)

class EmotionalState(BaseModel):
    """An emotional state with evidence and intensity."""
    emotion: str
    evidence: str
    intensity: float = Field(..., ge=0.0, le=1.0)

class CognitivePattern(BaseModel):
    """A cognitive pattern with evidence and significance."""
    pattern: str
    evidence: str
    significance: float = Field(..., ge=0.0, le=1.0)

class WritingStyle(BaseModel):
    """Analysis of writing style elements."""
    formality: float = Field(..., ge=0.0, le=1.0)
    complexity: float = Field(..., ge=0.0, le=1.0)
    emotionality: float = Field(..., ge=0.0, le=1.0)
    evidence: str

class LinguisticMarker(BaseModel):
    """A linguistic marker with evidence and interpretation."""
    marker: str
    evidence: str
    interpretation: str

class NeurolinguisticFeature(BaseModel):
    """Quantified neurolinguistic features with interpretation."""
    syntactic_complexity: float = Field(..., ge=0.0, le=1.0)
    pronoun_ratio: Dict[str, float]  # I/we/you/they ratios
    temporal_orientation: Dict[str, float]  # Past/present/future
    hedge_density: float = Field(..., ge=0.0, le=1.0)
    certainty_score: float = Field(..., ge=0.0, le=1.0)
    evidence: List[str]

class DarkTriadProfile(BaseModel):
    """Dark Triad trait analysis with behavioral predictions."""
    narcissism: float = Field(..., ge=0.0, le=1.0)
    machiavellianism: float = Field(..., ge=0.0, le=1.0)
    psychopathy: float = Field(..., ge=0.0, le=1.0)
    behavioral_manifestations: List[str]
    operational_risks: List[str]

class BehavioralPrediction(BaseModel):
    """Predicted behavior with confidence and triggers."""
    scenario: str
    predicted_behavior: str
    confidence: float
    triggering_conditions: List[str]
    mitigation_strategies: List[str]

class ProfileMetrics(BaseModel):
    """Quantitative assessment metrics"""
    persuasion_susceptibility: float = Field(..., ge=0.0, le=1.0)
    deception_capacity: float = Field(..., ge=0.0, le=1.0)
    information_hoarding: float = Field(..., ge=0.0, le=1.0)
    risk_tolerance: float = Field(..., ge=0.0, le=1.0)
    group_affiliation: float = Field(..., ge=0.0, le=1.0)
    cognitive_rigidity: float = Field(..., ge=0.0, le=1.0)

class SecurityProfile(BaseModel):
    """Security-oriented risk assessment"""
    opsec_weaknesses: List[str]
    detectable_patterns: List[str]
    predictable_behaviors: List[str]
    suggested_countermeasures: List[str]

class PsychologicalProfile(BaseModel):
    """A comprehensive psychological profile."""
    personality_traits: List[PersonalityTrait]
    emotional_states: List[EmotionalState]
    cognitive_patterns: List[CognitivePattern]
    writing_style: WritingStyle
    linguistic_markers: List[LinguisticMarker]
    overall_assessment: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    potential_biases: List[str]
    limitations: List[str]
    # New fields from enhancements
    neurolinguistic_features: Optional[NeurolinguisticFeature] = None
    dark_triad_profile: Optional[DarkTriadProfile] = None
    behavioral_predictions: Optional[List[BehavioralPrediction]] = None
    cognitive_biases: Optional[List[str]] = None
    cultural_lexicons: Optional[List[str]] = None
    profile_metrics: Optional[ProfileMetrics] = None
    security_profile: Optional[SecurityProfile] = None

# ===== PROMPT GENERATION =====

def generate_profile_prompt(text: str, tone: str = "balanced") -> str:
    """
    Generate a specialized prompt for psychological profiling.
    
    Args:
        text: The text to analyze
        tone: The desired tone of the profile ("positive", "negative", or "balanced")
        
    Returns:
        A detailed prompt for the model
    """
    try:
        # Get the appropriate template based on the desired tone
        template = get_profile_template(tone)
        
        # Get an example profile for reference
        example = get_example_profile(tone)
        
        # Identify the type of text to provide more specific instructions
        text_type_prompt = """
        First, identify the type of text you're analyzing:
        - Direct statements: Personal thoughts, feelings, or experiences
        - Random excerpts: Fragments of text without clear context
        - ChatGPT conversations: Interactions with AI, including prompts and responses
        - Essays: Structured written content with a clear purpose
        - Text messages: Informal communication, possibly fragmented
        - Other: Identify the type if it doesn't fit the above categories
        
        Then, adapt your analysis approach based on the text type:
        - For direct statements: Focus on emotional content, personal values, and self-perception
        - For random excerpts: Look for patterns and themes that might reveal underlying psychology
        - For ChatGPT conversations: Analyze both the user's prompts and how they respond to AI
        - For essays: Examine argument structure, evidence selection, and conclusion formation
        - For text messages: Consider informal language patterns, emoji usage, and communication style
        """
        
        # Advanced analysis directives
        advanced_directives = """
        **Neurolinguistic Focus:**
        1. Calculate pronoun ratios (I/we/they) and map to self-concept
        2. Analyze verb tense distribution for temporal orientation
        3. Quantify hedge words (might/could) vs definitive language
        4. Measure lexical density and syntactic complexity
        5. Identify semantic primes in emotional expression

        **Psychological Deep Dive:**
        1. Apply Dark Triad detection framework
        2. Map language to Hermann Brain Dominance model
        3. Analyze conceptual metaphors (Lakoffian frames)
        4. Detect cognitive dissonance patterns
        5. Identify narrative schema violations

        **Behavioral Forecasting:**
        1. Predict 3 most likely actions under stress
        2. Identify optimal persuasion strategies
        3. Determine vulnerability to recruitment
        4. Assess deception probability patterns
        5. Model information sensitivity thresholds
        """
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": f"""
                    {template}
                    
                    {text_type_prompt}
                    
                    {advanced_directives}
                    
                    Here is an example of the kind of analysis we're looking for:
                    
                    {example}
                    
                    Use this example as a reference for the level of detail, structure, and tone we want.
                    """
                },
                {"role": "user", "content": f"Create a prompt for analyzing this text: {text[:100]}..."},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating profile prompt: {str(e)}")
        return None

# ===== REASONING =====

def analyze_text_with_reasoning(text: str, prompt: str) -> str:
    """
    Analyze text using enhanced reasoning to generate insights.
    
    Args:
        text: The text to analyze
        prompt: The specialized prompt to use
        
    Returns:
        Detailed analysis as a string
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error analyzing text with reasoning: {str(e)}")
        return None

def generate_structured_profile(text: str, tone: str = "balanced") -> PsychologicalProfile:
    """
    Generate a structured psychological profile from text.
    
    Args:
        text: The text to analyze
        tone: The desired tone of the profile ("positive", "negative", or "balanced")
        
    Returns:
        A structured psychological profile
    """
    try:
        # First, generate a specialized prompt
        prompt = generate_profile_prompt(text, tone)
        if not prompt:
            raise ValueError("Failed to generate profile prompt")
        
        # Then, analyze the text with enhanced reasoning
        analysis = analyze_text_with_reasoning(text, prompt)
        if not analysis:
            raise ValueError("Failed to analyze text with reasoning")
        
        # Finally, extract structured data using the model's parse capability
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    You are an expert in psychological profiling and intelligence analysis.
                    Based on the provided analysis, extract a structured psychological profile
                    that follows the specified schema. Ensure all fields are properly filled
                    with relevant information from the analysis.
                    
                    Your response MUST be a valid JSON object with the following structure:
                    {
                      "personality_traits": [
                        {
                          "trait": "string",
                          "evidence": "string",
                          "confidence": number between 0 and 1
                        }
                      ],
                      "emotional_states": [
                        {
                          "emotion": "string",
                          "evidence": "string",
                          "intensity": number between 0 and 1
                        }
                      ],
                      "cognitive_patterns": [
                        {
                          "pattern": "string",
                          "evidence": "string",
                          "significance": number between 0 and 1
                        }
                      ],
                      "writing_style": {
                        "formality": number between 0 and 1,
                        "complexity": number between 0 and 1,
                        "emotionality": number between 0 and 1,
                        "evidence": "string"
                      },
                      "linguistic_markers": [
                        {
                          "marker": "string",
                          "evidence": "string",
                          "interpretation": "string"
                        }
                      ],
                      "overall_assessment": "string",
                      "confidence_score": number between 0 and 1,
                      "potential_biases": ["string"],
                      "limitations": ["string"],
                      "neurolinguistic_features": {
                        "syntactic_complexity": number between 0 and 1,
                        "pronoun_ratio": {
                          "I": number between 0 and 1,
                          "we": number between 0 and 1,
                          "you": number between 0 and 1,
                          "they": number between 0 and 1
                        },
                        "temporal_orientation": {
                          "past": number between 0 and 1,
                          "present": number between 0 and 1,
                          "future": number between 0 and 1
                        },
                        "hedge_density": number between 0 and 1,
                        "certainty_score": number between 0 and 1,
                        "evidence": ["string"]
                      },
                      "dark_triad_profile": {
                        "narcissism": number between 0 and 1,
                        "machiavellianism": number between 0 and 1,
                        "psychopathy": number between 0 and 1,
                        "behavioral_manifestations": ["string"],
                        "operational_risks": ["string"]
                      },
                      "behavioral_predictions": [
                        {
                          "scenario": "string",
                          "predicted_behavior": "string",
                          "confidence": number between 0 and 1,
                          "triggering_conditions": ["string"],
                          "mitigation_strategies": ["string"]
                        }
                      ],
                      "cognitive_biases": ["string"],
                      "cultural_lexicons": ["string"],
                      "profile_metrics": {
                        "persuasion_susceptibility": number between 0 and 1,
                        "deception_capacity": number between 0 and 1,
                        "information_hoarding": number between 0 and 1,
                        "risk_tolerance": number between 0 and 1,
                        "group_affiliation": number between 0 and 1,
                        "cognitive_rigidity": number between 0 and 1
                      },
                      "security_profile": {
                        "opsec_weaknesses": ["string"],
                        "detectable_patterns": ["string"],
                        "predictable_behaviors": ["string"],
                        "suggested_countermeasures": ["string"]
                      }
                    }
                    
                    Return your response as a valid JSON object that matches this schema exactly.
                    """
                },
                {"role": "user", "content": f"Analysis: {analysis}\n\nExtract a structured profile from this analysis and return it as JSON."},
            ],
            response_format={"type": "json_object"},
        )
        
        # Parse the JSON response into a PsychologicalProfile object
        profile_data = json.loads(completion.choices[0].message.content)
        return PsychologicalProfile(**profile_data)
    except Exception as e:
        print(f"Error generating structured profile: {str(e)}")
        return None

def generate_detailed_report(profile: PsychologicalProfile, tone: str = "balanced") -> str:
    """
    Generate a detailed report from a structured profile.
    
    Args:
        profile: The structured psychological profile
        tone: The desired tone of the report ("positive", "negative", or "balanced")
        
    Returns:
        A detailed report as a string
    """
    try:
        # Get an example profile for reference
        example = get_example_profile(tone)
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": f"""
                    You are an expert in psychological profiling and intelligence analysis.
                    Create a detailed, professional report based on the provided psychological profile.
                    The report should be written in a style similar to CIA intelligence reports,
                    with clear sections, professional language, and detailed analysis.
                    
                    Here is an example of the kind of report we're looking for:
                    
                    {example}
                    
                    Use this example as a reference for the level of detail, structure, and tone we want.
                    """
                },
                {"role": "user", "content": f"Profile: {profile.model_dump_json(indent=2)}\n\nGenerate a detailed report."},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating detailed report: {str(e)}")
        return None

def generate_intelligence_report(text: str, tone: str = "balanced") -> str:
    """
    Generate a complete intelligence report from text.
    
    Args:
        text: The text to analyze
        tone: The desired tone of the report ("positive", "negative", or "balanced")
        
    Returns:
        A detailed intelligence report as a string
    """
    try:
        # Get the appropriate template based on the desired tone
        template = get_profile_template(tone)
        
        # Get an example profile for reference
        example = get_example_profile(tone)
        
        # Identify the type of text to provide more specific instructions
        text_type_prompt = """
        First, identify the type of text you're analyzing:
        - Direct statements: Personal thoughts, feelings, or experiences
        - Random excerpts: Fragments of text without clear context
        - ChatGPT conversations: Interactions with AI, including prompts and responses
        - Essays: Structured written content with a clear purpose
        - Text messages: Informal communication, possibly fragmented
        - Other: Identify the type if it doesn't fit the above categories
        
        Then, adapt your analysis approach based on the text type:
        - For direct statements: Focus on emotional content, personal values, and self-perception
        - For random excerpts: Look for patterns and themes that might reveal underlying psychology
        - For ChatGPT conversations: Analyze both the user's prompts and how they respond to AI
        - For essays: Examine argument structure, evidence selection, and conclusion formation
        - For text messages: Consider informal language patterns, emoji usage, and communication style
        """
        
        # Advanced analysis directives
        advanced_directives = """
        **Neurolinguistic Focus:**
        1. Calculate pronoun ratios (I/we/they) and map to self-concept
        2. Analyze verb tense distribution for temporal orientation
        3. Quantify hedge words (might/could) vs definitive language
        4. Measure lexical density and syntactic complexity
        5. Identify semantic primes in emotional expression

        **Psychological Deep Dive:**
        1. Apply Dark Triad detection framework
        2. Map language to Hermann Brain Dominance model
        3. Analyze conceptual metaphors (Lakoffian frames)
        4. Detect cognitive dissonance patterns
        5. Identify narrative schema violations

        **Behavioral Forecasting:**
        1. Predict 3 most likely actions under stress
        2. Identify optimal persuasion strategies
        3. Determine vulnerability to recruitment
        4. Assess deception probability patterns
        5. Model information sensitivity thresholds
        """
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": f"""
                    {template}
                    
                    {text_type_prompt}
                    
                    {advanced_directives}
                    
                    Here is an example of the kind of analysis we're looking for:
                    
                    {example}
                    
                    Use this example as a reference for the level of detail, structure, and tone we want.
                    """
                },
                {"role": "user", "content": f"Analyze this text and generate a complete intelligence report: {text}"},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating intelligence report: {str(e)}")
        return None

def calculate_metrics(text: str) -> ProfileMetrics:
    """
    Calculate quantitative behavioral metrics from text.
    
    Args:
        text: The text to analyze
        
    Returns:
        Quantitative assessment metrics
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    You are an expert in psychological profiling and behavioral analysis.
                    Calculate quantitative behavioral metrics from the provided text.
                    Your response must be a valid JSON object with the following structure:
                    {
                      "persuasion_susceptibility": number between 0 and 1,
                      "deception_capacity": number between 0 and 1,
                      "information_hoarding": number between 0 and 1,
                      "risk_tolerance": number between 0 and 1,
                      "group_affiliation": number between 0 and 1,
                      "cognitive_rigidity": number between 0 and 1
                    }
                    
                    Use linguistic features and psychological patterns to calculate these metrics.
                    """
                },
                {"role": "user", "content": f"Text: {text}\n\nCalculate behavioral metrics and return as JSON."},
            ],
            response_format={"type": "json_object"},
        )
        
        # Parse the JSON response into a ProfileMetrics object
        metrics_data = json.loads(completion.choices[0].message.content)
        return ProfileMetrics(**metrics_data)
    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        return None

def generate_security_profile(text: str) -> SecurityProfile:
    """
    Analyze text for operational security risks.
    
    Args:
        text: The text to analyze
        
    Returns:
        A security-oriented risk assessment
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    You are an expert in operational security and risk assessment.
                    Analyze the provided text for operational security risks.
                    Your response must be a valid JSON object with the following structure:
                    {
                      "opsec_weaknesses": ["string"],
                      "detectable_patterns": ["string"],
                      "predictable_behaviors": ["string"],
                      "suggested_countermeasures": ["string"]
                    }
                    
                    Focus on patterns that could compromise security, such as:
                    - Predictable communication patterns
                    - Consistent metadata leakage
                    - Behavioral tells in stress scenarios
                    """
                },
                {"role": "user", "content": f"Text: {text}\n\nAnalyze for operational security risks and return as JSON."},
            ],
            response_format={"type": "json_object"},
        )
        
        # Parse the JSON response into a SecurityProfile object
        security_data = json.loads(completion.choices[0].message.content)
        return SecurityProfile(**security_data)
    except Exception as e:
        print(f"Error generating security profile: {str(e)}")
        return None

def main():
    """Run the CIA Profile Generator."""
    print("=== CIA Profile Generator ===")
    print("This tool analyzes text to generate CIA-level psychological profiles.")
    print("\nYou can analyze various types of text:")
    print("- Direct statements: Personal thoughts, feelings, or experiences")
    print("- Random excerpts: Fragments of text without clear context")
    print("- ChatGPT conversations: Interactions with AI, including prompts and responses")
    print("- Essays: Structured written content with a clear purpose")
    print("- Text messages: Informal communication, possibly fragmented")
    print("- Any other text that might reveal psychological insights")
    
    print("\nEnter text to analyze (type 'exit' to quit):")
    
    # Ask for the desired tone
    print("\nSelect profile tone:")
    print("1. Positive (emphasizes strengths and potential)")
    print("2. Negative (emphasizes risks and limitations)")
    print("3. Balanced (default)")
    
    tone_choice = input("Enter choice (1-3): ").strip()
    tone = "balanced"
    if tone_choice == "1":
        tone = "positive"
    elif tone_choice == "2":
        tone = "negative"
    
    while True:
        text = input("\nText: ")
        if text.lower() == 'exit':
            break
        
        if not text.strip():
            print("Please enter some text to analyze.")
            continue
        
        print("\nAnalyzing text... This may take a moment.")
        
        # Ask if the user wants a structured profile or a direct intelligence report
        report_type = input("Generate:\n1. Structured profile and detailed report\n2. Direct intelligence report\nEnter choice (1-2): ").strip()
        
        if report_type == "1":
            # Generate the structured profile
            profile = generate_structured_profile(text, tone)
            if not profile:
                print("Failed to generate profile. Please try again.")
                continue
            
            # Generate a detailed report
            report = generate_detailed_report(profile, tone)
            if not report:
                print("Failed to generate report. Please try again.")
                continue
            
            # Print the report
            print("\n=== PSYCHOLOGICAL PROFILE REPORT ===")
            print(report)
        else:
            # Generate a direct intelligence report
            report = generate_intelligence_report(text, tone)
            if not report:
                print("Failed to generate report. Please try again.")
                continue
            
            # Print the report
            print("\n=== INTELLIGENCE REPORT ===")
            print(report)
        
        # Ask if the user wants to save the report
        save = input("\nSave this report to a file? (y/n): ")
        if save.lower() == 'y':
            filename = input("Enter filename (default: profile_report.txt): ")
            if not filename:
                filename = "profile_report.txt"
            
            with open(filename, 'w') as f:
                f.write(report)
            
            print(f"Report saved to {filename}")
    
    print("\nThank you for using the CIA Profile Generator.")

if __name__ == "__main__":
    main() 
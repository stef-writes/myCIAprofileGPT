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
from src.templates.profile_templates import get_profile_template, get_example_profile

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

class CommunicationStyle(BaseModel):
    """Analysis of communication patterns and preferences."""
    primary_style: str  # e.g., "direct", "diplomatic", "analytical", "empathetic"
    secondary_style: str
    communication_strengths: List[str]
    communication_challenges: List[str]
    preferred_channels: List[str]  # e.g., "written", "verbal", "visual"
    adaptation_capacity: float = Field(..., ge=0.0, le=1.0)  # Ability to adjust communication style
    evidence: List[str]

class DecisionMakingPattern(BaseModel):
    """Analysis of decision-making approach and effectiveness."""
    primary_approach: str  # e.g., "analytical", "intuitive", "collaborative", "decisive"
    decision_speed: float = Field(..., ge=0.0, le=1.0)  # 0 = very slow, 1 = very fast
    risk_tolerance: float = Field(..., ge=0.0, le=1.0)
    information_gathering_style: str  # e.g., "comprehensive", "focused", "minimal"
    decision_quality_indicators: List[str]
    common_biases: List[str]
    evidence: List[str]

class StressResponse(BaseModel):
    """Analysis of stress handling and coping mechanisms."""
    primary_coping_mechanism: str
    stress_threshold: float = Field(..., ge=0.0, le=1.0)  # 0 = low threshold, 1 = high threshold
    recovery_speed: float = Field(..., ge=0.0, le=1.0)  # 0 = slow recovery, 1 = fast recovery
    stress_indicators: List[str]
    coping_strategies: List[str]
    potential_triggers: List[str]
    evidence: List[str]

class LeadershipPotential(BaseModel):
    """Assessment of leadership capabilities and style."""
    leadership_style: str  # e.g., "transformational", "servant", "autocratic", "democratic"
    influence_capacity: float = Field(..., ge=0.0, le=1.0)
    vision_development: float = Field(..., ge=0.0, le=1.0)
    team_building_ability: float = Field(..., ge=0.0, le=1.0)
    strategic_thinking: float = Field(..., ge=0.0, le=1.0)
    key_strengths: List[str]
    development_areas: List[str]
    evidence: List[str]

class TeamDynamics(BaseModel):
    """Analysis of team interaction and compatibility."""
    preferred_role: str  # e.g., "leader", "innovator", "mediator", "executor"
    collaboration_style: str
    conflict_handling: str
    team_contribution: List[str]
    potential_challenges: List[str]
    ideal_team_composition: List[str]
    evidence: List[str]

class CulturalContext(BaseModel):
    """Analysis of cultural influences and context."""
    cultural_lexicons: List[str] = Field(default_factory=list)
    regional_references: List[str] = Field(default_factory=list)
    socioeconomic_indicators: List[str] = Field(default_factory=list)
    cultural_values: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0.0, le=1.0)

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
    cultural_context: Optional[CulturalContext] = None
    profile_metrics: Optional[ProfileMetrics] = None
    security_profile: Optional[SecurityProfile] = None
    # New fields
    communication_style: Optional[CommunicationStyle] = None
    decision_making: Optional[DecisionMakingPattern] = None
    stress_response: Optional[StressResponse] = None
    leadership_potential: Optional[LeadershipPotential] = None
    team_dynamics: Optional[TeamDynamics] = None

# ===== PROMPT GENERATION =====

def generate_profile_prompt(text: str, analysis_type: str = "general") -> str:
    """Generate a specialized prompt for psychological profiling."""
    base_prompt = f"""You are an expert CIA psychological profiler with extensive experience in behavioral analysis, neuro-linguistic programming, and counterintelligence operations.
Your task is to conduct a comprehensive neuro-linguistic psycho-analysis of the following text to generate a detailed psychological profile.
Focus on both explicit statements and implicit patterns that reveal psychological traits, behavioral tendencies, and potential vulnerabilities.

Text to analyze:
{text}

Conduct a CIA-level psychological assessment that includes:

1. Personality Traits:
   - Core personality characteristics and behavioral patterns
   - Value systems and motivational drivers
   - Potential psychological vulnerabilities
   - Behavioral consistency indicators

2. Emotional States:
   - Primary emotional patterns and regulation capacity
   - Emotional expression style and suppression indicators
   - Emotional intelligence and manipulation potential
   - Emotional stability under pressure

3. Cognitive Patterns:
   - Thinking style and information processing
   - Problem-solving approach and adaptability
   - Decision-making patterns and risk assessment
   - Cognitive biases and blind spots
   - Mental model construction and worldview

4. Writing Style:
   - Formality level and social positioning
   - Technical precision and attention to detail
   - Emotional content and self-disclosure patterns
   - Structural organization and planning capacity
   - Language complexity and vocabulary selection

5. Communication Style:
   - Primary and secondary communication styles
   - Communication strengths and potential manipulation tactics
   - Preferred communication channels and information sharing
   - Adaptation capacity and social flexibility
   - Evidence from text with specific examples

6. Decision-Making Patterns:
   - Primary decision-making approach and methodology
   - Decision speed, quality, and consistency
   - Risk tolerance and uncertainty handling
   - Information gathering style and confirmation bias
   - Common decision-making biases and heuristics

7. Stress Response:
   - Primary coping mechanisms and resilience indicators
   - Stress threshold and breaking point indicators
   - Recovery patterns and adaptation strategies
   - Stress indicators and behavioral changes under pressure
   - Potential triggers and psychological vulnerabilities

8. Leadership Potential:
   - Leadership style and influence methodology
   - Influence capacity and persuasion techniques
   - Vision development and strategic thinking
   - Team building ability and group dynamics
   - Strategic thinking and long-term planning

9. Team Dynamics:
   - Preferred team role and social positioning
   - Collaboration style and group contribution
   - Conflict handling and resolution approach
   - Team contribution and value proposition
   - Ideal team composition and compatibility

10. Security Profile:
    - OPSEC awareness and information security practices
    - Information handling and disclosure patterns
    - Risk management and threat assessment
    - Counterintelligence indicators and vulnerabilities
    - Deception detection and truthfulness assessment

For each aspect, provide:
- Specific evidence from the text with direct quotes
- Confidence level in the assessment (0.0-1.0)
- Potential alternative interpretations
- Limitations of the analysis
- Counterintelligence implications

Format the output as a structured JSON object matching the PsychologicalProfile schema.
Ensure all assessments are evidence-based and avoid speculative conclusions.
Apply neuro-linguistic programming principles to identify embedded commands, presuppositions, and linguistic patterns that reveal deeper psychological structures."""

    # Add type-specific directives
    if analysis_type == "technical":
        base_prompt += """
Additional focus areas for technical analysis:
- Technical communication patterns and knowledge gaps
- Problem-solving methodology and approach
- Code/documentation style and attention to detail
- Technical decision-making and risk assessment
- Collaboration in technical contexts and knowledge sharing
- Information security practices and vulnerabilities"""
    elif analysis_type == "social":
        base_prompt += """
Additional focus areas for social analysis:
- Social interaction patterns and relationship dynamics
- Group behavior and conformity indicators
- Social influence and persuasion techniques
- Communication in social contexts and impression management
- Social positioning and status indicators
- Relationship building and maintenance strategies"""

    return base_prompt

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
                      "cultural_context": {
                        "cultural_lexicons": ["string"],
                        "regional_references": ["string"],
                        "socioeconomic_indicators": ["string"],
                        "cultural_values": ["string"],
                        "evidence": ["string"],
                        "confidence_score": number between 0 and 1
                      },
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
                    
                    The report should include all the following sections:
                    
                    1. Executive Summary
                    2. Core Personality Analysis
                       - Personality Traits
                       - Emotional Profile
                       - Cognitive Patterns
                    3. Communication & Decision Making
                       - Communication Style
                       - Decision Making Patterns
                    4. Stress & Leadership
                       - Stress Response Profile
                       - Leadership Assessment
                    5. Team Dynamics
                       - Team Compatibility
                    6. Writing & Communication Analysis
                       - Writing Style
                       - Linguistic Markers
                    7. Security Profile
                    8. Confidence Assessment
                       - Overall Confidence Score
                       - Potential Biases
                       - Analysis Limitations
                    9. Evidence Base
                    
                    For each section, provide specific evidence from the text with direct quotes where possible.
                    Include confidence levels for assessments and highlight any counterintelligence implications.
                    
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
        
        **Communication Analysis:**
        1. Identify primary and secondary communication styles
        2. Assess communication strengths and potential manipulation tactics
        3. Evaluate adaptation capacity and social flexibility
        4. Analyze information sharing patterns and disclosure tendencies
        
        **Decision-Making Assessment:**
        1. Evaluate decision-making approach and methodology
        2. Assess risk tolerance and uncertainty handling
        3. Identify information gathering style and confirmation bias
        4. Analyze decision speed, quality, and consistency
        
        **Stress Response Profiling:**
        1. Identify primary coping mechanisms and resilience indicators
        2. Assess stress threshold and breaking point indicators
        3. Evaluate recovery patterns and adaptation strategies
        4. Analyze stress indicators and behavioral changes under pressure
        
        **Leadership Potential:**
        1. Evaluate leadership style and influence methodology
        2. Assess influence capacity and persuasion techniques
        3. Analyze vision development and strategic thinking
        4. Evaluate team building ability and group dynamics
        
        **Team Dynamics:**
        1. Identify preferred team role and social positioning
        2. Assess collaboration style and group contribution
        3. Evaluate conflict handling and resolution approach
        4. Analyze team contribution and value proposition
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
                    
                    Create a comprehensive intelligence report that includes:
                    
                    1. Executive Summary
                    2. Key Behavioral Patterns
                    3. Communication Analysis
                    4. Decision-Making Assessment
                    5. Stress Response Profile
                    6. Leadership Assessment
                    7. Team Dynamics
                    8. Security Implications
                    9. Confidence Assessment
                    10. Evidence Base
                    
                    For each section, provide specific evidence from the text with direct quotes where possible.
                    Include confidence levels for assessments and highlight any counterintelligence implications.
                    
                    Here is an example of the kind of report we're looking for:
                    
                    {example}
                    
                    Use this example as a reference for the level of detail, structure, and tone we want.
                    """
                },
                {"role": "user", "content": f"Text to analyze: {text[:1000]}...\n\nGenerate a comprehensive intelligence report."},
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

class CIAProfile:
    """A class to manage CIA profiles."""
    
    def __init__(self, name: str):
        """Initialize a CIA profile with a name."""
        if not name:
            raise ValueError("Profile name cannot be empty")
        self.name = name
        self.content = None
        self.profile = None
    
    def update_content(self, content: str) -> None:
        """Update the profile content."""
        self.content = content
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the profile to a dictionary."""
        return {
            "name": self.name,
            "content": self.content,
            "profile": self.profile.dict() if self.profile else None
        }
    
    def generate_profile(self, tone: str = "balanced") -> None:
        """Generate a profile from the content."""
        if not self.content:
            raise ValueError("No content to generate profile from")
        self.profile = generate_structured_profile(self.content, tone)
    
    def get_report(self, tone: str = "balanced") -> str:
        """Get a detailed report from the profile."""
        if not self.profile:
            raise ValueError("No profile to generate report from")
        return generate_detailed_report(self.profile, tone)
    
    def get_intelligence_report(self, tone: str = "balanced") -> str:
        """Get an intelligence report from the profile."""
        if not self.content:
            raise ValueError("No content to generate intelligence report from")
        return generate_intelligence_report(self.content, tone)
    
    def get_security_profile(self) -> SecurityProfile:
        """Get a security profile from the content."""
        if not self.content:
            raise ValueError("No content to generate security profile from")
        return generate_security_profile(self.content)
    
    def get_metrics(self) -> ProfileMetrics:
        """Get metrics from the content."""
        if not self.content:
            raise ValueError("No content to calculate metrics from")
        return calculate_metrics(self.content)

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
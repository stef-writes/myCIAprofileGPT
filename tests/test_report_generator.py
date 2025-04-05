import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from src.utils.report_generator import (
    load_comprehensive_profile,
    format_trait,
    format_emotion,
    format_pattern,
    format_marker,
    format_prediction,
    format_countermeasure,
    generate_profile_report,
    save_report
)

# Sample data for testing
SAMPLE_PROFILE = {
    "core_profile": {
        "personality_traits": [
            {
                "trait": "Analytical",
                "confidence": 0.85,
                "evidence": "Uses logical arguments"
            }
        ],
        "emotional_states": [
            {
                "emotion": "Frustration",
                "intensity": 0.7,
                "evidence": "Expresses dissatisfaction"
            }
        ],
        "cognitive_patterns": [
            {
                "pattern": "Systematic thinking",
                "significance": 0.85,
                "evidence": "Organizes information logically"
            }
        ],
        "linguistic_markers": [
            {
                "marker": "Frequent use of technical terms",
                "evidence": "Uses industry-specific terminology",
                "interpretation": "Indicates technical expertise"
            }
        ],
        "writing_style": {
            "formality": "High",
            "complexity": "Medium",
            "emotionality": "Low",
            "evidence": "Uses formal language"
        },
        "neurolinguistic_features": {
            "syntactic_complexity": 0.75,
            "pronoun_ratio": {
                "I": 0.3,
                "we": 0.2,
                "you": 0.3,
                "they": 0.2
            },
            "temporal_orientation": {
                "past": 0.2,
                "present": 0.5,
                "future": 0.3
            },
            "hedge_density": 0.4,
            "certainty_score": 0.6,
            "evidence": ["Uses a mix of pronouns", "Balanced temporal orientation"]
        },
        "dark_triad_profile": {
            "narcissism": 0.3,
            "machiavellianism": 0.4,
            "psychopathy": 0.2,
            "behavioral_manifestations": ["Strategic thinking", "Goal-oriented behavior"],
            "operational_risks": ["May prioritize personal goals", "Could be manipulative"]
        },
        "behavioral_predictions": [
            {
                "scenario": "High-stress deadline",
                "predicted_behavior": "Focus on efficiency",
                "confidence": 0.8,
                "triggering_conditions": ["Time pressure"],
                "mitigation_strategies": ["Clear prioritization"]
            }
        ],
        "cognitive_biases": ["Confirmation bias", "Overconfidence"],
        "cultural_lexicons": ["Technical jargon", "Industry-specific terms"]
    },
    "metrics": {
        "persuasion_susceptibility": 0.5,
        "deception_capacity": 0.3,
        "information_hoarding": 0.4,
        "risk_tolerance": 0.6,
        "group_affiliation": 0.7,
        "cognitive_rigidity": 0.4
    },
    "security_analysis": {
        "opsec_weaknesses": ["Weakness 1", "Weakness 2"],
        "detectable_patterns": ["Pattern 1", "Pattern 2"],
        "predictable_behaviors": ["Behavior 1", "Behavior 2"],
        "suggested_countermeasures": ["Countermeasure 1", "Countermeasure 2"]
    },
    "integrated_report": """## Executive Summary
Test summary

## Core Assessment
Test assessment

## Motivation Layer
Test motivation

## Psychological & Behavioral Risk Profile
Test risk profile

## Strategic Liabilities
Test liabilities

## Unique Operational Hazards
Test hazards

## Strengths Worth Leveraging
Test strengths

## Structural Recommendations
Test recommendations

## Intelligence Summary
Test intelligence summary

## Final Verdict
Test final verdict"""
}

def test_load_comprehensive_profile():
    """Test loading a comprehensive profile from a JSON file."""
    mock_json = json.dumps(SAMPLE_PROFILE)
    with patch("builtins.open", mock_open(read_data=mock_json)):
        profile = load_comprehensive_profile()
        assert profile == SAMPLE_PROFILE

def test_format_trait():
    """Test formatting a personality trait."""
    trait = {
        "trait": "Analytical",
        "confidence": 0.85,
        "evidence": "Uses logical arguments"
    }
    formatted = format_trait(trait)
    assert "**Analytical**" in formatted
    assert "0.85" in formatted
    assert "Uses logical arguments" in formatted

def test_format_emotion():
    """Test formatting an emotional state."""
    emotion = {
        "emotion": "Frustration",
        "intensity": 0.7,
        "evidence": "Expresses dissatisfaction"
    }
    formatted = format_emotion(emotion)
    assert "**Frustration**" in formatted
    assert "0.7" in formatted
    assert "Expresses dissatisfaction" in formatted

def test_format_pattern():
    """Test formatting a cognitive pattern."""
    pattern = {
        "pattern": "Systematic thinking",
        "significance": 0.85,
        "evidence": "Organizes information logically"
    }
    formatted = format_pattern(pattern)
    assert "**Systematic thinking**" in formatted
    assert "0.85" in formatted
    assert "Organizes information logically" in formatted

def test_format_marker():
    """Test formatting a linguistic marker."""
    marker = {
        "marker": "Technical terms",
        "evidence": "Uses industry jargon",
        "interpretation": "Shows expertise"
    }
    formatted = format_marker(marker)
    assert "**Technical terms**" in formatted
    assert "Uses industry jargon" in formatted
    assert "Shows expertise" in formatted

def test_format_prediction():
    """Test formatting a behavioral prediction."""
    prediction = {
        "scenario": "High-stress deadline",
        "predicted_behavior": "Focus on efficiency",
        "confidence": 0.8,
        "triggering_conditions": ["Time pressure"],
        "mitigation_strategies": ["Clear prioritization"]
    }
    formatted = format_prediction(prediction)
    assert "High-stress deadline" in formatted
    assert "Focus on efficiency" in formatted
    assert "0.8" in formatted
    assert "Time pressure" in formatted
    assert "Clear prioritization" in formatted

def test_format_countermeasure():
    """Test formatting a countermeasure."""
    countermeasure = "Implement two-factor authentication"
    formatted = format_countermeasure(countermeasure)
    assert formatted == "- Implement two-factor authentication"

@patch("builtins.open", new_callable=mock_open)
def test_generate_profile_report(mock_file):
    """Test generating a profile report."""
    # Call the function
    output_file = generate_profile_report(SAMPLE_PROFILE)
    
    # Verify the output filename
    assert output_file == "profile_report.md"
    
    # Get the content that was written to the file
    report_content = mock_file.return_value.write.call_args[0][0]
    
    # Verify the report content
    assert "PSYCHOLOGICAL PROFILE REPORT" in report_content
    assert "EXECUTIVE SUMMARY" in report_content
    assert "CORE ASSESSMENT" in report_content
    assert "PERSONALITY PROFILE" in report_content
    assert "NEUROLINGUISTIC ANALYSIS" in report_content
    assert "PSYCHOLOGICAL ANALYSIS" in report_content
    assert "BEHAVIORAL PREDICTIONS" in report_content
    assert "BEHAVIORAL METRICS" in report_content
    assert "SECURITY PROFILE" in report_content
    
    # Verify the file was opened with the correct filename
    mock_file.assert_called_once_with("profile_report.md", 'w')

def test_save_report():
    """Test saving a report to a file."""
    report_text = "Test report content"
    with patch("builtins.open", mock_open()) as mock_file:
        save_report(report_text, "test_report.md")
        mock_file.assert_called_once()
        handle = mock_file()
        handle.write.assert_called_once_with(report_text) 
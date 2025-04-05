import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from src.examples.example_profile import (
    generate_comprehensive_profile,
    save_comprehensive_profile,
    main
)

# Sample text for testing
SAMPLE_TEXTS = [
    "This is a test text sample with some analytical content.",
    "I feel frustrated when things don't work as expected.",
    "The system needs to be more efficient and reliable."
]

# Mock profile data
MOCK_PROFILE = {
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
        ]
    },
    "neurolinguistic_analysis": [
        {
            "feature": "Formal language",
            "score": 0.8,
            "evidence": "Uses professional terminology"
        }
    ],
    "psychological_analysis": [
        {
            "aspect": "Problem-solving",
            "score": 0.9,
            "evidence": "Proposes solutions"
        }
    ],
    "behavioral_analysis": [
        {
            "pattern": "Systematic thinking",
            "confidence": 0.85,
            "evidence": "Organizes information logically"
        }
    ],
    "security_analysis": {
        "risk_level": "Medium",
        "vulnerabilities": ["Predictable patterns"],
        "recommendations": ["Implement randomization"]
    },
    "metrics": {
        "persuasion_susceptibility": 0.4,
        "deception_capacity": 0.3,
        "information_hoarding": 0.5
    },
    "integrated_report": "This is a test integrated report."
}

@patch("src.examples.example_profile.generate_structured_profile")
@patch("src.examples.example_profile.generate_detailed_report")
@patch("src.examples.example_profile.generate_intelligence_report")
@patch("src.examples.example_profile.calculate_metrics")
@patch("src.examples.example_profile.generate_security_profile")
def test_generate_comprehensive_profile(
    mock_security_profile,
    mock_metrics,
    mock_intelligence,
    mock_detailed,
    mock_structured
):
    """Test generating a comprehensive profile."""
    # Create a mock profile object with the required attributes
    mock_profile = MagicMock()
    
    # Set up the core profile attributes with proper structure
    mock_profile.personality_traits = [
        MagicMock(
            trait="Analytical",
            confidence=0.85,
            evidence="Uses logical arguments"
        )
    ]
    mock_profile.emotional_states = [
        MagicMock(
            emotion="Frustration",
            intensity=0.7,
            evidence="Expresses dissatisfaction"
        )
    ]
    mock_profile.cognitive_patterns = [
        MagicMock(
            pattern="Systematic thinking",
            significance=0.85,
            evidence="Organizes information logically"
        )
    ]
    mock_profile.neurolinguistic_features = {
        "syntactic_complexity": 0.75,
        "pronoun_ratio": {"I": 0.3, "we": 0.2, "you": 0.3, "they": 0.2},
        "temporal_orientation": {"past": 0.2, "present": 0.5, "future": 0.3},
        "hedge_density": 0.4,
        "certainty_score": 0.6,
        "evidence": ["Uses a mix of pronouns", "Balanced temporal orientation"]
    }
    mock_profile.dark_triad_profile = {
        "narcissism": 0.3,
        "machiavellianism": 0.4,
        "psychopathy": 0.2,
        "behavioral_manifestations": ["Strategic thinking", "Goal-oriented behavior"],
        "operational_risks": ["May prioritize personal goals", "Could be manipulative"]
    }
    mock_profile.behavioral_predictions = [
        MagicMock(
            scenario="High-stress deadline",
            predicted_behavior="Focus on efficiency over quality",
            confidence=0.8,
            triggering_conditions=["Time pressure", "Multiple competing priorities"],
            mitigation_strategies=["Clear prioritization", "Regular check-ins"]
        )
    ]
    
    # Set up mock returns
    mock_structured.return_value = mock_profile
    mock_detailed.return_value = "Detailed report content"
    mock_intelligence.return_value = "Intelligence report content"
    mock_metrics.return_value = MOCK_PROFILE["metrics"]
    mock_security_profile.return_value = MOCK_PROFILE["security_analysis"]
    
    # Generate profile
    profile = generate_comprehensive_profile(SAMPLE_TEXTS, "balanced")
    
    # Verify the profile structure
    assert profile["core_profile"] == mock_profile
    assert profile["metrics"] == MOCK_PROFILE["metrics"]
    assert profile["security_analysis"] == MOCK_PROFILE["security_analysis"]
    assert "integrated_report" in profile
    assert profile["integrated_report"] == "Intelligence report content"
    
    # Verify mocks were called
    mock_structured.assert_called()
    mock_intelligence.assert_called()
    mock_metrics.assert_called()
    mock_security_profile.assert_called()

@patch("src.examples.example_profile.get_output_path")
def test_save_comprehensive_profile(mock_get_output_path):
    """Test saving a comprehensive profile to a file."""
    # Mock the output path
    mock_get_output_path.return_value = Path("/test/output/comprehensive_profile.json")
    
    # Mock file operations
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        with patch("json.dump") as mock_json_dump:
            save_comprehensive_profile(MOCK_PROFILE)
            
            # Verify file was opened correctly
            mock_file.assert_called_once_with(Path("/test/output/comprehensive_profile.json"), 'w')
            
            # Verify JSON dump was called with the profile
            mock_json_dump.assert_called_once_with(MOCK_PROFILE, mock_file.return_value, indent=2)

@patch("src.examples.example_profile.generate_comprehensive_profile")
@patch("src.examples.example_profile.save_comprehensive_profile")
def test_main(mock_save, mock_generate):
    """Test the main function."""
    # Create a mock profile object with the required attributes
    mock_profile = MagicMock()
    
    # Set up the core profile attributes with proper structure
    mock_profile.personality_traits = [
        MagicMock(
            trait="Analytical",
            confidence=0.85,
            evidence="Uses logical arguments"
        )
    ]
    mock_profile.emotional_states = [
        MagicMock(
            emotion="Frustration",
            intensity=0.7,
            evidence="Expresses dissatisfaction"
        )
    ]
    mock_profile.cognitive_patterns = [
        MagicMock(
            pattern="Systematic thinking",
            significance=0.85,
            evidence="Organizes information logically"
        )
    ]
    
    # Set up mocks with the correct structure
    mock_generate.return_value = {
        "core_profile": mock_profile,
        "neurolinguistic_analysis": [{"text_sample": 1, "features": {}}],
        "psychological_analysis": [{"text_sample": 1, "dark_triad": {}}],
        "behavioral_analysis": [{"text_sample": 1, "predictions": []}],
        "metrics": MagicMock(
            persuasion_susceptibility=0.5,
            deception_capacity=0.3,
            risk_tolerance=0.4
        ),
        "security_analysis": MagicMock(
            opsec_weaknesses=["weakness1"],
            detectable_patterns=["pattern1"],
            suggested_countermeasures=["countermeasure1"]
        ),
        "integrated_report": "Test report"
    }
    
    # Call main
    main()
    
    # Verify mocks were called
    mock_generate.assert_called_once()
    mock_save.assert_called_once() 
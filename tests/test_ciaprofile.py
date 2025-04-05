import pytest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError
from src.ciabot.core.ciaprofile import (
    PersonalityTrait, EmotionalState, CognitivePattern, WritingStyle,
    LinguisticMarker, NeurolinguisticFeature, DarkTriadProfile,
    BehavioralPrediction, ProfileMetrics, SecurityProfile, PsychologicalProfile,
    generate_profile_prompt, analyze_text_with_reasoning,
    generate_structured_profile, generate_detailed_report,
    generate_intelligence_report, calculate_metrics,
    generate_security_profile, CIAProfile
)

# Test data
SAMPLE_TEXT = "This is a sample text for testing psychological profiling."
SAMPLE_PROMPT = "Analyze this text for psychological patterns."

# Model validation tests
def test_personality_trait_validation():
    """Test PersonalityTrait model validation."""
    # Valid trait
    trait = PersonalityTrait(
        trait="analytical",
        evidence="Uses precise language",
        confidence=0.8
    )
    assert trait.trait == "analytical"
    assert trait.confidence == 0.8

    # Invalid confidence
    with pytest.raises(ValidationError):
        PersonalityTrait(
            trait="analytical",
            evidence="Uses precise language",
            confidence=1.5  # Should be <= 1.0
        )

def test_emotional_state_validation():
    """Test EmotionalState model validation."""
    # Valid state
    state = EmotionalState(
        emotion="calm",
        evidence="Even tone in writing",
        intensity=0.6
    )
    assert state.emotion == "calm"
    assert state.intensity == 0.6

    # Invalid intensity
    with pytest.raises(ValidationError):
        EmotionalState(
            emotion="calm",
            evidence="Even tone in writing",
            intensity=-0.1  # Should be >= 0.0
        )

def test_writing_style_validation():
    """Test WritingStyle model validation."""
    # Valid style
    style = WritingStyle(
        formality=0.7,
        complexity=0.5,
        emotionality=0.3,
        evidence="Uses formal language with moderate complexity"
    )
    assert style.formality == 0.7
    assert style.complexity == 0.5

    # Invalid values
    with pytest.raises(ValidationError):
        WritingStyle(
            formality=1.2,  # Should be <= 1.0
            complexity=0.5,
            emotionality=0.3,
            evidence="Test"
        )

def test_psychological_profile_validation():
    """Test PsychologicalProfile model validation."""
    # Create valid profile
    profile = PsychologicalProfile(
        personality_traits=[
            PersonalityTrait(trait="analytical", evidence="Test", confidence=0.8)
        ],
        emotional_states=[
            EmotionalState(emotion="calm", evidence="Test", intensity=0.6)
        ],
        cognitive_patterns=[
            CognitivePattern(pattern="logical", evidence="Test", significance=0.7)
        ],
        writing_style=WritingStyle(
            formality=0.7,
            complexity=0.5,
            emotionality=0.3,
            evidence="Test"
        ),
        linguistic_markers=[
            LinguisticMarker(marker="formal", evidence="Test", interpretation="Test")
        ],
        overall_assessment="Test assessment",
        confidence_score=0.8,
        potential_biases=["Test bias"],
        limitations=["Test limitation"]
    )
    assert profile.confidence_score == 0.8
    assert len(profile.personality_traits) == 1

    # Test optional fields
    profile.neurolinguistic_features = NeurolinguisticFeature(
        syntactic_complexity=0.7,
        pronoun_ratio={"I": 0.3, "we": 0.2, "you": 0.3, "they": 0.2},
        temporal_orientation={"past": 0.3, "present": 0.4, "future": 0.3},
        hedge_density=0.2,
        certainty_score=0.8,
        evidence=["Test evidence"]
    )
    assert profile.neurolinguistic_features is not None

# Function tests
@patch('src.ciabot.core.ciaprofile.client')
def test_generate_profile_prompt(mock_client):
    """Test profile prompt generation."""
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Generated prompt"))]
    )
    
    prompt = generate_profile_prompt(SAMPLE_TEXT, tone="balanced")
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    mock_client.chat.completions.create.assert_called_once()

@patch('src.ciabot.core.ciaprofile.client')
def test_analyze_text_with_reasoning(mock_client):
    """Test text analysis with reasoning."""
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Analysis result"))]
    )
    
    result = analyze_text_with_reasoning(SAMPLE_TEXT, SAMPLE_PROMPT)
    assert isinstance(result, str)
    assert len(result) > 0
    mock_client.chat.completions.create.assert_called_once()

@patch('src.ciabot.core.ciaprofile.generate_profile_prompt')
@patch('src.ciabot.core.ciaprofile.analyze_text_with_reasoning')
def test_generate_structured_profile(mock_analyze, mock_prompt):
    """Test structured profile generation."""
    mock_prompt.return_value = "Test prompt"
    mock_analyze.return_value = """
    {
        "personality_traits": [{"trait": "analytical", "evidence": "Test", "confidence": 0.8}],
        "emotional_states": [{"emotion": "calm", "evidence": "Test", "intensity": 0.6}],
        "cognitive_patterns": [{"pattern": "logical", "evidence": "Test", "significance": 0.7}],
        "writing_style": {"formality": 0.7, "complexity": 0.5, "emotionality": 0.3, "evidence": "Test"},
        "linguistic_markers": [{"marker": "formal", "evidence": "Test", "interpretation": "Test"}],
        "overall_assessment": "Test assessment",
        "confidence_score": 0.8,
        "potential_biases": ["Test bias"],
        "limitations": ["Test limitation"]
    }
    """
    
    profile = generate_structured_profile(SAMPLE_TEXT)
    assert isinstance(profile, PsychologicalProfile)
    assert profile.confidence_score == 0.8
    assert len(profile.personality_traits) == 1

# CIAProfile class tests
def test_ciaprofile_initialization():
    """Test CIAProfile initialization."""
    profile = CIAProfile("test_profile")
    assert profile.name == "test_profile"
    assert profile.content is None
    assert profile.profile is None

def test_ciaprofile_update_content():
    """Test content updates."""
    profile = CIAProfile("test_profile")
    profile.update_content(SAMPLE_TEXT)
    assert profile.content == SAMPLE_TEXT

@patch('src.ciabot.core.ciaprofile.generate_structured_profile')
def test_ciaprofile_generate_profile(mock_generate):
    """Test profile generation."""
    mock_generate.return_value = PsychologicalProfile(
        personality_traits=[
            PersonalityTrait(trait="analytical", evidence="Test", confidence=0.8)
        ],
        emotional_states=[
            EmotionalState(emotion="calm", evidence="Test", intensity=0.6)
        ],
        cognitive_patterns=[
            CognitivePattern(pattern="logical", evidence="Test", significance=0.7)
        ],
        writing_style=WritingStyle(
            formality=0.7,
            complexity=0.5,
            emotionality=0.3,
            evidence="Test"
        ),
        linguistic_markers=[
            LinguisticMarker(marker="formal", evidence="Test", interpretation="Test")
        ],
        overall_assessment="Test assessment",
        confidence_score=0.8,
        potential_biases=["Test bias"],
        limitations=["Test limitation"]
    )
    
    profile = CIAProfile("test_profile")
    profile.update_content(SAMPLE_TEXT)
    profile.generate_profile()
    assert profile.profile is not None
    assert isinstance(profile.profile, PsychologicalProfile)
    mock_generate.assert_called_once_with(SAMPLE_TEXT, "balanced")

def test_profile_initialization(mock_openai_client):
    """Test that CIAProfile can be initialized with basic parameters."""
    profile = CIAProfile(name="Test Profile")
    assert profile.name == "Test Profile"
    assert profile.content is None  # Content should be None initially
    assert profile.profile is None  # Profile should be None initially

def test_profile_content_update(mock_openai_client):
    """Test updating profile content."""
    profile = CIAProfile(name="Test Profile")
    test_content = "This is test content"
    profile.update_content(test_content)
    assert profile.content == test_content

def test_profile_validation():
    """Test profile validation rules."""
    with pytest.raises(ValueError):
        CIAProfile(name="")  # Empty name should raise ValueError

def test_profile_serialization(mock_openai_client):
    """Test that profile can be serialized to dict."""
    profile = CIAProfile(name="Test Profile")
    profile_dict = profile.to_dict()
    assert isinstance(profile_dict, dict)
    assert profile_dict["name"] == "Test Profile"
    assert profile_dict["content"] is None
    assert profile_dict["profile"] is None

@patch('src.ciabot.core.ciaprofile.generate_structured_profile')
def test_profile_generation(mock_generate, mock_openai_client):
    """Test profile generation."""
    mock_generate.return_value = PsychologicalProfile(
        personality_traits=[
            PersonalityTrait(trait="analytical", evidence="Test", confidence=0.8)
        ],
        emotional_states=[
            EmotionalState(emotion="calm", evidence="Test", intensity=0.6)
        ],
        cognitive_patterns=[
            CognitivePattern(pattern="logical", evidence="Test", significance=0.7)
        ],
        writing_style=WritingStyle(
            formality=0.7,
            complexity=0.5,
            emotionality=0.3,
            evidence="Test"
        ),
        linguistic_markers=[
            LinguisticMarker(marker="formal", evidence="Test", interpretation="Test")
        ],
        overall_assessment="Test assessment",
        confidence_score=0.8,
        potential_biases=["Test bias"],
        limitations=["Test limitation"]
    )
    
    profile = CIAProfile(name="Test Profile")
    profile.update_content("This is test content")
    profile.generate_profile()
    assert profile.profile is not None
    mock_generate.assert_called_once_with("This is test content", "balanced")

@patch('src.ciabot.core.ciaprofile.generate_detailed_report')
@patch('src.ciabot.core.ciaprofile.generate_intelligence_report')
@patch('src.ciabot.core.ciaprofile.generate_security_profile')
@patch('src.ciabot.core.ciaprofile.calculate_metrics')
def test_profile_reports(mock_metrics, mock_security, mock_intel, mock_report, mock_openai_client):
    """Test profile report generation."""
    # Set up mocks
    mock_report.return_value = "Detailed report"
    mock_intel.return_value = "Intelligence report"
    mock_security.return_value = SecurityProfile(
        opsec_weaknesses=["Test weakness"],
        detectable_patterns=["Test pattern"],
        predictable_behaviors=["Test behavior"],
        suggested_countermeasures=["Test countermeasure"]
    )
    mock_metrics.return_value = ProfileMetrics(
        persuasion_susceptibility=0.5,
        deception_capacity=0.5,
        information_hoarding=0.5,
        risk_tolerance=0.5,
        group_affiliation=0.5,
        cognitive_rigidity=0.5
    )
    
    profile = CIAProfile(name="Test Profile")
    profile.update_content("This is test content")
    profile.generate_profile()
    
    # Test detailed report
    report = profile.get_report()
    assert isinstance(report, str)
    assert len(report) > 0
    mock_report.assert_called_once()
    
    # Test intelligence report
    intel_report = profile.get_intelligence_report()
    assert isinstance(intel_report, str)
    assert len(intel_report) > 0
    mock_intel.assert_called_once_with("This is test content", "balanced")
    
    # Test security profile
    security_profile = profile.get_security_profile()
    assert isinstance(security_profile, SecurityProfile)
    mock_security.assert_called_once_with("This is test content")
    
    # Test metrics
    metrics = profile.get_metrics()
    assert isinstance(metrics, ProfileMetrics)
    mock_metrics.assert_called_once_with("This is test content")

def test_openai_integration(mock_openai_client):
    """Test OpenAI integration using the mocked client."""
    # Use the mocked client from the fixture
    client = mock_openai_client
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": "Write a one-sentence bedtime story about a unicorn."
            }
        ]
    )
    assert completion.choices[0].message.content is not None 
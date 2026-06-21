"""Tests for the ML model"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from player_name_prediction.model import NamePredictionModel


def test_model_initialization():
    """Test model initialization"""
    model = NamePredictionModel()
    assert not model.is_trained
    assert len(model.name_patterns) == 0


def test_model_training():
    """Test model training"""
    model = NamePredictionModel()
    training_data = [
        {"name": "LeBron", "position": "Forward", "team": "Lakers"},
        {"name": "Steph", "position": "Guard", "team": "Warriors"},
        {"name": "Kevin", "position": "Forward", "team": "Suns"},
    ]
    
    result = model.train(training_data)
    
    assert model.is_trained
    assert result["status"] == "trained"
    assert result["samples"] == 3


def test_model_prediction():
    """Test model prediction"""
    model = NamePredictionModel()
    training_data = [
        {"name": "LeBron", "position": "Forward", "team": "Lakers"},
        {"name": "Steph", "position": "Guard", "team": "Warriors"},
    ]
    
    model.train(training_data)
    
    prediction = model.predict({"position": "Guard", "team": "Warriors"})
    
    assert "top_predictions" in prediction
    assert "confidence" in prediction
    assert len(prediction["top_predictions"]) > 0


def test_model_evaluation():
    """Test model evaluation"""
    model = NamePredictionModel()
    data = [
        {"name": "LeBron", "position": "Forward", "team": "Lakers"},
        {"name": "Steph", "position": "Guard", "team": "Warriors"},
    ]
    
    model.train(data)
    evaluation = model.evaluate(data)
    
    assert "accuracy" in evaluation
    assert "correct_predictions" in evaluation
    assert "total_samples" in evaluation


if __name__ == "__main__":
    test_model_initialization()
    test_model_training()
    test_model_prediction()
    test_model_evaluation()
    print("All model tests passed!")

"""Tests for the agentic AI agent"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from player_name_prediction.agent import PlayerNamePredictionAgent, ActionType


def test_agent_initialization():
    """Test agent initialization"""
    agent = PlayerNamePredictionAgent()
    assert agent.model_name == "gpt-4"
    assert len(agent.memory) == 0
    assert len(agent.action_history) == 0


def test_agent_think():
    """Test agent thinking process"""
    agent = PlayerNamePredictionAgent()
    context = "Guard playing for Lakers with jersey 23"
    analysis = agent.think(context)
    
    assert "context" in analysis
    assert "keywords" in analysis
    assert "patterns" in analysis
    assert len(analysis["keywords"]) > 0


def test_agent_predict():
    """Test agent prediction"""
    agent = PlayerNamePredictionAgent()
    player_data = {
        "position": "Guard",
        "team": "Lakers",
        "jersey_number": 23
    }
    
    prediction = agent.predict(player_data)
    
    assert "predicted_name" in prediction
    assert "confidence" in prediction
    assert "reasoning" in prediction
    assert "alternatives" in prediction
    assert 0 <= prediction["confidence"] <= 1


def test_agent_state():
    """Test agent state inspection"""
    agent = PlayerNamePredictionAgent()
    state = agent.get_agent_state()
    
    assert state["model"] == "gpt-4"
    assert state["memory_size"] == 0
    assert state["actions_performed"] == 0


if __name__ == "__main__":
    test_agent_initialization()
    test_agent_think()
    test_agent_predict()
    test_agent_state()
    print("All agent tests passed!")

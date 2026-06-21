"""Tests for the data processor"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from player_name_prediction.data_processor import DataProcessor, PlayerData


def test_data_processor_initialization():
    """Test data processor initialization"""
    processor = DataProcessor()
    assert len(processor.get_all_players()) == 0


def test_add_and_get_player():
    """Test adding and retrieving player"""
    processor = DataProcessor()
    player = PlayerData("1", "LeBron James", "Forward", "6'9", 250, "Lakers", 23)
    processor.add_player(player)
    
    retrieved = processor.get_player("1")
    assert retrieved is not None
    assert retrieved.name == "LeBron James"


def test_filter_by_position():
    """Test filtering by position"""
    processor = DataProcessor()
    processor.add_player(PlayerData("1", "LeBron", "Forward", "6'9", 250, "Lakers", 23))
    processor.add_player(PlayerData("2", "Steph", "Guard", "6'2", 190, "Warriors", 30))
    
    forwards = processor.filter_by_position("Forward")
    assert len(forwards) == 1
    assert forwards[0].name == "LeBron"


def test_statistics():
    """Test dataset statistics"""
    processor = DataProcessor()
    processor.add_player(PlayerData("1", "LeBron", "Forward", "6'9", 250, "Lakers", 23))
    processor.add_player(PlayerData("2", "Steph", "Guard", "6'2", 190, "Warriors", 30))
    
    stats = processor.get_statistics()
    assert stats["total_players"] == 2
    assert stats["unique_positions"] == 2
    assert stats["unique_teams"] == 2


if __name__ == "__main__":
    test_data_processor_initialization()
    test_add_and_get_player()
    test_filter_by_position()
    test_statistics()
    print("All data processor tests passed!")

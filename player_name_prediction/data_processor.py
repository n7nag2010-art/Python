"""Data Processing Module for Player Information"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import csv
from pathlib import Path


@dataclass
class PlayerData:
    """Player data structure"""
    player_id: str
    name: str
    position: str
    height: str
    weight: int
    team: str
    jersey_number: int
    draft_year: Optional[int] = None
    country: Optional[str] = None
    college: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DataProcessor:
    """Process and manage player data"""

    def __init__(self):
        self.players: Dict[str, PlayerData] = {}
        self.dataset_path = Path("data")
        self.dataset_path.mkdir(exist_ok=True)

    def add_player(self, player: PlayerData) -> None:
        """Add player to database"""
        self.players[player.player_id] = player

    def get_player(self, player_id: str) -> Optional[PlayerData]:
        """Get player by ID"""
        return self.players.get(player_id)

    def get_all_players(self) -> List[PlayerData]:
        """Get all players"""
        return list(self.players.values())

    def filter_by_position(self, position: str) -> List[PlayerData]:
        """Filter players by position"""
        return [p for p in self.players.values() if p.position.lower() == position.lower()]

    def filter_by_team(self, team: str) -> List[PlayerData]:
        """Filter players by team"""
        return [p for p in self.players.values() if p.team.lower() == team.lower()]

    def save_to_json(self, filename: str = "players.json") -> None:
        """Save player data to JSON file"""
        filepath = self.dataset_path / filename
        data = {pid: p.to_dict() for pid, p in self.players.items()}
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_json(self, filename: str = "players.json") -> None:
        """Load player data from JSON file"""
        filepath = self.dataset_path / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                data = json.load(f)
                for pid, player_dict in data.items():
                    self.players[pid] = PlayerData(**player_dict)

    def export_csv(self, filename: str = "players.csv") -> None:
        """Export player data to CSV"""
        filepath = self.dataset_path / filename
        if not self.players:
            return
        
        with open(filepath, 'w', newline='') as f:
            fieldnames = list(self.players[list(self.players.keys())[0]].to_dict().keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for player in self.players.values():
                writer.writerow(player.to_dict())

    def get_statistics(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        if not self.players:
            return {"total_players": 0}
        
        positions = {}
        teams = {}
        for player in self.players.values():
            positions[player.position] = positions.get(player.position, 0) + 1
            teams[player.team] = teams.get(player.team, 0) + 1
        
        return {
            "total_players": len(self.players),
            "positions": positions,
            "teams": teams,
            "unique_positions": len(positions),
            "unique_teams": len(teams)
        }

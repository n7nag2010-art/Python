"""Machine Learning Model for Name Prediction"""

import json
from typing import Dict, List, Any, Tuple
from collections import Counter
import math


class NamePredictionModel:
    """ML Model for predicting player names"""

    def __init__(self):
        self.name_patterns = {}
        self.position_names = {}
        self.team_names = {}
        self.n_gram_model = {}
        self.is_trained = False

    def train(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train the model on player data"""
        self._extract_patterns(training_data)
        self._build_position_model(training_data)
        self._build_team_model(training_data)
        self._build_ngram_model(training_data)
        self.is_trained = True
        
        return {
            "status": "trained",
            "samples": len(training_data),
            "pattern_count": len(self.name_patterns),
            "positions_tracked": len(self.position_names),
            "teams_tracked": len(self.team_names)
        }

    def _extract_patterns(self, data: List[Dict[str, Any]]) -> None:
        """Extract name patterns from data"""
        names = [d.get("name", "") for d in data if "name" in d]
        
        for name in names:
            # First letter pattern
            if name:
                first_letter = name[0]
                self.name_patterns[first_letter] = self.name_patterns.get(first_letter, 0) + 1
            
            # Length pattern
            length = len(name)
            pattern_key = f"length_{length}"
            self.name_patterns[pattern_key] = self.name_patterns.get(pattern_key, 0) + 1

    def _build_position_model(self, data: List[Dict[str, Any]]) -> None:
        """Build position-specific name model"""
        for item in data:
            position = item.get("position", "unknown")
            name = item.get("name", "")
            
            if position not in self.position_names:
                self.position_names[position] = []
            self.position_names[position].append(name)

    def _build_team_model(self, data: List[Dict[str, Any]]) -> None:
        """Build team-specific name model"""
        for item in data:
            team = item.get("team", "unknown")
            name = item.get("name", "")
            
            if team not in self.team_names:
                self.team_names[team] = []
            self.team_names[team].append(name)

    def _build_ngram_model(self, data: List[Dict[str, Any]]) -> None:
        """Build n-gram model for name generation"""
        names = [d.get("name", "").lower() for d in data if "name" in d]
        
        # Bigram model
        bigrams = []
        for name in names:
            for i in range(len(name) - 1):
                bigrams.append(name[i:i+2])
        
        self.n_gram_model["bigrams"] = Counter(bigrams)

    def predict(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict player name based on context"""
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        position = context.get("position", "unknown")
        team = context.get("team", "unknown")
        
        # Get candidates from position model
        position_candidates = self.position_names.get(position, [])
        team_candidates = self.team_names.get(team, [])
        
        # Score candidates
        scores = {}
        for name in set(position_candidates + team_candidates):
            score = 0
            if name in position_candidates:
                score += 0.5
            if name in team_candidates:
                score += 0.5
            scores[name] = score
        
        # Get top predictions
        sorted_predictions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_predictions = sorted_predictions[:5]
        
        return {
            "top_predictions": [name for name, score in top_predictions],
            "scores": dict(top_predictions),
            "confidence": self._calculate_confidence(top_predictions)
        }

    def _calculate_confidence(self, predictions: List[Tuple[str, float]]) -> float:
        """Calculate prediction confidence"""
        if not predictions:
            return 0.0
        
        top_score = predictions[0][1] if predictions else 0
        return min(top_score, 1.0)

    def evaluate(self, test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate model performance"""
        correct = 0
        total = len(test_data)
        
        for item in test_data:
            prediction = self.predict({"position": item.get("position"), "team": item.get("team")})
            if item.get("name") in prediction.get("top_predictions", []):
                correct += 1
        
        accuracy = correct / total if total > 0 else 0
        return {
            "accuracy": accuracy,
            "correct_predictions": correct,
            "total_samples": total
        }

    def save_model(self, filepath: str) -> None:
        """Save model to file"""
        model_data = {
            "name_patterns": self.name_patterns,
            "position_names": {k: v for k, v in self.position_names.items()},
            "team_names": {k: v for k, v in self.team_names.items()},
            "is_trained": self.is_trained
        }
        with open(filepath, 'w') as f:
            json.dump(model_data, f, indent=2)

    def load_model(self, filepath: str) -> None:
        """Load model from file"""
        with open(filepath, 'r') as f:
            model_data = json.load(f)
            self.name_patterns = model_data.get("name_patterns", {})
            self.position_names = model_data.get("position_names", {})
            self.team_names = model_data.get("team_names", {})
            self.is_trained = model_data.get("is_trained", False)

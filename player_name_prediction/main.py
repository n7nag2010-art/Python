#!/usr/bin/env python3
"""Main entry point for Player Name Prediction Agentic AI System"""

import sys
from typing import Dict, Any
from agent import PlayerNamePredictionAgent
from data_processor import DataProcessor, PlayerData
from model import NamePredictionModel


class PlayerNamePredictionSystem:
    """Complete agentic AI system for player name prediction"""

    def __init__(self):
        self.agent = PlayerNamePredictionAgent()
        self.data_processor = DataProcessor()
        self.model = NamePredictionModel()
        self.setup_demo_data()

    def setup_demo_data(self) -> None:
        """Setup demo player data"""
        demo_players = [
            PlayerData("1", "LeBron James", "Forward", "6'9", 250, "Lakers", 23, 2003),
            PlayerData("2", "Stephen Curry", "Guard", "6'2", 190, "Warriors", 30, 2009),
            PlayerData("3", "Kevin Durant", "Forward", "7'0", 240, "Suns", 35, 2007),
            PlayerData("4", "Nikola Jokic", "Center", "6'11", 280, "Nuggets", 15, 2014),
            PlayerData("5", "Luka Doncic", "Guard", "6'7", 230, "Mavericks", 77, 2018),
            PlayerData("6", "Jayson Tatum", "Forward", "6'8", 210, "Celtics", 0, 2017),
            PlayerData("7", "Damian Lillard", "Guard", "6'2", 195, "Blazers", 0, 2012),
            PlayerData("8", "Giannis Antetokounmpo", "Forward", "6'11", 242, "Bucks", 34, 2013),
        ]
        
        for player in demo_players:
            self.data_processor.add_player(player)

    def run_demo(self) -> None:
        """Run demonstration of the system"""
        print("\n" + "="*60)
        print("Player Name Prediction - Agentic AI System")
        print("="*60 + "\n")

        # Show agent state
        print("Agent State:")
        agent_state = self.agent.get_agent_state()
        for key, value in agent_state.items():
            print(f"  {key}: {value}")

        # Show data statistics
        print("\nDataset Statistics:")
        stats = self.data_processor.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # Train model
        print("\nTraining Model...")
        training_data = [p.to_dict() for p in self.data_processor.get_all_players()]
        train_result = self.model.train(training_data)
        for key, value in train_result.items():
            print(f"  {key}: {value}")

        # Run predictions
        print("\nRunning Predictions with Agentic AI:\n")
        
        test_contexts = [
            {"position": "Guard", "team": "Warriors", "jersey_number": 30},
            {"position": "Forward", "team": "Lakers", "jersey_number": 23},
            {"position": "Center", "team": "Nuggets", "jersey_number": 15},
        ]

        for i, context in enumerate(test_contexts, 1):
            print(f"Prediction {i}:")
            print(f"  Input Context: {context}")
            
            # Agent prediction
            agent_prediction = self.agent.predict(context)
            print(f"  Agent Predicted Name: {agent_prediction['predicted_name']}")
            print(f"  Confidence: {agent_prediction['confidence']:.2f}")
            print(f"  Reasoning: {agent_prediction['reasoning']}")
            print(f"  Alternatives: {agent_prediction['alternatives']}")
            print(f"  Validation Score: {agent_prediction['validation_score']:.2f}")
            
            # Model prediction
            model_prediction = self.model.predict(context)
            if "top_predictions" in model_prediction:
                print(f"  ML Model Top Predictions: {model_prediction['top_predictions'][:3]}")
            print()

        # Model evaluation
        print("\nModel Evaluation:")
        eval_result = self.model.evaluate(training_data)
        for key, value in eval_result.items():
            print(f"  {key}: {value}")

        # Save data and model
        print("\nSaving Data and Model...")
        self.data_processor.save_to_json()
        self.data_processor.export_csv()
        self.model.save_model("player_name_model.json")
        print("  ✓ Data saved to data/players.json")
        print("  ✓ CSV exported to data/players.csv")
        print("  ✓ Model saved to player_name_model.json")

        # Display agent memory
        print("\nAgent Learning Summary:")
        print(f"  Predictions stored in memory: {len(self.agent.memory)}")
        print(f"  Total actions performed: {len(self.agent.action_history)}")
        print("\n" + "="*60)
        print("System demonstration completed successfully!")
        print("="*60 + "\n")

    def interactive_mode(self) -> None:
        """Run in interactive mode"""
        print("\nEntering Interactive Mode...")
        print("Commands: predict, stats, train, exit")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == "exit":
                    print("Exiting...")
                    break
                elif command == "stats":
                    stats = self.data_processor.get_statistics()
                    print(json.dumps(stats, indent=2))
                elif command == "train":
                    training_data = [p.to_dict() for p in self.data_processor.get_all_players()]
                    result = self.model.train(training_data)
                    print(json.dumps(result, indent=2))
                elif command == "predict":
                    position = input("Position: ")
                    team = input("Team: ")
                    prediction = self.agent.predict({"position": position, "team": team})
                    print(f"\nPredicted Name: {prediction['predicted_name']}")
                    print(f"Confidence: {prediction['confidence']:.2f}")
                else:
                    print("Unknown command. Try: predict, stats, train, exit")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main function"""
    import json
    
    system = PlayerNamePredictionSystem()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        system.interactive_mode()
    else:
        system.run_demo()


if __name__ == "__main__":
    main()

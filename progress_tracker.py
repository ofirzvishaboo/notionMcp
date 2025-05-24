from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os
from api_interactions import NotionAPI

class ProgressTracker:
    def __init__(self):
        """Initialize the progress tracker with Notion API integration."""
        self.notion_api = NotionAPI()

    def track_completion(self, task_id: str, progress: int) -> bool:
        """
        Track the completion progress of a task.

        Args:
            task_id: The ID of the task
            progress: Progress percentage (0-100)

        Returns:
            bool: True if successful, False otherwise
        """
        return self.notion_api.update_progress(task_id, progress)

    def get_weekly_progress(self, week_number: int) -> Dict:
        """
        Get progress statistics for a specific week.

        Args:
            week_number: The week number to get progress for

        Returns:
            Dict: Progress statistics for the week
        """
        # Calculate date range for the week
        start_date = datetime.now() - timedelta(days=7 * (week_number - 1))
        end_date = start_date + timedelta(days=6)

        # Query tasks for the week
        filter_params = {
            "and": [
                {
                    "property": "Due Date",
                    "date": {
                        "on_or_after": start_date.isoformat()
                    }
                },
                {
                    "property": "Due Date",
                    "date": {
                        "on_or_before": end_date.isoformat()
                    }
                }
            ]
        }

        tasks = self.notion_api.query_database(
            os.getenv("TASKS_DATABASE_ID"),
            filter_params
        )

        # Calculate statistics
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task["properties"]["Progress"]["number"] == 100)
        average_progress = sum(task["properties"]["Progress"]["number"] for task in tasks) / total_tasks if total_tasks > 0 else 0

        return {
            "week_number": week_number,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "average_progress": average_progress
        }

    def adjust_difficulty(self, user_performance: Dict) -> Dict:
        """
        Adjust task difficulty based on user performance.

        Args:
            user_performance: Dictionary containing user performance metrics

        Returns:
            Dict: Adjusted difficulty parameters
        """
        # Default difficulty parameters
        difficulty = {
            "question_complexity": "medium",
            "summary_length": 200,
            "tasks_per_week": 5
        }

        # Adjust based on performance
        if user_performance["completion_rate"] > 80:
            # User is performing well, increase difficulty
            difficulty["question_complexity"] = "high"
            difficulty["summary_length"] = 250
            difficulty["tasks_per_week"] = 7
        elif user_performance["completion_rate"] < 50:
            # User is struggling, decrease difficulty
            difficulty["question_complexity"] = "low"
            difficulty["summary_length"] = 150
            difficulty["tasks_per_week"] = 3

        return difficulty

    def get_feedback(self) -> Dict:
        """
        Get user feedback about their learning experience.

        Returns:
            Dict: User feedback and suggestions
        """
        print("\nHow did you feel about this week's learning?")
        print("1. Too easy")
        print("2. Just right")
        print("3. Too difficult")

        while True:
            try:
                response = int(input("Enter your choice (1-3): "))
                if 1 <= response <= 3:
                    break
                print("Please enter a number between 1 and 3")
            except ValueError:
                print("Please enter a valid number")

        print("\nAny areas you need more help with? (Press Enter to skip)")
        areas = input().strip()

        return {
            "difficulty_rating": response,
            "areas_for_improvement": areas if areas else None
        }
import streamlit as st
import os
from datetime import datetime, timedelta
from typing import Dict, List
from api_interactions import NotionAPI
from summaries import SummaryGenerator
from questions import QuestionGenerator
from progress_tracker import ProgressTracker

class LearningAssistant:
    def __init__(self):
        """Initialize the learning assistant with all necessary components."""
        self.notion_api = NotionAPI()
        self.summary_generator = SummaryGenerator()
        self.question_generator = QuestionGenerator()
        self.progress_tracker = ProgressTracker()

    def process_learning_material(self, content: str) -> Dict:
        """
        Process learning material to generate summary and questions.

        Args:
            content: The learning material to process

        Returns:
            Dict: Generated summary and questions
        """
        # Generate summary
        summary, is_valid = self.summary_generator.generate_summary(content)
        if not is_valid:
            st.warning("Generated summary exceeds word limit. Please try with shorter content.")
            return None

        # Confirm summary
        if not self.summary_generator.confirm_summary(summary):
            st.info("Summary rejected. Please try again with different content.")
            return None

        # Generate questions
        questions = self.question_generator.generate_questions(summary)
        validated_questions = self.question_generator.validate_questions(questions)

        return {
            "summary": summary,
            "questions": validated_questions
        }

    def create_weekly_tasks(self, week_number: int, difficulty: Dict) -> List[str]:
        """
        Create weekly learning tasks.

        Args:
            week_number: The week number
            difficulty: Difficulty parameters

        Returns:
            List[str]: List of created task IDs
        """
        task_ids = []
        start_date = datetime.now() + timedelta(days=7 * (week_number - 1))

        # Create summary task
        summary_task_id = self.notion_api.create_task(
            title=f"Week {week_number} Summary",
            due_date=(start_date + timedelta(days=2)).isoformat(),
            progress=0
        )
        task_ids.append(summary_task_id)

        # Create question tasks
        for i in range(difficulty["tasks_per_week"]):
            question_task_id = self.notion_api.create_task(
                title=f"Week {week_number} Question Set {i+1}",
                due_date=(start_date + timedelta(days=3+i)).isoformat(),
                progress=0
            )
            task_ids.append(question_task_id)

        return task_ids

def main():
    st.title("Learning Assistant")

    # Initialize the assistant
    assistant = LearningAssistant()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Process Material", "View Progress", "Settings"])

    if page == "Process Material":
        st.header("Process Learning Material")

        # Input for learning material
        content = st.text_area("Enter your learning material:", height=200)

        if st.button("Process"):
            if content:
                with st.spinner("Processing..."):
                    result = assistant.process_learning_material(content)
                    if result:
                        st.subheader("Generated Summary")
                        st.write(result["summary"])

                        st.subheader("Review Questions")
                        for i, qa in enumerate(result["questions"], 1):
                            st.write(f"Q{i}. {qa['question']}")
                            with st.expander(f"Answer {i}"):
                                st.write(qa["answer"])
            else:
                st.warning("Please enter some learning material.")

    elif page == "View Progress":
        st.header("Learning Progress")

        # Get current week number
        current_week = (datetime.now() - datetime(2024, 1, 1)).days // 7 + 1

        # Display weekly progress
        progress = assistant.progress_tracker.get_weekly_progress(current_week)

        st.subheader(f"Week {current_week} Progress")
        st.write(f"Total Tasks: {progress['total_tasks']}")
        st.write(f"Completed Tasks: {progress['completed_tasks']}")
        st.write(f"Completion Rate: {progress['completion_rate']:.1f}%")
        st.write(f"Average Progress: {progress['average_progress']:.1f}%")

        # Progress bar
        st.progress(progress['completion_rate'] / 100)

    else:  # Settings
        st.header("Settings")

        # Display current difficulty settings
        st.subheader("Current Difficulty Settings")
        difficulty = assistant.progress_tracker.adjust_difficulty({
            "completion_rate": 70  # Example value
        })

        st.write(f"Question Complexity: {difficulty['question_complexity']}")
        st.write(f"Summary Length: {difficulty['summary_length']} words")
        st.write(f"Tasks per Week: {difficulty['tasks_per_week']}")

        # Feedback section
        st.subheader("Provide Feedback")
        if st.button("Give Feedback"):
            feedback = assistant.progress_tracker.get_feedback()
            st.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()
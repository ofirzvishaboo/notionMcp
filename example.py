from assistant import LearningAssistant
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()

    # Initialize the assistant
    assistant = LearningAssistant()

    # Example 1: Process learning material
    learning_content = """
    Python is a high-level, interpreted programming language known for its simplicity and readability.
    It was created by Guido van Rossum and first released in 1991. Python supports multiple programming paradigms,
    including procedural, object-oriented, and functional programming. Its design philosophy emphasizes code
    readability with its notable use of significant whitespace. Python features a dynamic type system and
    automatic memory management. It has a comprehensive standard library and is often called a "batteries included"
    language. Python is widely used in web development, data analysis, artificial intelligence, scientific computing,
    and automation. The language's popularity has grown significantly due to its versatility and the large ecosystem
    of third-party packages available through the Python Package Index (PyPI).
    """

    print("Example 1: Processing Learning Material")
    print("-" * 50)
    result = assistant.process_learning_material(learning_content)
    if result:
        print("\nGenerated Summary:")
        print(result["summary"])
        print("\nGenerated Questions:")
        for i, qa in enumerate(result["questions"], 1):
            print(f"\nQ{i}. {qa['question']}")
            print(f"A{i}. {qa['answer']}")

    # Example 2: Create weekly tasks
    print("\nExample 2: Creating Weekly Tasks")
    print("-" * 50)
    week_number = 1
    difficulty = {
        "question_complexity": "medium",
        "summary_length": 200,
        "tasks_per_week": 5
    }

    task_ids = assistant.create_weekly_tasks(week_number, difficulty)
    print(f"Created {len(task_ids)} tasks for week {week_number}")

    # Example 3: Track progress
    print("\nExample 3: Tracking Progress")
    print("-" * 50)
    # Update progress for the first task
    if task_ids:
        assistant.progress_tracker.track_completion(task_ids[0], 50)
        print(f"Updated progress for task {task_ids[0]} to 50%")

    # Get weekly progress
    progress = assistant.progress_tracker.get_weekly_progress(week_number)
    print("\nWeekly Progress:")
    print(f"Total Tasks: {progress['total_tasks']}")
    print(f"Completed Tasks: {progress['completed_tasks']}")
    print(f"Completion Rate: {progress['completion_rate']:.1f}%")
    print(f"Average Progress: {progress['average_progress']:.1f}%")

if __name__ == "__main__":
    main()
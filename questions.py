from transformers import pipeline
from typing import List, Dict
import torch

class QuestionGenerator:
    def __init__(self):
        """Initialize the question generator with a pre-trained model."""
        # Check if CUDA is available, otherwise use CPU
        device = 0 if torch.cuda.is_available() else -1
        self.question_generator = pipeline(
            "text2text-generation",
            model="t5-base",
            device=device
        )

    def generate_questions(self, text: str, num_questions: int = 3) -> List[Dict]:
        """
        Generate questions based on the input text.

        Args:
            text: The text to generate questions from
            num_questions: Number of questions to generate

        Returns:
            List[Dict]: List of generated questions with their answers
        """
        try:
            questions = []
            for _ in range(num_questions):
                # Generate question
                question_prompt = f"generate question: {text}"
                question_response = self.question_generator(
                    question_prompt,
                    max_new_tokens=50,
                    num_return_sequences=1
                )
                question = question_response[0]['generated_text'].strip()

                # Generate answer
                answer_prompt = f"answer this question based on the text: {question} {text}"
                answer_response = self.question_generator(
                    answer_prompt,
                    max_new_tokens=100,
                    num_return_sequences=1
                )
                answer = answer_response[0]['generated_text'].strip()

                questions.append({
                    "question": question,
                    "answer": answer
                })

            return questions

        except Exception as e:
            print(f"Error generating questions: {e}")
            return []

    def validate_questions(self, questions: List[Dict]) -> List[Dict]:
        """
        Validate generated questions for quality and relevance.

        Args:
            questions: List of question-answer pairs

        Returns:
            List[Dict]: List of validated questions
        """
        validated_questions = []

        for qa in questions:
            # Basic validation rules
            if (len(qa["question"].split()) >= 3 and  # Question should be at least 3 words
                "?" in qa["question"] and  # Should end with question mark
                len(qa["answer"].split()) >= 5):  # Answer should be at least 5 words
                validated_questions.append(qa)

        return validated_questions

    def format_questions(self, questions: List[Dict]) -> str:
        """
        Format questions and answers for display.

        Args:
            questions: List of question-answer pairs

        Returns:
            str: Formatted string of questions and answers
        """
        formatted_text = "Review Questions:\n\n"

        for i, qa in enumerate(questions, 1):
            formatted_text += f"Q{i}. {qa['question']}\n"
            formatted_text += f"A{i}. {qa['answer']}\n\n"

        return formatted_text
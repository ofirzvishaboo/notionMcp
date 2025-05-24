from transformers import pipeline
from typing import Optional, Tuple
import torch

class SummaryGenerator:
    def __init__(self):
        """Initialize the summary generator with a pre-trained model."""
        # Force CPU usage to avoid device switching issues
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1  # Force CPU
        )

    def generate_summary(self, text: str, max_length: int = 200) -> Tuple[str, bool]:
        """
        Generate a summary of the input text.

        Args:
            text: The text to summarize
            max_length: Maximum length of the summary in words

        Returns:
            Tuple[str, bool]: The generated summary and a flag indicating if it's within the word limit
        """
        try:
            # Ensure minimum input length
            if len(text.split()) < 10:
                return "Input text is too short for summarization. Please provide more content.", False

            # Split text into chunks if it's too long
            chunks = self._split_text(text)
            summaries = []

            for chunk in chunks:
                # Calculate appropriate max_length for the chunk
                chunk_length = len(chunk.split())
                # More aggressive summarization - target 1/3 of the original length
                chunk_max_length = min(max_length // len(chunks), max(30, chunk_length // 3))

                summary = self.summarizer(
                    chunk,
                    max_new_tokens=chunk_max_length,
                    min_length=min(30, chunk_max_length // 2),
                    do_sample=False
                )
                summaries.append(summary[0]['summary_text'])

            final_summary = " ".join(summaries)
            word_count = len(final_summary.split())

            # If still too long, do a final pass
            if word_count > max_length:
                final_summary = self.summarizer(
                    final_summary,
                    max_new_tokens=max_length,
                    min_length=max_length // 2,
                    do_sample=False
                )[0]['summary_text']
                word_count = len(final_summary.split())

            return final_summary, word_count <= max_length

        except Exception as e:
            print(f"Error generating summary: {e}")
            return "", False

    def _split_text(self, text: str, chunk_size: int = 512) -> list:
        """
        Split text into smaller chunks for processing.

        Args:
            text: The text to split
            chunk_size: Maximum size of each chunk

        Returns:
            list: List of text chunks
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1  # +1 for space

            if current_size >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def confirm_summary(self, summary: str) -> bool:
        """
        Ask for user confirmation of the generated summary.

        Args:
            summary: The summary to confirm

        Returns:
            bool: True if confirmed, False otherwise
        """
        print("\nGenerated Summary:")
        print(summary)
        print(f"\nWord count: {len(summary.split())}")
        print("\nDo you confirm this summary as accurate? [Yes/No]")

        while True:
            response = input().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please answer with Yes/No or Y/N")
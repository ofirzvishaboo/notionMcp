import os
import asyncio
from typing import Dict, List, Optional
from notion_client import Client
from dotenv import load_dotenv
import torch

# Initialize PyTorch with CPU
torch.set_num_threads(1)
torch.set_num_interop_threads(1)

class NotionAPI:
    def __init__(self):
        """Initialize the Notion API client."""
        load_dotenv()
        self.client = Client(auth=os.getenv("NOTION_API_KEY"))

        # Ensure we're using CPU
        if torch.cuda.is_available():
            torch.cuda.set_device('cpu')

    def _truncate_text(self, text: str, max_length: int = 2000) -> str:
        """
        Truncate text to fit Notion's limits.

        Args:
            text: The text to truncate
            max_length: Maximum length allowed (default: 2000 for Notion)

        Returns:
            str: Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."

    def create_database(self, title: str, properties: Dict) -> str:
        """
        Create a new database in Notion.

        Args:
            title: The title of the database
            properties: Dictionary of property configurations

        Returns:
            str: The ID of the created database
        """
        try:
            response = self.client.databases.create(
                parent={"type": "page_id", "page_id": os.getenv("NOTION_PAGE_ID")},
                title=[{"type": "text", "text": {"content": title}}],
                properties=properties
            )
            return response["id"]
        except Exception as e:
            print(f"Error creating database: {e}")
            return None

    def create_page(self, database_id: str, properties: Dict) -> str:
        """
        Create a new page in a Notion database.

        Args:
            database_id: The ID of the database
            properties: Dictionary of page properties

        Returns:
            str: The ID of the created page
        """
        try:
            # Truncate text content if it exists
            for prop_name, prop_value in properties.items():
                if isinstance(prop_value, dict) and "rich_text" in prop_value:
                    for text_block in prop_value["rich_text"]:
                        if "text" in text_block and "content" in text_block["text"]:
                            text_block["text"]["content"] = self._truncate_text(text_block["text"]["content"])
                elif isinstance(prop_value, dict) and "title" in prop_value:
                    for title_block in prop_value["title"]:
                        if "text" in title_block and "content" in title_block["text"]:
                            title_block["text"]["content"] = self._truncate_text(title_block["text"]["content"])

            response = self.client.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            return response["id"]
        except Exception as e:
            print(f"Error creating page: {e}")
            return None

    def update_page(self, page_id: str, properties: Dict) -> bool:
        """
        Update an existing page in Notion.

        Args:
            page_id: The ID of the page to update
            properties: Dictionary of updated properties

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )
            return True
        except Exception as e:
            print(f"Error updating page: {e}")
            return False

    def query_database(self, database_id: str, filter_params: Optional[Dict] = None) -> List[Dict]:
        """
        Query a Notion database.

        Args:
            database_id: The ID of the database to query
            filter_params: Optional filter parameters

        Returns:
            List[Dict]: List of pages matching the query
        """
        try:
            response = self.client.databases.query(
                database_id=database_id,
                filter=filter_params
            )
            return response["results"]
        except Exception as e:
            print(f"Error querying database: {e}")
            return []

    def create_task(self, title: str, due_date: str, progress: int = 0) -> str:
        """
        Create a new task in the tasks database.

        Args:
            title: The title of the task
            due_date: The due date of the task
            progress: The progress percentage (0-100)

        Returns:
            str: The ID of the created task
        """
        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Due Date": {"date": {"start": due_date}},
            "Progress": {"number": progress}
        }
        return self.create_page(os.getenv("TASKS_DATABASE_ID"), properties)

    def update_progress(self, page_id: str, progress: int) -> bool:
        """
        Update the progress of a task.

        Args:
            page_id: The ID of the task page
            progress: The new progress percentage (0-100)

        Returns:
            bool: True if successful, False otherwise
        """
        properties = {
            "Progress": {"number": progress}
        }
        return self.update_page(page_id, properties)
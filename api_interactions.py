import os
from typing import Dict, List, Optional
from notion_client import Client
from dotenv import load_dotenv

class NotionAPI:
    def __init__(self):
        """Initialize the Notion API client."""
        load_dotenv()
        self.client = Client(auth=os.getenv("NOTION_API_KEY"))

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
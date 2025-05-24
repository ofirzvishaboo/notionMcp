import os
from dotenv import load_dotenv
from api_interactions import NotionAPI

def setup_notion_database():
    # Load environment variables
    load_dotenv()

    # Initialize Notion API
    notion = NotionAPI()

    # Define database properties
    properties = {
        "Name": {
            "title": {}
        },
        "Due Date": {
            "date": {}
        },
        "Progress": {
            "number": {
                "format": "percent"
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Not Started", "color": "gray"},
                    {"name": "In Progress", "color": "blue"},
                    {"name": "Completed", "color": "green"}
                ]
            }
        },
        "Type": {
            "select": {
                "options": [
                    {"name": "Summary", "color": "purple"},
                    {"name": "Question Set", "color": "orange"}
                ]
            }
        }
    }

    # Create the database
    database_id = notion.create_database(
        title="Learning Tasks",
        properties=properties
    )

    if database_id:
        print(f"Database created successfully!")
        print(f"Database ID: {database_id}")
        print("\nPlease add this ID to your .env file as TASKS_DATABASE_ID")
    else:
        print("Failed to create database. Please check your Notion API key and page permissions.")

if __name__ == "__main__":
    setup_notion_database()
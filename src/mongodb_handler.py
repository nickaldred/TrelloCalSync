from pymongo import MongoClient
from pymongo.database import Database


class MongoDBHandler:
    """Handles all MongoDB operations."""

    def __init__(self, host: str, port: int, db_name: str):
        """
        Initialize MongoDBHandler with host, port and database name.

        Args:
            host (str): The host of the MongoDB server.
            port (int): The port of the MongoDB server.
            db_name (str): The name of the database to connect to.
        """
        self.client: MongoClient = MongoClient(host, port)
        self.db: Database = self.client[db_name]

    def add_collection(self, collection_name: str) -> bool:
        """
        Add a new collection to the database.

        Args:
            collection_name (str): The name of the new collection.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.db.create_collection(collection_name)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def add_document(self, collection_name: str, document: dict) -> bool:
        """
        Add a new document to a collection.

        Args:
            collection_name (str): The name of the collection.
            document (dict): The document to add.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            collection = self.db[collection_name]
            print(collection.insert_one(document))
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def update_document(
        self, collection_name: str, query: dict, new_values: dict
    ) -> bool:
        """
        Update a document in a collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to select the document.
            new_values (dict): The new values to update.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {"$set": new_values})
            return result.modified_count > 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def delete_document(self, collection_name: str, query: dict) -> bool:
        """
        Delete a document from a collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to select the document.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def create_index(self, collection_name: str, field_name: str) -> bool:
        """
        Create an index on a field in a collection.

        Args:
            collection_name (str): The name of the collection.
            field_name (str): The name of the field to index.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            collection = self.db[collection_name]
            collection.create_index(field_name)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def get_document(self, collection_name: str, query: dict) -> dict:
        """
        Get a document from a collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to select the document.

        Returns:
            dict: The document if found, None otherwise.
        """
        try:
            collection = self.db[collection_name]
            return collection.find_one(query)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None



test = MongoDBHandler('localhost', 27017, 'test')

test_data = {"board_id": "3", "cal_id": "3", "event_title": "test_event"}

# print(test.add_document('test_collection', test_data))


# test.create_index('test_collection', 'board_id')
# test.create_index('test_collection', 'cal_id')

print(test.get_document('test_collection', {'board_id': '3'}))
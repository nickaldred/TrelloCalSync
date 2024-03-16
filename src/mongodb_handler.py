"""Handles all MongoDB operations."""

from typing import Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult
from pymongo.errors import PyMongoError


class MongoDbHandler:
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

        except PyMongoError as e:
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
            collection: Collection = self.db[collection_name]
            collection.insert_one(document)
            return True

        except PyMongoError as e:
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
            collection: Collection = self.db[collection_name]
            result: UpdateResult = (
                collection.update_one(query, {"$set": new_values}))
            return result.modified_count > 0

        except PyMongoError as e:
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
            collection: Collection = self.db[collection_name]
            result: DeleteResult = collection.delete_one(query)
            return result.deleted_count > 0

        except PyMongoError as e:
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
            collection: Collection = self.db[collection_name]
            collection.create_index(field_name)
            return True
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            return False

    def get_document(self, collection_name: str, query: dict) -> Any:
        """
        Get a document from a collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to select the document.

        Returns:
            dict: The document if found, None otherwise.
        """

        try:
            collection: Collection = self.db[collection_name]
            document = collection.find_one(query)
            return document
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            return {}

    def get_collection(self, collection_name: str) -> Collection:
        """
        Get a collection from the database.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            Collection: The collection if found, None otherwise.
        """
        try:
            collection: Collection = self.db[collection_name]
            return collection
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            return None
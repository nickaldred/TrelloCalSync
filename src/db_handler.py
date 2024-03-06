"""This module contains the abstract base class for database handlers."""

from abc import ABC, abstractmethod


class DBHandler(ABC):
    """Abstract base class for database handlers."""

    @abstractmethod
    def add_collection(self, collection_name: str) -> bool:
        """Create a new collection in the database."""

    @abstractmethod
    def add_document(self, collection_name: str, document: dict) -> bool:
        """Add a new document to the specified collection in the
        database.
        """

    @abstractmethod
    def update_document(
        self, collection_name: str, query: dict, new_values: dict
    ) -> bool:
        """Update a document in the specified collection in the
        database.
        """

    @abstractmethod
    def delete_document(self, collection_name: str, query: dict) -> bool:
        """Delete a document from the specified collection in the
        database.
        """

    @abstractmethod
    def create_index(self, collection_name: str, field_name: str) -> bool:
        """Create an index on a field in the specified collection in
        the database.
        """

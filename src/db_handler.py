"""This module contains the abstract base class for database handlers."""

from abc import ABC, abstractmethod


class DBHandler(ABC):
    """Abstract base class for database handlers."""

    @abstractmethod
    def add_collection(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def add_document(self, collection_name: str, document: dict) -> bool:
        pass

    @abstractmethod
    def update_document(
        self, collection_name: str, query: dict, new_values: dict
    ) -> bool:
        pass

    @abstractmethod
    def delete_document(self, collection_name: str, query: dict) -> bool:
        pass

    @abstractmethod
    def create_index(self, collection_name: str, field_name: str) -> bool:
        pass
from abc import ABC, abstractmethod
from typing import TypeVar, Set
from uuid import UUID

from kirypto.basic_data_store.domain.objects import Item

TItem = TypeVar("TItem")
TId = TypeVar("TId")


class ItemPersistence(ABC):
    @abstractmethod
    def create(self, item: Item) -> None:
        pass

    @abstractmethod
    def retrieve(self, id: UUID) -> Item:
        pass

    @abstractmethod
    def retrieve_all(self) -> Set[UUID]:
        pass

    @abstractmethod
    def update(self, item: Item) -> None:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass

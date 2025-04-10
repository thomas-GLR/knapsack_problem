from typing import Set
from item import Item


class Solution:
    def __init__(self):
        self.items_indexes = set()
        self.profit = 0
        self.weight = 0

    def add_item(self, item_index: int, item: Item) -> None:
        self.items_indexes.add(item_index)
        self.weight += item.weight
        self.profit += item.profit

    def remove_item(self, item_index: int, item: Item) -> None:
        self.items_indexes.remove(item_index)
        self.weight -= item.weight
        self.profit -= item.profit

    def check_enough_place(self, item: Item, max_capacity) -> bool:
        return self.weight + item.weight <= max_capacity

    def contains_item(self, index_item: int) -> bool:
        return index_item in self.items_indexes

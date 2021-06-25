# -*- coding: utf-8 -*-

"""
src.models.coffee
~~~~~~~~~~~~~~~~~~~
This script contains the Coffee model, which represents a coffee beverage.
A coffee beverage can be brewed by a CoffeeMachine object.
"""
from typing import Any

from src.utils import Mililiters


class Coffee:
    """Who doesn't love a proper cup of coffee on Monday morning?"""

    def __init__(self, volume: Mililiters, with_milk: bool = False) -> None:
        self._volume: Mililiters = volume
        self._milk: Mililiters = with_milk

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._volume == other._volume and self._milk == other._milk

    @property
    def volume(self) -> Mililiters:
        return self._volume

    @property
    def milk(self) -> Mililiters:
        return self._milk

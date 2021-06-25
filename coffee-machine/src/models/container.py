# -*- coding: utf-8 -*-

"""
src.models.container
~~~~~~~~~~~~~~~~~~~
This script contains the Container model and its two extensions: WaterContainer and MilkContainer.
"""
from src.exceptions import NotEnoughCoffeeBeans
from src.exceptions import NotEnoughRefillable
from src.exceptions import NotEnoughMilk
from src.exceptions import NotEnoughWater
from src.utils import Mililiters, Refillable
from src.utils import Grams


class Container:
    """The Container contains the substance needed for preparing beverages"""

    error_when_empty = NotEnoughRefillable

    def __init__(self, capacity: Refillable = 1000):
        self._capacity: Refillable = capacity
        self._fill_level: Refillable = 0

    @property
    def fill_level(self) -> Refillable:
        return self._fill_level

    @property
    def capacity(self) -> Refillable:
        return self._capacity

    def _get_refillable(self, quantity: Refillable = 0) -> Refillable:
        """Obtain a given quantity of a refillable material out of the Container"""
        if self._fill_level < quantity:
            raise self.error_when_empty
        self._fill_level -= quantity
        return quantity

    def refill(self) -> None:
        """Refill the Container to the brim"""
        self._fill_level = self._capacity


class WaterContainer(Container):
    """The WaterContainer contains water needed for preparing beverages"""

    def __init__(self, capacity: Mililiters = 1000) -> None:
        super().__init__(capacity=capacity)
        self.error_when_empty = NotEnoughWater

    def get_water(self, volume: Mililiters = 0) -> Mililiters:
        """Pump out a given amount of water out of the WaterContainer"""
        return super()._get_refillable(quantity=volume)


class MilkContainer(Container):
    """The MilkContainer contains milk needed for preparing beverages"""

    def __init__(self, capacity: Mililiters = 1000) -> None:
        super().__init__(capacity=capacity)
        self.error_when_empty = NotEnoughMilk

    def get_milk(self, volume: Mililiters = 0) -> Mililiters:
        """Pump out a given amount of milk out of the MilkContainer"""
        return super()._get_refillable(quantity=volume)


class CoffeeBeansContainer(Container):
    """The CoffeeBeansContainer contains coffee beans needed for preparing beverages"""

    def __init__(self, capacity: Grams = 300) -> None:
        super().__init__(capacity=capacity)
        self.error_when_empty = NotEnoughCoffeeBeans

    def get_coffee_beans(self, weight: Grams = 0) -> Grams:
        """Obtain a given weight of coffee beans out of the CoffeeBeansContainer"""
        return super()._get_refillable(quantity=weight)

# -*- coding: utf-8 -*-

"""
src.models.coffee_machine
~~~~~~~~~~~~~~~~~~~
This script contains the CoffeeMachine model, which represents a coffee machine.
A coffee machine can brew various servings of Coffee objects.
It consists of a milk container and a water container.
"""

from typing import Dict

from src.models.container import CoffeeBeansContainer
from src.exceptions import NotEnoughMilk
from src.exceptions import NotEnoughWater
from src.exceptions import TurnedOff
from src.exceptions import NotEnoughCoffeeBeans
from src.models.container import MilkContainer
from src.models.container import WaterContainer
from src.models.coffee import Coffee
from src.utils import Mililiters
from src.utils import Beverage
from src.utils import Grams
from src.utils import Material
from src.utils import Refillable
from src.utils import Serving


class CoffeeMachine:
    """The CoffeeMachine serves coffee-like beverages"""

    _servings: Dict[Beverage, Dict[Serving, Dict[Material, Refillable]]] = {
        'coffee': {
            'small': {'water': 100, 'coffee beans': 8},
            'medium': {'water': 150, 'coffee beans': 12},
            'large': {'water': 250, 'coffee beans': 20},
            'default': {'water': 150, 'coffee beans': 12}
        },
        # 'espresso': {
        #     'single': {'water': 50, 'coffee beans': 10},
        #     'double': {'water': 100, 'coffee beans': 20},
        #     'default': 50
        # },
        'default': {
            # 'single': {'water': 50, 'coffee beans': 10},
            # 'double': {'water': 100, 'coffee beans': 20},
            'small': {'water': 100, 'coffee beans': 8},
            'medium': {'water': 150, 'coffee beans': 12},
            'large': {'water': 250, 'coffee beans': 20},
            'default': {'water': 150, 'coffee beans': 12}
        }
    }
    _milk_serving: Mililiters = 50

    def __init__(self,
                 water_container_capacity: Mililiters = 1000,
                 milk_container_capacity: Mililiters = 500,
                 coffee_beans_container_capacity: Grams = 75) -> None:
        self._is_on: bool = False
        self._water_container: WaterContainer = WaterContainer(capacity=water_container_capacity)
        self._milk_container: MilkContainer = MilkContainer(capacity=milk_container_capacity)
        self._coffee_beans_container: CoffeeBeansContainer = CoffeeBeansContainer(
            capacity=coffee_beans_container_capacity)

    def __str__(self) -> str:
        return f'''CoffeeMachine with: 
        WaterContainer ({self._water_container.fill_level}/{self._water_container.capacity} ml) 
        MilkContainer ({self._milk_container.fill_level}/{self._milk_container.capacity} ml)
        CoffeeBeansContainer ({self._coffee_beans_container.fill_level}/{self._coffee_beans_container.capacity} ml)
        Turned {"ON" if self._is_on else "OFF"}'''

    @property
    def is_on(self) -> bool:
        return self._is_on

    @property
    def water_level(self) -> Mililiters:
        """Check the remaining water in the container"""
        return self._water_container.fill_level

    @property
    def milk_level(self) -> Mililiters:
        """Check the remaining milk in the container"""
        return self._milk_container.fill_level

    @property
    def coffee_beans_level(self) -> Grams:
        """Check the remaining coffee beans in the container"""
        return self._coffee_beans_container.fill_level

    @property
    def milk_serving(self) -> Mililiters:
        """Check the milk serving for a beverage with milk"""
        return CoffeeMachine._milk_serving

    def turn_on(self) -> None:
        """Just turn the CoffeeMachine on."""
        self._is_on = True

    def turn_off(self) -> None:
        """It's over. Turn is off, for God's sake."""
        self._is_on = False

    def prepare_coffee(self, serving: Serving = 'default', with_milk: bool = False) -> Coffee:
        """Preparing Coffee never was so simple."""
        _coffee_volume = self.get_beverage_water_volume(beverage='coffee', serving=serving)
        _coffee_beans_weight = self.get_beverage_coffee_beans_weight(beverage='coffee',
                                                                     serving=serving)
        if self._is_on is False:
            raise TurnedOff

        # first check the requirements for a requested Coffee
        if self.water_level < _coffee_volume:
            raise NotEnoughWater
        if with_milk and self.milk_level < self.milk_serving:
            raise NotEnoughMilk
        if self.coffee_beans_level < _coffee_beans_weight:
            raise NotEnoughCoffeeBeans

        # then (try to) consume them
        try:
            _water_needed = self._water_container.get_water(volume=_coffee_volume)
        except NotEnoughWater:
            raise NotEnoughWater
        if with_milk:
            try:
                _milk_needed = self._milk_container.get_milk(volume=self._milk_serving)
            except NotEnoughMilk:
                raise NotEnoughMilk
        try:
            _coffee_beans_needed = self._coffee_beans_container.get_coffee_beans(
                weight=_coffee_beans_weight)
        except NotEnoughWater:
            raise NotEnoughWater
        # TODO: use the water to brew coffee with Brewer object
        #  instead of just mocking the whole process
        return Coffee(volume=_water_needed, with_milk=with_milk)

    def prepare_coffee_with_milk(self, serving: Serving = 'default') -> Coffee:
        """Explicitly ask for a coffee with milk. No milk, no satisfaction."""
        return self.prepare_coffee(serving=serving, with_milk=True)

    def refill_water(self) -> None:
        """Make sure there is enough water for the beverages to be brewed"""
        self._water_container.refill()

    def refill_milk(self) -> None:
        """Don't forget about the milk"""
        self._milk_container.refill()

    def refill_coffee_beans(self):
        """No coffee beans? Not anymore!"""
        self._coffee_beans_container.refill()

    @staticmethod
    def _get_servings_for_beverage(beverage: Beverage = 'default'
                                   ) -> Dict[Serving, Dict[Material, Refillable]]:
        # TODO """Get a mapping between the beverage and its servings"""
        try:
            return CoffeeMachine._servings[beverage]
        except KeyError:
            # TODO: inform about switching to default value
            return CoffeeMachine._servings['default']

    @staticmethod
    def _get_required_materials_for_beverage_serving(
            beverage: Beverage = 'default',
            serving: Serving = 'default'
    ) -> Dict[Material, Refillable]:
        """Get required materials for the specific serving of the specific beverage"""
        _beverage_servings: Dict[Serving, Dict[Material, Refillable]] = \
            CoffeeMachine._get_servings_for_beverage(beverage)
        try:
            return _beverage_servings[serving]
        except KeyError:
            # TODO: inform about switching to default value
            return _beverage_servings['default']

    @staticmethod
    def get_beverage_water_volume(beverage: Beverage = 'default',
                                  serving: Serving = 'default') -> Mililiters:
        """Get volume of the water used for the specific serving of the specific beverage"""
        _beverage_serving_required_materials: Dict[Material, Refillable] = \
            CoffeeMachine._get_required_materials_for_beverage_serving(beverage=beverage,
                                                                       serving=serving)
        try:
            return _beverage_serving_required_materials['water']
        except KeyError:
            # TODO: inform about returning 0
            return 0

    @staticmethod
    def get_beverage_coffee_beans_weight(beverage: Beverage = 'default',
                                         serving: Serving = 'default') -> Grams:
        """Get weight of the coffee beans used for the specific serving of the specific beverage"""
        _beverage_serving_required_materials: Dict[Material, Refillable] = \
            CoffeeMachine._get_required_materials_for_beverage_serving(beverage=beverage,
                                                                       serving=serving)
        try:
            return _beverage_serving_required_materials['coffee beans']
        except KeyError:
            # TODO: inform about returning 0
            return 0


# -*- coding: utf-8 -*-

"""
tests.tests_models.test_milk_container
~~~~~~~~~~~~~~~~~~~
This script contains tests for the MilkContainer model.
"""

from pytest import fixture, mark, raises

from src.exceptions import CoffeeMachineException
from src.exceptions import NotEnoughMilk
from src.models.container import MilkContainer
from src.utils import Mililiters


@fixture()
def create_milk_container(request) -> MilkContainer:
    """Create MilkContainer object for testing."""
    try:
        _container_capacity = request.param
    except AttributeError:
        _container_capacity = TestMilkContainer.capacity_default
    _container = MilkContainer(capacity=_container_capacity)
    return _container


class TestMilkContainer:

    capacity_default: Mililiters = 1000

    @mark.parametrize(
        ('create_milk_container', 'milk_volume', 'expectation'),
        [(100, 200, raises(NotEnoughMilk)),
         (0, 1, raises(NotEnoughMilk))],
        indirect=['create_milk_container']
    )
    def test_fill_level_raise_not_enough_milk(self,
                                              create_milk_container: MilkContainer,
                                              milk_volume: Mililiters,
                                              expectation: CoffeeMachineException) -> None:
        """Test an edge case, when there is not enough milk to get from the MilkContainer"""
        with expectation:
            create_milk_container.get_milk(volume=milk_volume)

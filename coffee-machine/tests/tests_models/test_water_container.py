# -*- coding: utf-8 -*-

"""
tests.tests_models.test_water_container
~~~~~~~~~~~~~~~~~~~
This script contains tests for the WaterContainer model.
"""
from pytest import fixture, mark, raises

from src.exceptions import CoffeeMachineException
from src.exceptions import NotEnoughWater
from src.models.container import WaterContainer
from src.utils import Mililiters


@fixture
def create_water_container(request) -> WaterContainer:
    """Create WaterContainer object for testing."""
    try:
        _container_capacity = request.param
    except AttributeError:
        _container_capacity = TestWaterContainer.capacity_default
    _container = WaterContainer(capacity=_container_capacity)
    return _container


class TestWaterContainer:

    capacity_default: Mililiters = 1000

    @mark.parametrize(
        ('create_water_container', 'water_volume', 'expectation'),
        [(100, 200, raises(NotEnoughWater)),
         (0, 1, raises(NotEnoughWater))],
        indirect=['create_water_container']
    )
    def test_fill_level_raise_not_enough_water(self,
                                               create_water_container: WaterContainer,
                                               water_volume: Mililiters,
                                               expectation: CoffeeMachineException) -> None:
        """Test an edge case, when there is not enough water to get from the WaterContainer"""
        with expectation:
            create_water_container.get_water(volume=water_volume)

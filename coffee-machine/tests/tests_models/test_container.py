# -*- coding: utf-8 -*-

"""
tests.tests_models.test_container
~~~~~~~~~~~~~~~~~~~
This script contains tests for the Container model.
"""

from random import randrange

from pytest import fixture, mark, raises

from src.exceptions import NotEnoughRefillable
from src.exceptions import CoffeeMachineException
from src.models.container import Container
from src.utils import Refillable


@fixture()
def create_container(request) -> Container:
    """Create Container object for testing."""
    try:
        _container_capacity = request.param
    except AttributeError:
        _container_capacity = TestContainer.capacity_default
    _container = Container(capacity=_container_capacity)
    return _container


class TestContainer:
    capacity_default: Refillable = 1000

    def test_initialization(self, create_container: Container) -> None:
        """Test Container object initialization"""
        pass

    def test_initial_attribute_values(self, create_container: Container) -> None:
        """Test checking the initial attribute values of the Container"""
        assert create_container.capacity == TestContainer.capacity_default
        assert create_container.fill_level == 0

    @mark.parametrize(
        ('create_container', 'quantity_of_refillable_to_get', 'expected_fill_level'),
        [(1000, 500, 500),
         (500, 500, 0),
         (600, 0, 600)],
        indirect=['create_container']
    )
    def test_fill_level(self,
                        create_container: Container,
                        quantity_of_refillable_to_get: Refillable,
                        expected_fill_level: Refillable) -> None:
        """Test if we can get an actual fill level of the Container"""
        create_container.refill()
        assert create_container.fill_level == create_container.capacity
        create_container._get_refillable(quantity=quantity_of_refillable_to_get)
        assert create_container.fill_level == expected_fill_level

    @mark.parametrize(
        ('create_container', 'quantity_of_refillable_to_get', 'expected_exception'),
        [(100, 200, raises(NotEnoughRefillable)),
         (0, 1, raises(NotEnoughRefillable))],
        indirect=['create_container']
    )
    def test_fill_level_raise_not_enough_refillable(self,
                                                    create_container: Container,
                                                    quantity_of_refillable_to_get: Refillable,
                                                    expected_exception: CoffeeMachineException
                                                    ) -> None:
        """Test an edge case, when there is not enough material to get from the Container"""
        with expected_exception:
            create_container._get_refillable(quantity=quantity_of_refillable_to_get)

    def test_refill(self, create_container: Container) -> None:
        """Test refilling Container with a refillable material, after getting some/all of it"""
        _max_quantity = create_container.capacity
        create_container.refill()
        create_container._get_refillable(quantity=randrange(1, _max_quantity))
        assert create_container.fill_level != create_container.capacity
        create_container.refill()
        assert create_container.fill_level == create_container.capacity
        create_container._get_refillable(quantity=_max_quantity)
        assert create_container.fill_level == 0
        create_container.refill()
        assert create_container.fill_level == create_container.capacity

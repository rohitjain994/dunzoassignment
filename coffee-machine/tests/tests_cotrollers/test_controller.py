# -*- coding: utf-8 -*-

"""
tests.tests_controllers.test_controller
~~~~~~~~~~~~~~~~~~~
This script contains tests for the app Controller.
"""

import pytest
from src.controllers.controller import Controller


@pytest.fixture()
def create_controller() -> Controller:
    """Create Controller object for testing"""
    _controller = Controller()
    return _controller


class TestController:

    def test_initialization(self, create_controller: Controller) -> None:
        """Test Controller object initialization"""
        pass

    def test_initial_attribute_values(self, create_controller: Controller) -> None:
        """Test checking the initial attribute values of the Controller"""
        assert create_controller.coffee_machine.is_on
        assert create_controller.coffee_machine.water_level > 0
        assert create_controller.coffee_machine.milk_level > 0
        assert create_controller.coffee_machine.coffee_beans_level > 0
        assert create_controller.view
        assert not create_controller.play


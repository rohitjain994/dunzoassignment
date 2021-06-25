# -*- coding: utf-8 -*-

"""
src.controllers.controller
~~~~~~~~~~~~~~~~~~~
This script contains the Controller class being in control of the CoffeeMachine's actions.
"""
from src.exceptions import NotEnoughCoffeeBeans
from src.exceptions import NotEnoughMilk
from src.exceptions import NotEnoughWater
from src.exceptions import TurnedOff
from src.models.coffee_machine import CoffeeMachine
from src.views import view
from src.utils import Mililiters


class Controller:

    def __init__(
            self,
            coffee_machine_water_container_capacity: Mililiters = 500,
            coffee_machine_milk_container_capacity: Mililiters = 200,
            coffee_machine_coffee_beans_container_capacity: Mililiters = 100) -> None:
        self.play = False
        self.coffee_machine = CoffeeMachine(
            water_container_capacity=coffee_machine_water_container_capacity,
            milk_container_capacity=coffee_machine_milk_container_capacity,
            coffee_beans_container_capacity=coffee_machine_coffee_beans_container_capacity
        )
        self.coffee_machine.refill_water()
        self.coffee_machine.refill_milk()
        self.coffee_machine.refill_coffee_beans()
        self.coffee_machine.turn_on()
        self.view = view

    def run(self) -> None:
        self.play = True
        while self.play:
            self.present_coffee_machine()
            self.get_user_action()

    def present_coffee_machine(self) -> None:
        view.present_coffee_machine(
            water_container_fill_level=self.coffee_machine.water_level,
            milk_container_fill_level=self.coffee_machine.milk_level,
            coffee_beans_container_fill_level=self.coffee_machine.coffee_beans_level,
            is_on=self.coffee_machine.is_on
        )

    def get_user_action(self) -> None:
        choice: str = self.view.prompt_user_with_possible_actions(
            coffee_machine_is_on=self.coffee_machine.is_on
        )
        if 'turn the coffee machine' in choice:
            self.coffee_machine.turn_on() if 'ON' in choice else self.coffee_machine.turn_off()
        elif 'coffee' in choice:
            _, serving, *_ = choice.split(' ')  # as in 'drink large coffee with milk'
            with_milk = 'with milk' in choice
            self.prepare_coffee(serving=serving, with_milk=with_milk)
        elif choice == 'go away':
            self.play = False
        elif choice == 'refill water':
            self.coffee_machine.refill_water()
        elif choice == 'refill milk':
            self.coffee_machine.refill_milk()
        elif choice == 'refill coffee beans':
            self.coffee_machine.refill_coffee_beans()

    def prepare_coffee(self, serving: str, with_milk: bool) -> None:
        try:
            coffee = self.coffee_machine.prepare_coffee(serving=serving, with_milk=with_milk)
        except NotEnoughWater:
            self.view.show_error('Not enough water! Refill the water container!')
        except NotEnoughMilk:
            self.view.show_error('Not enough milk! Refill the milk container!')
        except NotEnoughCoffeeBeans:
            self.view.show_error('Not enough coffee beans! Refill the coffee beans container!')
        except TurnedOff:
            self.view.show_error('Coffee machine is turned off. Turn it on to make beverage!')
        else:
            self.view.present_coffee(milk=coffee.milk, volume=coffee.volume)

# -*- coding: utf-8 -*-

"""
src.views.view
~~~~~~~~~~~~~~~~~~~
This script contains the main and only view of the application.
It is implemented as a CLI; it requires Click module.
"""

import click

from src.utils import Mililiters
from src.utils import Grams


def present_coffee_machine(water_container_fill_level: Mililiters,
                           milk_container_fill_level: Mililiters,
                           coffee_beans_container_fill_level: Grams,
                           is_on: bool) -> None:
    print(f'''
    ---===---
    CoffeeMachine with: 
        - WaterContainer ({water_container_fill_level} ml) 
        - MilkContainer ({milk_container_fill_level} ml)
        - CoffeeBeansContainer({coffee_beans_container_fill_level} g)
    Turned {"ON" if is_on else "OFF"}
    ---===---
    ''')


def prompt_user_with_possible_actions(coffee_machine_is_on: bool = False) -> str:
    choice = click.prompt(
        'What would you like to do now?', 
        type=click.Choice([
            f'turn the coffee machine {"OFF" if coffee_machine_is_on else "ON"}',
            'drink small coffee',
            'drink medium coffee',
            'drink large coffee',
            'drink small coffee with milk',
            'drink medium coffee with milk',
            'drink large coffee with milk',
            'refill water',
            'refill milk',
            'refill coffee beans',
            'go away'
        ], case_sensitive=False))
    return choice


def present_coffee(volume: Mililiters, milk: Mililiters) -> None:
    click.echo(f'''
    Yes! {volume}ml Coffee{" with milk" if milk else ""} is ready!''')


def show_error(text: str) -> None:
    click.echo(f'''
    No, no, no - {text}''')

import random

def roll_die():
    """Rolls a 6-sided die and returns the result."""
    return random.randint(1, 6)

def roll_multiple_dice(quantity):
    """Rolls several 6-sided dice and returns a list with the results."""
    return [roll_die() for _ in range(quantity)]

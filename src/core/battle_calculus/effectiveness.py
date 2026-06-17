def get_effectiveness(attacker_type, defender_type):
    """
    Returns the effectiveness multiplier of an attack based on the attacker's type and the defender's type.

    Parameters:
    attacker_type (str): The type of the attacking Pokémon.
    defender_type (str): The type of the defending Pokémon.

    Returns:
    float: The effectiveness multiplier (e.g., 0.5 for not very effective, 1 for normal, 2 for super effective).
    """
    # Define a type effectiveness chart

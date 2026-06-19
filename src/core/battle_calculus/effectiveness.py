import json


def load_type_chart(generation: int) -> dict:
    filename = f"data/type_charts/gen{generation}.json"
    with open(filename) as f:
        return json.load(f)


def get_effectiveness(attack_type, defender_type1, defender_type2=None):
    """
    Returns the effectiveness multiplier of an attack based on the attacker's type and the defender's type.

    Parameters:
    attack_type (str): The type of the attacking Pokémon.
    defender_type1 (str): The first type of the defending Pokémon.
    defender_type2 (str, optional): The second type of the defending Pokémon.

    Returns:
    float: The effectiveness multiplier (e.g., 0.5 for not very effective, 1 for normal, 2 for super effective).
    """
    # Load the type chart for the current generation
    type_chart = load_type_chart(generation=1)  # Assuming generation 1 for this example

    # Get the effectiveness multiplier from the type chart
    effectiveness = type_chart.get(attack_type, {}).get(defender_type1, 1.0)

    if defender_type2:
        effectiveness *= type_chart.get(attack_type, {}).get(defender_type2, 1.0)

    return effectiveness

import random
from dataclasses import dataclass
from enum import IntEnum

from src.models.move import BattleMove
from src.models.pokemon import BattlePokemon
from src.models.status import StatusKind


class Priority(IntEnum):
    """
    Gen 1 only has two relevant priority tiers for player moves.
    """

    NORMAL = 0
    HIGH = 1  # Quick Attack


HIGH_PRIORITY_MOVES = {"quick attack", "counter"}

PARALYSIS_SPEED_MULTIPLIER = 0.25


@dataclass
class TurnOrder:
    """Result of determine_turn_order() — who moves first and why."""

    first: BattlePokemon
    second: BattlePokemon
    first_move: BattleMove
    second_move: BattleMove
    tied: bool = False  # True if the same speed forced a random pick
    priority_decided: bool = False  # True if priority difference decided order


def get_move_priority(battle_move: BattleMove) -> Priority:
    """Returns the Gen 1 priority tier of a move."""
    name = battle_move.move.name.lower()
    if name in HIGH_PRIORITY_MOVES:
        return Priority.HIGH
    return Priority.NORMAL


def effective_speed(pokemon: BattlePokemon, is_paralysed: bool) -> int:
    """
    Returns the effective speed used for turn order comparison.

    In Gen 1, paralysis reduces speed to 25% of the Pokémon's current
    speed stat (floor division, matching the game's integer arithmetic).
    """
    base = pokemon.pokemon.speed
    if is_paralysed:
        return int(base * PARALYSIS_SPEED_MULTIPLIER)
    return base


def is_paralysed(pokemon: BattlePokemon) -> bool:
    """
    Checks whether a BattlePokemon has an active paralysis status.
    The caller is expected to pass the full BattlePokemon with statuses
    loaded; this is a pure helper that avoids a DB call.
    """
    return any(s.kind == StatusKind.PARALYSIS for s in pokemon.statuses)


def determine_turn_order(
    pokemon_a: BattlePokemon,
    move_a: BattleMove,
    pokemon_b: BattlePokemon,
    move_b: BattleMove,
    *,
    paralysed_a: bool = False,
    paralysed_b: bool = False,
    random_on_tie: bool = True,
) -> TurnOrder:
    """
    Determines which Pokémon moves first this turn under Gen 1 rules.

    Resolution order:
      1. Higher priority bracket moves first.
      2. Within the same bracket, higher effective speed moves first.
      3. Equal effective speed → random (coin flip), same as the game.

    Parameters
    ----------
    pokemon_a, move_a : first combatant and their chosen move
    pokemon_b, move_b : second combatant and their chosen move
    paralysed_a       : whether pokemon_a is paralysed this turn
    paralysed_b       : whether pokemon_b is paralysed this turn
    random_on_tie     : if False, always picks pokemon_a on a tie (useful
                        for deterministic tests that don't want to mock random)
    """
    priority_a = get_move_priority(move_a)
    priority_b = get_move_priority(move_b)

    # --- Step 1: priority bracket ---
    if priority_a != priority_b:
        if priority_a > priority_b:
            return TurnOrder(
                first=pokemon_a,
                second=pokemon_b,
                first_move=move_a,
                second_move=move_b,
                priority_decided=True,
            )
        else:
            return TurnOrder(
                first=pokemon_b,
                second=pokemon_a,
                first_move=move_b,
                second_move=move_a,
                priority_decided=True,
            )

    # --- Step 2: effective speed within same priority ---
    speed_a = effective_speed(pokemon_a, paralysed_a)
    speed_b = effective_speed(pokemon_b, paralysed_b)

    if speed_a != speed_b:
        if speed_a > speed_b:
            return TurnOrder(
                first=pokemon_a,
                second=pokemon_b,
                first_move=move_a,
                second_move=move_b,
            )
        else:
            return TurnOrder(
                first=pokemon_b,
                second=pokemon_a,
                first_move=move_b,
                second_move=move_a,
            )

    # --- Step 3: speed tie → random ---
    if random_on_tie:
        a_goes_first = random.choice([True, False])
    else:
        a_goes_first = True  # deterministic fallback for tests

    if a_goes_first:
        return TurnOrder(
            first=pokemon_a,
            second=pokemon_b,
            first_move=move_a,
            second_move=move_b,
            tied=True,
        )
    return TurnOrder(
        first=pokemon_b,
        second=pokemon_a,
        first_move=move_b,
        second_move=move_a,
        tied=True,
    )

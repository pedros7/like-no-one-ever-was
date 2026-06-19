import random
from unittest.mock import patch

import pytest

from src.models.move import BattleMove
from src.models.pokemon import BattlePokemon
from core.battle_calculus.order_of_attack import (
    PARALYSIS_SPEED_MULTIPLIER,
    Priority,
    TurnOrder,
    determine_turn_order,
    effective_speed,
    get_move_priority,
)
from models import Move, Pokemon

# ---------------------------------------------------------------------------
# Factories — build minimal objects without a DB session
# ---------------------------------------------------------------------------


def make_pokemon(name: str, speed: int) -> BattlePokemon:
    """Creates a BattlePokemon with a fixed speed stat and no active statuses."""
    mon = Pokemon(
        id=None,
        name=name,
        species=name.lower(),
        level=50,
        hp=100,
        attack=80,
        defense=70,
        sp_attack=80,
        sp_defense=70,
        speed=speed,
    )
    battler = BattlePokemon(
        id=None,
        pokemon_id=1,
        battle_id=1,
        team=0,
        current_hp=100,
        fainted=False,
    )
    battler.pokemon = mon
    battler.statuses = []
    return battler


def make_battle_move(move_name: str, power: int = 80) -> BattleMove:
    """Creates a BattleMove wrapping a Move with the given name."""
    move = Move(
        id=None,
        name=move_name,
        type="normal",
        contact=True,
        max_pp=15,
        power=power,
        accuracy=100,
    )
    bm = BattleMove(
        id=None,
        battle_pokemon_id=1,
        move_id=1,
        slot=1,
        current_pp=15,
        max_pp=15,
    )
    bm.move = move
    return bm


# ---------------------------------------------------------------------------
# get_move_priority
# ---------------------------------------------------------------------------


class TestGetMovePriority:
    def test_normal_move_is_priority_0(self):
        bm = make_battle_move("tackle")
        assert get_move_priority(bm) == Priority.NORMAL

    def test_quick_attack_is_priority_1(self):
        bm = make_battle_move("quick attack")
        assert get_move_priority(bm) == Priority.HIGH

    def test_counter_is_priority_1_in_gen1(self):
        """Counter is +1 priority in Gen 1, unlike later gens."""
        bm = make_battle_move("counter")
        assert get_move_priority(bm) == Priority.HIGH

    def test_thunderbolt_is_priority_0(self):
        bm = make_battle_move("thunderbolt")
        assert get_move_priority(bm) == Priority.NORMAL

    def test_move_name_is_case_insensitive(self):
        bm = make_battle_move("Quick Attack")
        assert get_move_priority(bm) == Priority.HIGH


# ---------------------------------------------------------------------------
# effective_speed
# ---------------------------------------------------------------------------


class TestEffectiveSpeed:
    def test_no_paralysis_returns_base_speed(self):
        mon = make_pokemon("pikachu", speed=110)
        assert effective_speed(mon, is_paralysed=False) == 110

    def test_paralysis_reduces_speed_to_25_percent(self):
        """Gen 1: paralysis = 75% speed cut → effective speed is 25% of stat."""
        mon = make_pokemon("pikachu", speed=110)
        assert effective_speed(mon, is_paralysed=True) == int(110 * 0.25)

    def test_paralysis_uses_floor_division(self):
        """Speed values that don't divide evenly should floor, not round."""
        mon = make_pokemon("rhydon", speed=40)
        assert effective_speed(mon, is_paralysed=True) == int(40 * 0.25)  # 10

    def test_paralysis_multiplier_constant_is_correct(self):
        assert PARALYSIS_SPEED_MULTIPLIER == 0.25


# ---------------------------------------------------------------------------
# Priority decides order
# ---------------------------------------------------------------------------


class TestPriorityOrder:
    def test_quick_attack_beats_slower_normal_move(self):
        """Quick Attack (+1) goes before Tackle (0) regardless of speed."""
        fast = make_pokemon("tauros", speed=110)
        slow = make_pokemon("snorlax", speed=30)
        quick = make_battle_move("quick attack")
        tackle = make_battle_move("tackle")

        # Snorlax is slower but uses Quick Attack — should go first
        result = determine_turn_order(slow, quick, fast, tackle)

        assert result.first is slow
        assert result.second is fast
        assert result.priority_decided is True
        assert result.tied is False

    def test_quick_attack_beats_faster_normal_move(self):
        """Priority ignores speed completely — even a faster foe loses to +1."""
        slow = make_pokemon("slowbro", speed=30)
        fast = make_pokemon("jolteon", speed=130)
        quick = make_battle_move("quick attack")
        surf = make_battle_move("surf")

        result = determine_turn_order(slow, quick, fast, surf)

        assert result.first is slow
        assert result.priority_decided is True

    def test_both_quick_attack_falls_back_to_speed(self):
        """Same priority tier → speed decides. priority_decided must be False."""
        fast = make_pokemon("jolteon", speed=130)
        slow = make_pokemon("slowbro", speed=30)
        quick_a = make_battle_move("quick attack")
        quick_b = make_battle_move("quick attack")

        result = determine_turn_order(fast, quick_a, slow, quick_b)

        assert result.first is fast
        assert result.priority_decided is False

    def test_counter_priority_beats_normal_move(self):
        """Counter is +1 priority in Gen 1."""
        slow = make_pokemon("chansey", speed=50)
        fast = make_pokemon("tauros", speed=110)
        counter = make_battle_move("counter")
        body_slam = make_battle_move("body slam")

        result = determine_turn_order(slow, counter, fast, body_slam)

        assert result.first is slow
        assert result.priority_decided is True


# ---------------------------------------------------------------------------
# Speed decides order (same priority)
# ---------------------------------------------------------------------------


class TestSpeedOrder:
    def test_faster_pokemon_goes_first(self):
        fast = make_pokemon("jolteon", speed=130)
        slow = make_pokemon("snorlax", speed=30)
        move_a = make_battle_move("thunderbolt")
        move_b = make_battle_move("body slam")

        result = determine_turn_order(fast, move_a, slow, move_b)

        assert result.first is fast
        assert result.second is slow
        assert result.priority_decided is False
        assert result.tied is False

    def test_order_is_symmetric(self):
        """Passing args in reverse should flip first/second."""
        fast = make_pokemon("jolteon", speed=130)
        slow = make_pokemon("snorlax", speed=30)
        move_a = make_battle_move("thunderbolt")
        move_b = make_battle_move("body slam")

        result = determine_turn_order(slow, move_b, fast, move_a)

        assert result.first is fast
        assert result.second is slow

    def test_correct_moves_are_paired_with_correct_pokemon(self):
        fast = make_pokemon("electrode", speed=140)
        slow = make_pokemon("onix", speed=70)
        move_fast = make_battle_move("thunder")
        move_slow = make_battle_move("rock throw")

        result = determine_turn_order(fast, move_fast, slow, move_slow)

        assert result.first_move is move_fast
        assert result.second_move is move_slow


# ---------------------------------------------------------------------------
# Paralysis speed reduction
# ---------------------------------------------------------------------------


class TestParalysisOrder:
    def test_paralysis_can_flip_turn_order(self):
        """
        Faster Pokémon paralysed: effective speed drops to 25%.
        If the slower foe is faster than that reduced value, foe goes first.
        Jolteon 130 → paralysed → 32. Slowbro 80 > 32, so Slowbro goes first.
        """
        jolteon = make_pokemon("jolteon", speed=130)
        slowbro = make_pokemon("slowbro", speed=80)
        move_a = make_battle_move("thunderbolt")
        move_b = make_battle_move("psychic")

        result = determine_turn_order(
            jolteon,
            move_a,
            slowbro,
            move_b,
            paralysed_a=True,
        )

        assert result.first is slowbro
        assert result.second is jolteon

    def test_paralysis_does_not_flip_if_still_faster(self):
        """
        Mewtwo (130 speed) paralysed → effective 32.
        Geodude (40 speed) is still slower than 32 — Mewtwo still goes first.
        """
        mewtwo = make_pokemon("mewtwo", speed=130)
        geodude = make_pokemon("geodude", speed=20)
        move_a = make_battle_move("psychic")
        move_b = make_battle_move("tackle")

        result = determine_turn_order(
            mewtwo,
            move_a,
            geodude,
            move_b,
            paralysed_a=True,
        )

        assert result.first is mewtwo

    def test_both_paralysed_faster_base_still_wins(self):
        """Both paralysed: effective speeds are both at 25%, ratio preserved."""
        fast = make_pokemon("jolteon", speed=130)
        slow = make_pokemon("vaporeon", speed=65)
        move_a = make_battle_move("thunderbolt")
        move_b = make_battle_move("surf")

        result = determine_turn_order(
            fast,
            move_a,
            slow,
            move_b,
            paralysed_a=True,
            paralysed_b=True,
        )

        assert result.first is fast

    def test_both_paralysed_can_tie(self):
        """Both at the same base speed + paralysis → effective speeds are equal → tie."""
        mon_a = make_pokemon("clefable", speed=60)
        mon_b = make_pokemon("wigglytuff", speed=60)
        move_a = make_battle_move("body slam")
        move_b = make_battle_move("body slam")

        result = determine_turn_order(
            mon_a,
            move_a,
            mon_b,
            move_b,
            paralysed_a=True,
            paralysed_b=True,
            random_on_tie=False,
        )

        assert result.tied is True


# ---------------------------------------------------------------------------
# Speed ties
# ---------------------------------------------------------------------------


class TestSpeedTie:
    def test_equal_speed_sets_tied_flag(self):
        mon_a = make_pokemon("persian", speed=115)
        mon_b = make_pokemon("electrode", speed=115)
        move_a = make_battle_move("slash")
        move_b = make_battle_move("thunder")

        result = determine_turn_order(
            mon_a,
            move_a,
            mon_b,
            move_b,
            random_on_tie=False,
        )

        assert result.tied is True

    def test_tie_produces_valid_order(self):
        """Even on a tie the result must have both Pokémon in first/second."""
        mon_a = make_pokemon("persian", speed=115)
        mon_b = make_pokemon("electrode", speed=115)
        move_a = make_battle_move("slash")
        move_b = make_battle_move("thunder")

        result = determine_turn_order(
            mon_a,
            move_a,
            mon_b,
            move_b,
            random_on_tie=False,
        )

        assert result.first in (mon_a, mon_b)
        assert result.second in (mon_a, mon_b)
        assert result.first is not result.second

    def test_tie_is_random_over_many_samples(self):
        """
        Over enough trials both outcomes should appear.
        The probability of one side winning all 50 flips is (0.5)^50 ≈ 10^-15.
        """
        mon_a = make_pokemon("persian", speed=115)
        mon_b = make_pokemon("electrode", speed=115)
        move_a = make_battle_move("slash")
        move_b = make_battle_move("thunder")

        firsts = set()
        for _ in range(50):
            result = determine_turn_order(mon_a, move_a, mon_b, move_b)
            firsts.add(id(result.first))

        assert (
            len(firsts) == 2
        ), "Expected both Pokémon to go first at least once in 50 trials"

    def test_unequal_speed_does_not_set_tied_flag(self):
        fast = make_pokemon("jolteon", speed=130)
        slow = make_pokemon("snorlax", speed=30)
        move_a = make_battle_move("thunderbolt")
        move_b = make_battle_move("body slam")

        result = determine_turn_order(fast, move_a, slow, move_b)

        assert result.tied is False

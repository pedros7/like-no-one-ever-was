import pytest
from src.core.battle_calculus.effectiveness import get_effectiveness


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def assert_effectiveness(atk, def1, expected_multiplier, def2=None):
    """Thin wrapper so failures print a readable label."""
    result = get_effectiveness(atk, def1, def2)
    assert result == expected_multiplier, (
        f"{atk} → {def1}{f'/{def2}' if def2 else ''}: "
        f"expected {expected_multiplier}, got {result}"
    )


# ---------------------------------------------------------------------------
# Single-type: Neutral damage result
# ---------------------------------------------------------------------------
class TestsNeutralDamage:
    """Tests for single-type Pokémon where the attack is neutral"""

    def test_normal_vs_normal(self):
        assert_effectiveness("normal", "normal", 1.0)

    def test_fire_vs_electric(self):
        assert_effectiveness("fire", "electric", 1.0)

    def test_water_vs_ghost(self):
        assert_effectiveness("water", "ghost", 1.0)

    def test_grass_vs_psychic(self):
        assert_effectiveness("grass", "psychic", 1.0)


# ---------------------------------------------------------------------------
# Single-type: Not very effective (0.5x)
# ---------------------------------------------------------------------------
class TestNotVeryEffective:
    def test_fire_vs_fire(self):
        assert_effectiveness("fire", "fire", 0.5)

    def test_water_vs_grass(self):
        assert_effectiveness("water", "grass", 0.5)

    def test_electric_vs_grass(self):
        assert_effectiveness("electric", "grass", 0.5)

    def test_grass_vs_fire(self):
        assert_effectiveness("grass", "fire", 0.5)


# ---------------------------------------------------------------------------
# Single-type: Very effective (2x)
# ---------------------------------------------------------------------------
class TestVeryEffective:
    def test_fire_vs_grass(self):
        assert_effectiveness("fire", "grass", 2.0)

    def test_water_vs_fire(self):
        assert_effectiveness("water", "fire", 2.0)

    def test_electric_vs_water(self):
        assert_effectiveness("electric", "water", 2.0)

    def test_grass_vs_water(self):
        assert_effectiveness("grass", "water", 2.0)


# ---------------------------------------------------------------------------
# Single-type: immune (0x)
# ---------------------------------------------------------------------------
class TestImmune:
    def test_normal_vs_ghost(self):
        """Normal cannot hit Ghost."""
        assert_effectiveness("normal", "ghost", 0.0)

    def test_electric_vs_ground(self):
        """Electric cannot hit Ground."""
        assert_effectiveness("electric", "ground", 0.0)

    def test_fighting_vs_ghost(self):
        """Fighting cannot hit Ghost."""
        assert_effectiveness("fighting", "ghost", 0.0)

    def test_ground_vs_flying(self):
        """Ground cannot hit Flying."""
        assert_effectiveness("ground", "flying", 0.0)


# ---------------------------------------------------------------------------
# Dual-type: Double not very effective (0.25x)
# ---------------------------------------------------------------------------
class TestDualDoubleNotVeryEffective:
    def test_fire_vs_fire_rock(self):
        assert_effectiveness("fire", "fire", 0.25, "rock")

    def test_water_vs_water_grass(self):
        assert_effectiveness("water", "water", 0.25, "grass")


# ---------------------------------------------------------------------------
# Dual-type: Not very effective (0.5x)
# ---------------------------------------------------------------------------
class TestDualNotVeryEffective:
    def test_fire_vs_fire_flying(self):
        assert_effectiveness("fire", "fire", 0.5, "flying")

    def test_fire_vs_water_psychic(self):
        assert_effectiveness("fire", "water", 0.5, "psychic")

    def test_electric_vs_grass_poison(self):
        assert_effectiveness("electric", "grass", 0.5, "poison")

    def test_grass_vs_fire_ghost(self):
        assert_effectiveness("grass", "fire", 0.5, "ghost")


# ---------------------------------------------------------------------------
# Dual-type: neutral from cancelling multipliers (1x)
# ---------------------------------------------------------------------------
class TestDualNeutralFromCancelling:
    def test_fire_vs_grass_water(self):
        assert_effectiveness("fire", "grass", 1.0, "water")

    def test_water_vs_fire_grass(self):
        assert_effectiveness("water", "fire", 1.0, "grass")

    def test_electric_vs_water_grass(self):
        assert_effectiveness("electric", "water", 1.0, "grass")

    def test_ice_vs_water_dragon(self):
        assert_effectiveness("ice", "water", 1.0, "dragon")


# ---------------------------------------------------------------------------
# Dual-type: immune overrides super effective (0x)
# ---------------------------------------------------------------------------
class TestDualImmuneOverride:
    def test_normal_vs_ghost_fighting(self):
        assert_effectiveness("normal", "ghost", 0.0, "fighting")

    def test_electric_vs_ground_flying(self):
        assert_effectiveness("electric", "ground", 0.0, "flying")

    def test_fighting_vs_ghost_normal(self):
        assert_effectiveness("fighting", "ghost", 0.0, "normal")

    def test_ground_vs_flying_fire(self):
        assert_effectiveness("ground", "flying", 0.0, "fire")


# ---------------------------------------------------------------------------
# Dual-type: Double very effective (4x)
# ---------------------------------------------------------------------------
class TestDualDoubleVeryEffective:
    def test_fire_vs_grass_bug(self):
        assert_effectiveness("fire", "grass", 4.0, "bug")

    def test_electric_vs_water_flying(self):
        assert_effectiveness("electric", "water", 4.0, "flying")

    def test_grass_vs_water_ground(self):
        assert_effectiveness("grass", "water", 4.0, "ground")

    def test_water_vs_ground_rock(self):
        assert_effectiveness("water", "ground", 4.0, "rock")


# ---------------------------------------------------------------------------
# Gen 1 bugs
# ---------------------------------------------------------------------------
class TestGen1Bugs:
    def test_ghost_vs_psychic_is_immune_not_super_effective(self):
        """
        BUG 1: Ghost → Psychic is 0x in actual Gen 1 code.
        Every game guide claimed 2x, and the Saffron City NPC says
        'Psychic-types only fear Ghosts and Bugs!' — the code disagrees.
        Fixed to 2x in Gen 2.
        """
        assert_effectiveness("ghost", "psychic", 0.0)

    def test_bug_vs_poison_is_super_effective(self):
        """
        BUG 2: Bug → Poison is 2x in Gen 1.
        Fixed to 0.5x in Gen 2.
        """
        assert_effectiveness("bug", "poison", 2.0)

    def test_poison_vs_bug_is_super_effective(self):
        """
        BUG 3: Poison → Bug is 2x in Gen 1, creating a mutually
        super-effective pair — unique in franchise history.
        Fixed to 1x in Gen 2.
        """
        assert_effectiveness("poison", "bug", 2.0)

    def test_ice_vs_fire_is_neutral(self):
        """
        BUG 4: Ice → Fire is 1x in Gen 1. Should logically be 0.5x
        (fire resisting ice makes sense) and was corrected to 0.5x in Gen 2.
        """
        assert_effectiveness("ice", "fire", 1.0)

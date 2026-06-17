from enum import Enum

from sqlmodel import Field, SQLModel


class StatusKind(str, Enum):
    BURN = "burn"
    PARALYSIS = "paralysis"
    POISON = "poison"
    BADLY_POISONED = "badly_poisoned"
    SLEEP = "sleep"
    FREEZE = "freeze"
    CONFUSION = "confusion"
    FLINCH = "flinch"


# Non-volatile statuses: only one can apply at a time, persists across switches
NON_VOLATILE = {
    StatusKind.BURN,
    StatusKind.PARALYSIS,
    StatusKind.POISON,
    StatusKind.BADLY_POISONED,
    StatusKind.SLEEP,
    StatusKind.FREEZE,
}

# Volatile statuses: cleared on switch-out, multiple can stack
VOLATILE = {
    StatusKind.CONFUSION,
    StatusKind.FLINCH,
}


class BattleStatus(SQLModel, table=True):
    """An active status instance applied to a Pokémon in a battle."""

    id: int | None = Field(default=None, primary_key=True)

    battle_pokemon_id: int = Field(foreign_key="battlepokemon.id")
    kind: StatusKind

    turns_remaining: int | None = None  # e.g. sleep duration
    counter: int = 0  # e.g. badly poisoned's increasing damage counter

    @property
    def is_volatile(self) -> bool:
        return self.kind in VOLATILE

    def tick(self) -> None:
        if self.turns_remaining is not None:
            self.turns_remaining = max(0, self.turns_remaining - 1)

    @property
    def expired(self) -> bool:
        return self.turns_remaining == 0

from sqlmodel import Field, SQLModel, Relationship


class Move(SQLModel, table=True):
    """Static move data — the 'dex' definition of a move."""

    id: int | None = Field(default=None, primary_key=True)
    name: str
    type: str
    contact: bool

    pp: int
    power: int | None = None
    accuracy: int | None = None


class Moveset(SQLModel, table=True):
    """Which moves a Pokémon knows (the 'loadout'), not runtime state."""

    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)

    move1_id: int = Field(foreign_key="move.id")
    move2_id: int | None = Field(default=None, foreign_key="move.id")
    move3_id: int | None = Field(default=None, foreign_key="move.id")
    move4_id: int | None = Field(default=None, foreign_key="move.id")


class BattleMove(SQLModel, table=True):
    """
    Runtime state for a single move slot during a battle.
    One row per (battle participant, slot), tracking current PP,
    PP-ups applied, disabled status, etc.
    """

    id: int | None = Field(default=None, primary_key=True)

    battle_pokemon_id: int = Field(foreign_key="battlepokemon.id")
    move_id: int = Field(foreign_key="move.id")
    slot: int

    current_pp: int
    max_pp: int  # max_pp + any pp-ups, copied in at battle start
    disabled: bool = False  # e.g. from Disable / Taunt / Torment effects

    move: Move = Relationship()

    def use(self) -> None:
        if self.current_pp <= 0:
            raise ValueError(f"{self.move.name} has no PP left")
        self.current_pp -= 1

    @property
    def is_depleted(self) -> bool:
        return self.current_pp <= 0

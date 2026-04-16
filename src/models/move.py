from sqlmodel import Field, SQLModel


class Move(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    type: str

    pp: int
    power: int | None = None
    accuracy: int | None = None


class Moveset(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)

    move1_id: int = Field(foreign_key="move.id")
    move2_id: int | None = Field(default=None, foreign_key="move.id")
    move3_id: int | None = Field(default=None, foreign_key="move.id")
    move4_id: int | None = Field(default=None, foreign_key="move.id")

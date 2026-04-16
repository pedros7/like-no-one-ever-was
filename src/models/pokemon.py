from sqlmodel import Field, SQLModel


class Pokemon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class PokemonStats(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)

    # Typing
    type1: str
    type2: str | None

    # Stats
    hp: int
    attack: int
    defense: int
    speed: int
    special: int

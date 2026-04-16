from sqlmodel import Field, SQLModel


class PokemonMoveset(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)

    move1_id: int = Field(foreign_key="move.id")
    move2_id: int = Field(foreign_key="move.id")
    move3_id: int = Field(foreign_key="move.id")
    move4_id: int = Field(foreign_key="move.id")

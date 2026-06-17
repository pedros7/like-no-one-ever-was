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


class BattlePokemon:
    def __init__(
        self, name, hp, attack, defense, speed, special, type1, type2=None, moves=None
    ):
        self.name = name
        self.type1 = type1
        self.type2 = type2

        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.special = special

        self.moves = moves or []

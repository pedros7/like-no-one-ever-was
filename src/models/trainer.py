from sqlmodel import Field, SQLModel
from src.models.pokemon import BattlePokemon


class Trainer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class TrainerPokemon(SQLModel, table=True):
    trainer_id: int = Field(foreign_key="trainer.id", primary_key=True)
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)

    slot: int


class BattleTrainer:
    def __init__(self, name, team: list[BattlePokemon]):
        self.name = name
        self.team = team

from sqlmodel import Field, SQLModel


class Move(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    type: str

    pp: int
    power: int | None = None
    accuracy: int | None = None

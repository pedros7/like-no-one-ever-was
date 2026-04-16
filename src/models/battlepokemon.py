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

from enum import IntEnum
from typing import NamedTuple, Optional


class FillerType(IntEnum):
    Hero = 0
    Villain = 1
    Other = 2


class FillerData(NamedTuple):
    name: str
    type: FillerType
    name_pos: Optional[str] = None
    name_neg: Optional[str] = None


filler = [
    FillerData("StartHandsize", FillerType.Hero, "Starting Handsize +1", "Starting Handsize -1"),
    FillerData("HeroHp", FillerType.Hero, "Hero Toughness 1", "Hero Fragility 1"),
    FillerData("Mulligan", FillerType.Hero, name_pos="1 Mulligan"),
    FillerData("HeroDamageDealt", FillerType.Hero, "Hero [TYPE]Strength 1", "Hero [TYPE]Weakness 1"),
    FillerData("HeroDamageTaken", FillerType.Hero,
               "Hero [TYPE]Fortification 1", "Hero [TYPE]Vulnerability 1"),
    FillerData("HeroCardPlay", FillerType.Hero, "Haste 1", "Slowness 1"),
    FillerData("HeroPower", FillerType.Hero, "Power use +1", "Power use -1"),
    FillerData("HeroCardDraw", FillerType.Hero, "Ingenuity 1", "Stupidity 1"),
    FillerData("VillainHp", FillerType.Villain, "Villain Fragility 1", "Villain Toughness 1"),
    FillerData("VillainDamageDealt", FillerType.Villain,
               "Villain [TYPE]Weakness 1", "Villain [TYPE]Strength 1"),
    FillerData("VillainDamageTaken", FillerType.Villain,
               "Villain [TYPE]Vulnerability 1", "Villain [TYPE]Fortification 1"),
    FillerData("VillainCardPlays", FillerType.Villain, "Horde -1", "Horde +1"),
    FillerData("VillainStartCardPlays", FillerType.Villain, name_neg="Rapid Deployment 1"),
    FillerData("HeroCannotPlay", FillerType.Other, name_neg="Slowing Assault 1"),
    FillerData("HeroCannotPower", FillerType.Other, name_neg="Power Assault 1"),
    FillerData("HeroCannotDraw", FillerType.Other, name_neg="Mental Assault 1"),
    FillerData("HeroCannotDamage", FillerType.Other, name_neg="Weakening Assault 1"),
    FillerData("Scion", FillerType.Other, name_pos="Scion of Oblivaeon")
]

damage_types = [
    "",
    "Cold ",
    "Energy ",
    "Fire ",
    "Infernal ",
    "Lightning ",
    "Melee ",
    "Projectile ",
    "Psychic ",
    "Radiant ",
    "Sonic ",
    "Toxic ",
]

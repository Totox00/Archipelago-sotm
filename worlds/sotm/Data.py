from enum import IntEnum
from itertools import groupby
from typing import NamedTuple, Callable, Set, Optional

from BaseClasses import CollectionState


class SotmState:
    items: Set[str]

    def __init__(self):
        self.items = set()

    def has(self, item: str, _player: int, _count: int = 1) -> bool:
        return item in self.items


class SotmCategory(IntEnum):
    Scion = 0
    Hero = 1
    Villain = 2
    TeamVillain = 3
    Environment = 4
    Variant = 5
    VillainVariant = 6
    Filler = 7


class SotmSource(IntEnum):
    RookCity = 0
    InfernalRelics = 1
    ShatteredTimelines = 2
    WrathOfTheCosmos = 3
    Vengeance = 4
    VillainsOfTheMultiverse = 5
    Oblivaeon = 6
    Unity = 7
    TheScholar = 8
    Guise = 9
    Stuntman = 10
    Benchmark = 11
    TheVoidGuard = 12
    Ambuscade = 13
    MissInformation = 14
    WagerMaster = 15
    Chokepoint = 16
    SilverGulch1883 = 17
    TheFinalWasteland = 18
    OmnitronIV = 19
    TheCelestialTribunal = 20
    TheCauldron = 21
    CauldronPromos = 22


fanmade_sources = [SotmSource.TheCauldron, SotmSource.CauldronPromos]


def has_fanmade(sources: list[SotmSource]) -> bool:
    return True in (source in fanmade_sources for source in sources)


class SotmData(NamedTuple):
    name: str
    sources: list[SotmSource]
    category: SotmCategory
    base: Optional[str] = None
    rule: Optional[Callable[[CollectionState | SotmState, int], bool]] = None


data = [SotmData(*row) for row in [
    # Villains
    ("Baron Blade", [], SotmCategory.Villain),
    ("Mad Bomber Baron Blade", [], SotmCategory.VillainVariant, "Baron Blade",
     lambda state, player: has_all_of(["Baron Blade", "Citizen Dawn"], state, player)),
    ("Citizen Dawn", [], SotmCategory.Villain),
    ("Grand Warlord Voss", [], SotmCategory.Villain),
    ("Omnitron", [], SotmCategory.Villain),
    ("Omnitron II", [], SotmCategory.VillainVariant, "Omnitron",
     lambda state, player: has_all_of(["Omnitron", "Grand Warlord Voss"], state, player)),
    ("Ambuscade", [SotmSource.Ambuscade], SotmCategory.Villain),
    ("The Chairman", [SotmSource.RookCity], SotmCategory.Villain),
    ("The Matriarch", [SotmSource.RookCity], SotmCategory.Villain),
    ("Plague Rat", [SotmSource.RookCity], SotmCategory.Villain),
    ("Spite", [SotmSource.RookCity], SotmCategory.Villain),
    ("Spite: Agent of Gloom", [SotmSource.RookCity], SotmCategory.VillainVariant, "Spite",
     lambda state, player: has_all_of(["Spite", "Gloomweaver"], state, player)),
    ("Akash'Bhuta", [SotmSource.InfernalRelics], SotmCategory.Villain),
    ("Apostate", [SotmSource.InfernalRelics], SotmCategory.Villain),
    ("The Ennead", [SotmSource.InfernalRelics], SotmCategory.Villain),
    ("Gloomweaver", [SotmSource.InfernalRelics], SotmCategory.Villain),
    ("Skinwalker Gloomweaver", [SotmSource.InfernalRelics], SotmCategory.VillainVariant, "Gloomweaver",
     lambda state, player: has_all_of(["Spite", "Gloomweaver", "Spite: Agent of Gloom", "Rook City"], state, player)),
    ("Miss Information", [SotmSource.MissInformation], SotmCategory.Villain),
    ("La Capitán", [SotmSource.ShatteredTimelines], SotmCategory.Villain),
    ("The Dreamer", [SotmSource.ShatteredTimelines], SotmCategory.Villain),
    ("Iron Legacy", [SotmSource.ShatteredTimelines], SotmCategory.Villain),
    ("Kismet", [SotmSource.ShatteredTimelines], SotmCategory.Villain),
    ("Trickster Kismet", [SotmSource.ShatteredTimelines], SotmCategory.VillainVariant, "Kismet",
     lambda state, player: has_all_of(["Kismet", "The Block"], state, player)
        and any_variants_of(["K.N.Y.F.E.", "Argent Adept", "Fanatic"], state, player)),
    ("Deadline", [SotmSource.WrathOfTheCosmos], SotmCategory.Villain),
    ("Infinitor", [SotmSource.WrathOfTheCosmos], SotmCategory.Villain),
    ("Heroic Infinitor", [SotmSource.WrathOfTheCosmos], SotmCategory.VillainVariant, "Infinitor",
     lambda state, player: any_variants_of(["Infinitor", "Captain Cosmic"], state, player)),
    ("Kaargra Warfang", [SotmSource.WrathOfTheCosmos], SotmCategory.Villain),
    ("Progeny", [SotmSource.WrathOfTheCosmos], SotmCategory.Villain),
    ("Wager Master", [SotmSource.WagerMaster], SotmCategory.Villain),
    ("Chokepoint", [SotmSource.Chokepoint], SotmCategory.Villain),
    ("Anathema", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Evolved Anathema", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Celadroch", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Dendron", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Windcolor Dendron", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Dynamo", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Gray", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("The Infernal Choir", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Menagerie", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("The Mistress of Fate", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Mythos", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Oriphel", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Outlander", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Phase", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("The Ram", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("1929 Ram", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Scream Machine", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Swarm Eater", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Hivemind Swarm Eater", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Tiamat", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Hydra Tiamat", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Tiamat 2199", [SotmSource.TheCauldron], SotmCategory.Villain),
    ("Vector", [SotmSource.TheCauldron], SotmCategory.Villain),
    # Team Villains
    ("Baron Blade (Team)", [SotmSource.Vengeance], SotmCategory.TeamVillain),
    ("Ermine", [SotmSource.Vengeance], SotmCategory.TeamVillain),
    ("Friction", [SotmSource.Vengeance], SotmCategory.TeamVillain),
    ("Fright Train", [SotmSource.Vengeance], SotmCategory.TeamVillain),
    ("Proletariat", [SotmSource.Vengeance], SotmCategory.TeamVillain),
    ("Ambuscade (Team)", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    ("Biomancer", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    ("Bugbear", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    ("La Capitan (Team)", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    ("Citizens Hammer and Anvil", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    ("Greazer", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    ("Miss Information (Team)", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    ("The Operative", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    ("Plague Rat (Team)", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    ("Sergeant Steel", [SotmSource.VillainsOfTheMultiverse], SotmCategory.TeamVillain),
    # Heroes
    ("Absolute Zero", [], SotmCategory.Hero),
    ("Bunker", [], SotmCategory.Hero),
    ("Fanatic", [], SotmCategory.Hero),
    ("Haka", [], SotmCategory.Hero),
    ("Legacy", [], SotmCategory.Hero),
    ("Ra", [], SotmCategory.Hero),
    ("Tachyon", [], SotmCategory.Hero),
    ("Tempest", [], SotmCategory.Hero),
    ("The Visionary", [], SotmCategory.Hero),
    ("Wraith", [], SotmCategory.Hero),
    ("Unity", [SotmSource.Unity], SotmCategory.Hero),
    ("Expatriette", [SotmSource.RookCity], SotmCategory.Hero),
    ("Mister Fixer", [SotmSource.RookCity], SotmCategory.Hero),
    ("Argent Adept", [SotmSource.InfernalRelics], SotmCategory.Hero),
    ("Nightmist", [SotmSource.InfernalRelics], SotmCategory.Hero),
    ("The Scholar", [SotmSource.TheScholar], SotmCategory.Hero),
    ("Chrono-Ranger", [SotmSource.ShatteredTimelines], SotmCategory.Hero),
    ("Omnitron-X", [SotmSource.ShatteredTimelines], SotmCategory.Hero),
    ("Captain Cosmic", [SotmSource.WrathOfTheCosmos], SotmCategory.Hero),
    ("Sky-Scraper", [SotmSource.WrathOfTheCosmos], SotmCategory.Hero),
    ("Guise", [SotmSource.Guise], SotmCategory.Hero),
    ("K.N.Y.F.E.", [SotmSource.Vengeance], SotmCategory.Hero),
    ("The Naturalist", [SotmSource.Vengeance], SotmCategory.Hero),
    ("Parse", [SotmSource.Vengeance], SotmCategory.Hero),
    ("The Sentinels", [SotmSource.Vengeance], SotmCategory.Hero),
    ("Setback", [SotmSource.Vengeance], SotmCategory.Hero),
    ("Benchmark", [SotmSource.Benchmark], SotmCategory.Hero),
    ("Stuntman", [SotmSource.Stuntman], SotmCategory.Hero),
    ("Dr. Medico", [SotmSource.TheVoidGuard], SotmCategory.Hero),
    ("The Idealist", [SotmSource.TheVoidGuard], SotmCategory.Hero),
    ("Mainstay", [SotmSource.TheVoidGuard], SotmCategory.Hero),
    ("Writhe", [SotmSource.TheVoidGuard], SotmCategory.Hero),
    ("Akash'Thriya", [SotmSource.Oblivaeon], SotmCategory.Hero),
    ("La Comodora", [SotmSource.Oblivaeon], SotmCategory.Hero),
    ("The Harpy", [SotmSource.Oblivaeon], SotmCategory.Hero),
    ("Lifeline", [SotmSource.Oblivaeon], SotmCategory.Hero),
    ("Luminary", [SotmSource.Oblivaeon], SotmCategory.Hero),
    ("Baccarat", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("The Cricket", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Cypher", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Doc Havoc", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Drift", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Echelon", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Gargoyle", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Gyrosaur", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Impact", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("The Knight", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Lady of the Wood", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Magnificent Mara", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Malichae", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Necro", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Pyre", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Quicksilver", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Starlight", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("The Stranger", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Tango One", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Terminus", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Titan", [SotmSource.TheCauldron], SotmCategory.Hero),
    ("Vanish", [SotmSource.TheCauldron], SotmCategory.Hero),
    # Environments
    ("Insula Primalis", [], SotmCategory.Environment),
    ("Megalopolis", [], SotmCategory.Environment),
    ("Ruins of Atlantis", [], SotmCategory.Environment),
    ("Wagner Mars Base", [], SotmCategory.Environment),
    ("Silver Gulch 1883", [SotmSource.SilverGulch1883], SotmCategory.Environment),
    ("Pike Industrial Complex", [SotmSource.RookCity], SotmCategory.Environment),
    ("Rook City", [SotmSource.RookCity], SotmCategory.Environment),
    ("Realm of Discord", [SotmSource.InfernalRelics], SotmCategory.Environment),
    ("Tomb of Anubis", [SotmSource.InfernalRelics], SotmCategory.Environment),
    ("The Final Wasteland", [SotmSource.TheFinalWasteland], SotmCategory.Environment),
    ("The Block", [SotmSource.ShatteredTimelines], SotmCategory.Environment),
    ("Time Cataclysm", [SotmSource.ShatteredTimelines], SotmCategory.Environment),
    ("Dok'Thorath Capital", [SotmSource.WrathOfTheCosmos], SotmCategory.Environment),
    ("The Enclave of the Endlings", [SotmSource.WrathOfTheCosmos], SotmCategory.Environment),
    ("Omnitron IV", [SotmSource.OmnitronIV], SotmCategory.Environment),
    ("Freedom Tower", [SotmSource.Vengeance], SotmCategory.Environment),
    ("Mobile Defense Platform", [SotmSource.Vengeance], SotmCategory.Environment),
    ("The Court of Blood", [SotmSource.VillainsOfTheMultiverse], SotmCategory.Environment),
    ("Madame Mittermeier's Fantastical Festival of Conundrums and Curiosities", [SotmSource.VillainsOfTheMultiverse],
     SotmCategory.Environment),
    ("Magmaria", [SotmSource.VillainsOfTheMultiverse], SotmCategory.Environment),
    ("The Temple of Zhu Long", [SotmSource.VillainsOfTheMultiverse], SotmCategory.Environment),
    ("The Celestial Tribunal", [SotmSource.TheCelestialTribunal], SotmCategory.Environment),
    ("Champion Studios", [SotmSource.Oblivaeon], SotmCategory.Environment),
    ("Fort Adamant", [SotmSource.Oblivaeon], SotmCategory.Environment),
    ("Maerynian Refuge", [SotmSource.Oblivaeon], SotmCategory.Environment),
    ("Mordengrad", [SotmSource.Oblivaeon], SotmCategory.Environment),
    ("Nexus of the Void", [SotmSource.Oblivaeon], SotmCategory.Environment),
    ("Blackwood Forest", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("Catchwater Harbor 1929", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("The Chasm of a Thousand Nights", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("The Cybersphere", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("Dungeons of Terror", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("F.S.C. Continuance Wanderer", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("Halberd E.R.C.", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("Nightlore Citadel", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("Northspar", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("Oblask Crater", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("St. Simeon's Catacombs", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("Superstorm Akela", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("Vault 5", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("The Wandering Isle", [SotmSource.TheCauldron], SotmCategory.Environment),
    ("Windmill City", [SotmSource.TheCauldron], SotmCategory.Environment),
    # Variants
    ("America's Greatest Legacy", [], SotmCategory.Variant, "Legacy",
     lambda state, player: has_all_of(["Ambuscade", "Silver Gulch 1883"], state, player)),
    ("America's Newest Legacy", [], SotmCategory.Variant, "Legacy",
     lambda state, player: any_variants_of(["Legacy", "Baron Blade"], state, player)
        and state.has("Wagner Mars Base", player)),
    ("Dark Visionary", [], SotmCategory.Variant, "The Visionary",
     lambda state, player: any_variant("The Visionary", state, player) and state.has("Gloomweaver", player)),
    ("The Eternal Haka", [], SotmCategory.Variant, "Haka",
     lambda state, player: any_variant("Haka", state, player) and state.has("The Final Wasteland", player)),
    ("G.I. Bunker", [], SotmCategory.Variant, "Bunker",
     lambda state, player: any_variant("Bunker", state, player)),
    ("Ra: Horus of Two Horizons", [], SotmCategory.Variant, "Ra",
     lambda state, player: any_variant("Ra", state, player) and state.has("The Ennead", player)),
    ("Ra: Setting Sun", [], SotmCategory.Variant, "Ra",
     lambda state, player: has_all_of(["Ra: Horus of Two Horizons", "The Ennead", "Tomb of Anubis"],
                                      state, player)),
    ("Redeemer Fanatic", [], SotmCategory.Variant, "Fanatic",
     lambda state, player: any_variant("Fanatic", state, player) and state.has("Apostate", player)),
    ("Rook City Wraith", [], SotmCategory.Variant, "Wraith",
     lambda state, player: any_variant("Wraith", state, player)),
    ("The Super-Scientific Tachyon", [], SotmCategory.Variant, "Tachyon",
     lambda state, player: any_variant("Tachyon", state, player)),
    ("The Visionary Unleashed", [], SotmCategory.Variant, "The Visionary",
     lambda state, player: has_all_of(["Dark Visionary", "Argent Adept", "The Enclave of the Endlings"],
                                      state, player)),
    ("Captain Cosmic Requital", [SotmSource.WrathOfTheCosmos], SotmCategory.Variant, "Captain Cosmic",
     lambda state, player: state.has("Captain Cosmic", player)
        and any_variant("Infinitor", state, player)),
    ("Chrono-Ranger The Best of Times", [SotmSource.ShatteredTimelines], SotmCategory.Variant, "Chrono-Ranger",
     lambda state, player: any_variants_of(["Chrono-Ranger", "Tachyon"], state, player)
        and has_all_of(["Ambuscade", "Wagner Mars Base"], state, player)),
    ("Dark Conductor Argent Adept", [SotmSource.InfernalRelics], SotmCategory.Variant, "Argent Adept",
     lambda state, player: any_variant("Argent Adept", state, player)),
    ("Extremist Sky-Scraper", [SotmSource.WrathOfTheCosmos], SotmCategory.Variant, "Sky-Scraper",
     lambda state, player: state.has("Sky-Scraper", player) and any_variant("Baron Blade", state, player)),
    ("Omnitron-U", [SotmSource.ShatteredTimelines], SotmCategory.Variant, "Omnitron-X",
     lambda state, player: any_variant("Unity", state, player)
        and has_all_of(["Omnitron-X", "Omnitron", "Omnitron II"], state, player)),
    ("Santa Guise", [SotmSource.Guise], SotmCategory.Variant, "Guise",
     lambda state, player: any_variant("Guise", state, player)),
    ("The Scholar of the Infinite", [SotmSource.TheScholar], SotmCategory.Variant, "The Scholar",
     lambda state, player: any_variant("The Scholar", state, player)
        and (any_variant("Gloomweaver", state, player) or state.has("Apostate", player))),
    ("Action Hero Stuntman", [SotmSource.Stuntman], SotmCategory.Variant, "Stuntman",
     lambda state, player: any_variant("The Sentinels", state, player)
        and has_all_of(["Ambuscade", "Ambuscade (Team)", "The Chairman", "Pike Industrial Complex"], state, player)
        and team_villain_count(state, player)),
    ("Akash'Thriya: Spirit of the Void", [SotmSource.Oblivaeon], SotmCategory.Variant, "Akash'Thriya",
     lambda state, player: any_variant("Akash'Thriya", state, player) and state.has("Nexus of the Void", player)),
    ("Benchmark Supply & Demand", [SotmSource.Benchmark], SotmCategory.Variant, "Benchmark",
     lambda state, player: has_all_of([
         "Ambuscade (Team)", "Baron Blade (Team)", "Friction (Team)", "Fright Train (Team)", "Plague Rat (Team)"
     ], state, player) and
        any_variants_of(["Benchmark", "Expatriette", "Luminary", "Parse", "Setback"], state, player)),
    ("Heroic Luminary", [SotmSource.Oblivaeon], SotmCategory.Variant, "Luminary",
     lambda state, player: has_all_of(["Realm of Discord", "Freedom Tower", "Megalopolis"], state, player)
        and any_variants_of(["Luminary", "Legacy", "Bunker", "Absolute Zero", "Tachyon", "Wraith", "Baron Blade"],
                            state, player)),
    ("K.N.Y.F.E. Rogue Agent", [SotmSource.Vengeance], SotmCategory.Variant, "K.N.Y.F.E.",
     lambda state, player: has_all_of(["K.N.Y.F.E.", "The Block"], state, player)),
    ("La Comodora: Curse of the Black Spot", [SotmSource.Oblivaeon], SotmCategory.Variant, "La Comodora",
     lambda state, player: any_variant("La Comodora", state, player) and state.has("Time Cataclysm", player)),
    ("Lifeline Blood Mage", [SotmSource.Oblivaeon], SotmCategory.Variant, "Lifeline",
     lambda state, player: any_variant("Lifeline", state, player)
        and state.has("The Court of Blood", player)),
    ("Parse: Fugue State", [SotmSource.Vengeance], SotmCategory.Variant, "Parse",
     lambda state, player: has_all_of(["Parse", "Progeny"], state, player)),
    ("The Adamant Sentinels", [SotmSource.Vengeance], SotmCategory.Variant, "The Sentinels",
     lambda state, player: state.has("The Sentinels", player)),
    ("The Hunted Naturalist", [SotmSource.Vengeance], SotmCategory.Variant, "The Naturalist",
     lambda state, player: state.has("The Naturalist", player)),
    ("Termi-Nation Bunker", [], SotmCategory.Variant, "Bunker",
     lambda state, player: has_all_of(["Bunker", "Omnitron", "Omnitron II", "Omnitron IV"], state, player)),
    ("Termi-Nation Absolute Zero", [], SotmCategory.Variant, "Absolute Zero",
     lambda state, player: state.has("Absolute Zero", player)),
    ("Termi-Nation Unity", [SotmSource.Unity], SotmCategory.Variant, "Unity",
     lambda state, player: state.has("Unity", player)),
    ("Freedom Six Absolute Zero", [], SotmCategory.Variant, "Absolute Zero",
     lambda state, player: state.has("Absolute Zero", player) and state.has("Iron Legacy", player)),
    ("Freedom Six Bunker", [], SotmCategory.Variant, "Bunker",
     lambda state, player: state.has("Bunker", player) and state.has("Iron Legacy", player)),
    ("Freedom Six Tachyon", [], SotmCategory.Variant, "Tachyon",
     lambda state, player: state.has("Tachyon", player) and state.has("Iron Legacy", player)),
    ("Freedom Six Tempest", [], SotmCategory.Variant, "Tempest",
     lambda state, player: state.has("Tempest", player) and state.has("Iron Legacy", player)),
    ("Freedom Six Wraith", [], SotmCategory.Variant, "Wraith",
     lambda state, player: state.has("Wraith", player) and has_all_of(["Iron Legacy", "The Chairman"], state, player)),
    ("Freedom Six Unity", [SotmSource.Unity], SotmCategory.Variant, "Unity",
     lambda state, player: state.has("Unity", player) and state.has("Iron Legacy", player)),
    ("Dark Watch Expatriette", [SotmSource.RookCity], SotmCategory.Variant, "Expatriette",
     lambda state, player: any_variants_of(["Expatriette", "Baron Blade"], state, player)
        and state.has("Rook City", player)),
    ("Dark Watch Mister Fixer", [SotmSource.RookCity], SotmCategory.Variant, "Mister Fixer",
     lambda state, player: any_variant("Mister Fixer", state, player) and state.has("The Chairman", player)),
    ("Dark Watch Nightmist", [SotmSource.InfernalRelics], SotmCategory.Variant, "Nightmist",
     lambda state, player: any_variants_of(["Nightmist", "Expatriette"], state, player)
        and state.has("Realm of Discord", player)),
    ("Dark Watch Setback", [SotmSource.Vengeance], SotmCategory.Variant, "Setback",
     lambda state, player: has_all_of([
         "Setback",
         "Dark Watch Expatriette",
         "Dark Watch Mister Fixer",
         "Dark Watch Nightmist",
         "The Chairman",
         "Rook City"
     ], state, player)),
    ("Dark Watch Harpy", [SotmSource.Oblivaeon], SotmCategory.Variant, "The Harpy",
     lambda state, player: any_variants_of(["The Harpy", "Gloomweaver"], state, player)
        and state.has("Realm of Discord", player)),
    ("Prime Wardens Argent Adept", [SotmSource.InfernalRelics], SotmCategory.Variant, "Argent Adept",
     lambda state, player: has_all_of([
         "Akash'Bhuta", "Argent Adept", "Captain Cosmic", "Haka", "Tempest", "Redeemer Fanatic"
     ], state, player)),
    ("Prime Wardens Captain Cosmic", [SotmSource.WrathOfTheCosmos], SotmCategory.Variant, "Captain Cosmic",
     lambda state, player: has_all_of(["Prime Wardens Argent Adept", "Captain Cosmic", "Dok'Thorath Capital"],
                                      state, player)),
    ("Prime Wardens Fanatic", [], SotmCategory.Variant, "Fanatic",
     lambda state, player: has_all_of(["Prime Wardens Argent Adept", "Apostate"], state, player)
        and (state.has("Fanatic", player) or state.has("Redeemer Fanatic", player))),
    ("Prime Wardens Haka", [], SotmCategory.Variant, "Haka",
     lambda state, player: has_all_of(["Prime Wardens Argent Adept", "Haka", "Ambuscade"], state, player)),
    ("Prime Wardens Tempest", [], SotmCategory.Variant, "Tempest",
     lambda state, player: has_all_of(["Prime Wardens Argent Adept", "Tempest"], state, player)),
    ("Xtreme Prime Wardens Argent Adept", [SotmSource.InfernalRelics], SotmCategory.Variant, "Argent Adept",
     lambda state, player: has_all_of(["Argent Adept", "Insula Primalis"], state, player)),
    ("Xtreme Prime Wardens Tempest", [], SotmCategory.Variant, "Tempest",
     lambda state, player: has_all_of(["Tempest", "The Enclave of the Endlings"], state, player)),
    ("Xtreme Prime Wardens Captain Cosmic", [SotmSource.WrathOfTheCosmos], SotmCategory.Variant, "Captain Cosmic",
     lambda state, player: has_all_of(["Captain Cosmic", "Dok'Thorath Capital"], state, player)),
    ("Xtreme Prime Wardens Fanatic", [], SotmCategory.Variant, "Fanatic",
     lambda state, player: has_all_of(["Fanatic", "The Court of Blood"], state, player)),
    ("Xtreme Prime Wardens Haka", [], SotmCategory.Variant, "Haka",
     lambda state, player: has_all_of(["Haka", "Magmaria"], state, player)),
    ("Freedom Five Absolute Zero", [], SotmCategory.Variant, "Absolute Zero",
     lambda state, player: freedom_five_reqs(state, player)),
    ("Freedom Five Bunker", [], SotmCategory.Variant, "Bunker",
     lambda state, player: freedom_five_reqs(state, player)),
    ("Freedom Five Wraith", [], SotmCategory.Variant, "Wraith",
     lambda state, player: freedom_five_reqs(state, player)),
    ("Freedom Five Tachyon", [], SotmCategory.Variant, "Tachyon",
     lambda state, player: freedom_five_reqs(state, player)),
    ("Freedom Five Legacy", [], SotmCategory.Variant, "Legacy",
     lambda state, player: freedom_five_reqs(state, player)),
    ("Super Sentai Idealist", [SotmSource.TheVoidGuard], SotmCategory.Variant, "The Idealist",
     lambda state, player: any_variant("The Idealist", state, player)),
    ("Dr. Medico Malpractice", [SotmSource.TheVoidGuard], SotmCategory.Variant, "Dr. Medico",
     lambda state, player: any_variant("Dr. Medico", state, player)
        and state.has("Ambuscade (Team)", player)
        and team_villain_count(state, player)),
    ("Cosmic Inventor Writhe", [SotmSource.TheVoidGuard], SotmCategory.Variant, "Writhe",
     lambda state, player: any_variant("Writhe", state, player)),
    ("Road Warrior Mainstay", [SotmSource.TheVoidGuard], SotmCategory.Variant, "Mainstay",
     lambda state, player: any_variant("Mainstay", state, player)),
    ("Completionist Guise", [SotmSource.Guise], SotmCategory.Variant, "Guise"),
    ("Baccarat Ace of Swords", [SotmSource.TheCauldron], SotmCategory.Variant, "Baccarat"),
    ("Baccarat Ace of Sorrows", [SotmSource.TheCauldron], SotmCategory.Variant, "Baccarat"),
    ("Baccarat 1929", [SotmSource.TheCauldron], SotmCategory.Variant, "Baccarat"),
    ("First Response Cricket", [SotmSource.TheCauldron], SotmCategory.Variant, "The Cricket"),
    ("The Cricket Renegade", [SotmSource.TheCauldron], SotmCategory.Variant, "The Cricket"),
    ("The Cricket Wasteland Ronin", [SotmSource.TheCauldron], SotmCategory.Variant, "The Cricket"),
    ("First Response Cypher", [SotmSource.TheCauldron], SotmCategory.Variant, "Cypher"),
    ("Cypher Swarming Protocol", [SotmSource.TheCauldron], SotmCategory.Variant, "Cypher"),
    ("First Response Doc Havoc", [SotmSource.TheCauldron], SotmCategory.Variant, "Doc Havoc"),
    ("Doc Havoc 2199", [SotmSource.TheCauldron], SotmCategory.Variant, "Doc Havoc"),
    ("Drift Through the Breach", [SotmSource.TheCauldron], SotmCategory.Variant, "Drift"),
    ("Drift 1929 & 2199", [SotmSource.TheCauldron], SotmCategory.Variant, "Drift"),
    ("Drift 1609", [SotmSource.TheCauldron], SotmCategory.Variant, "Drift"),
    ("Drift 1789", [SotmSource.TheCauldron], SotmCategory.Variant, "Drift"),
    ("Test Subject Drift", [SotmSource.TheCauldron], SotmCategory.Variant, "Drift"),
    ("First Response Echelon", [SotmSource.TheCauldron], SotmCategory.Variant, "Echelon"),
    ("Echelon 2199", [SotmSource.TheCauldron], SotmCategory.Variant, "Echelon"),
    ("Gargoyle Wasteland Ronin", [SotmSource.TheCauldron], SotmCategory.Variant, "Gargoyle"),
    ("Gargoyle 2199", [SotmSource.TheCauldron], SotmCategory.Variant, "Gargoyle"),
    ("Gargoyle Dragon Ranger", [SotmSource.TheCauldron], SotmCategory.Variant, "Gargoyle"),
    ("Gargoyle Infiltrator", [SotmSource.TheCauldron], SotmCategory.Variant, "Gargoyle"),
    ("Gyrosaur Speed Demon", [SotmSource.TheCauldron], SotmCategory.Variant, "Gyrosaur"),
    ("Gyrosaur Renegade", [SotmSource.TheCauldron], SotmCategory.Variant, "Gyrosaur"),
    ("Captain Gyrosaur", [SotmSource.TheCauldron], SotmCategory.Variant, "Gyrosaur"),
    ("Impact Renegade", [SotmSource.TheCauldron], SotmCategory.Variant, "Impact"),
    ("Impact Wasteland Ronin", [SotmSource.TheCauldron], SotmCategory.Variant, "Impact"),
    ("The Fair Knight", [SotmSource.TheCauldron], SotmCategory.Variant, "The Knight"),
    ("The Berserker Knight", [SotmSource.TheCauldron], SotmCategory.Variant, "The Knight"),
    ("The Knight 1929", [SotmSource.TheCauldron], SotmCategory.Variant, "The Knight"),
    ("The Knights Wasteland Ronin", [SotmSource.TheCauldron], SotmCategory.Variant, "The Knight"),
    ("Lady of the Wood Season of Change", [SotmSource.TheCauldron], SotmCategory.Variant, "Lady of the Wood"),
    ("Ministry of Strategic Science Lady of the Wood", [SotmSource.TheCauldron], SotmCategory.Variant,
     "Lady of the Wood"),
    ("Lady of the Wood 2199", [SotmSource.TheCauldron], SotmCategory.Variant, "Lady of the Wood"),
    ("Ministry of Strategic Science Magnificent Mara", [SotmSource.TheCauldron], SotmCategory.Variant,
     "Magnificent Mara"),
    ("Magnificent Mara 1929", [SotmSource.TheCauldron], SotmCategory.Variant, "Magnificent Mara"),
    ("Shardmaster Malichae", [SotmSource.TheCauldron], SotmCategory.Variant, "Malichae"),
    ("Ministry of Strategic Science Malichae", [SotmSource.TheCauldron], SotmCategory.Variant, "Malichae"),
    ("Necro Warden of Chaos", [SotmSource.TheCauldron], SotmCategory.Variant, "Necro"),
    ("Necro 1929", [SotmSource.TheCauldron], SotmCategory.Variant, "Necro"),
    ("Necro Last of the Forgotten Order", [SotmSource.TheCauldron], SotmCategory.Variant, "Necro"),
    ("The Unstable Pyre", [SotmSource.TheCauldron], SotmCategory.Variant, "Pyre"),
    ("Pyre Wasteland Ronin", [SotmSource.TheCauldron], SotmCategory.Variant, "Pyre"),
    ("Pyre Expedition Oblask", [SotmSource.TheCauldron], SotmCategory.Variant, "Pyre"),
    ("The Uncanny Quicksilver", [SotmSource.TheCauldron], SotmCategory.Variant, "Quicksilver"),
    ("Quicksilver Renegade", [SotmSource.TheCauldron], SotmCategory.Variant, "Quicksilver"),
    ("Harbinger Quicksilver", [SotmSource.TheCauldron], SotmCategory.Variant, "Quicksilver"),
    ("Starlight Genesis", [SotmSource.TheCauldron], SotmCategory.Variant, "Starlight"),
    ("Nightlore Council Starlight", [SotmSource.TheCauldron], SotmCategory.Variant, "Starlight"),
    ("Starlight Area-51", [SotmSource.TheCauldron], SotmCategory.Variant, "Starlight"),
    ("The Runecarved Stranger", [SotmSource.TheCauldron], SotmCategory.Variant, "The Stranger"),
    ("The Stranger 1929", [SotmSource.TheCauldron], SotmCategory.Variant, "The Stranger"),
    ("The Stranger Wasteland Ronin", [SotmSource.TheCauldron], SotmCategory.Variant, "The Stranger"),
    ("The Stranger in the Corn", [SotmSource.TheCauldron], SotmCategory.Variant, "The Stranger"),
    ("Tango One Ghost Ops", [SotmSource.TheCauldron], SotmCategory.Variant, "Tango One"),
    ("Tango One 1929", [SotmSource.TheCauldron], SotmCategory.Variant, "Tango One"),
    ("Tango One Creed of the Sniper", [SotmSource.TheCauldron], SotmCategory.Variant, "Tango One"),
    ("Ministry of Strategic Science Terminus", [SotmSource.TheCauldron], SotmCategory.Variant, "Terminus"),
    ("Terminus 2199", [SotmSource.TheCauldron], SotmCategory.Variant, "Terminus"),
    ("Ministry of Strategic Science Titan", [SotmSource.TheCauldron], SotmCategory.Variant, "Titan"),
    ("Titan 2199", [SotmSource.TheCauldron], SotmCategory.Variant, "Titan"),
    ("Titan Oni", [SotmSource.TheCauldron], SotmCategory.Variant, "Titan"),
    ("First Response Vanish", [SotmSource.TheCauldron], SotmCategory.Variant, "Vanish"),
    ("Vanish 1929", [SotmSource.TheCauldron], SotmCategory.Variant, "Vanish"),
    ("Vanish Tomb of Thieves", [SotmSource.TheCauldron], SotmCategory.Variant, "Vanish"),
    ("Urban Warfare Expatriette", [SotmSource.CauldronPromos, SotmSource.RookCity],
     SotmCategory.Variant, "Expatriette"),
    ("Siege Breaker Bunker", [SotmSource.CauldronPromos], SotmCategory.Variant, "Bunker"),
    ("Nitro Boost Absolute Zero", [SotmSource.CauldronPromos], SotmCategory.Variant, "Absolute Zero"),
    ("Enlightened Mister Fixer", [SotmSource.CauldronPromos, SotmSource.RookCity],
     SotmCategory.Variant, "Mister Fixer"),
    ("Northern Wind Mister Fixer", [SotmSource.CauldronPromos, SotmSource.RookCity],
     SotmCategory.Variant, "Mister Fixer"),
    ("Omnitron-XI", [SotmSource.CauldronPromos, SotmSource.ShatteredTimelines], SotmCategory.Variant, "Omnitron-X"),
]]

difficulties = ["Normal", "Advanced", "Challenge", "Ultimate"]

_base_to_variants: dict[str, list[str]] = {
    key: [d.name for d in group] for key, group in
    groupby(sorted(d for d in data if d.category == SotmCategory.Variant or d.category == SotmCategory.VillainVariant),
            key=lambda d: d.base)
}


def any_variant(base: str, state: CollectionState | SotmState, player: int) -> bool:
    return True in (state.has(name, player) for name in _base_to_variants[base])


def team_villain_count(state: CollectionState | SotmState, player: int) -> bool:
    return [state.has(d.name, player) for d in data if d.category == SotmCategory.TeamVillain].count(True) >= 3


def has_all_of(items: list[str], state: CollectionState | SotmState, player: int) -> bool:
    return False not in (state.has(item, player) for item in items)


def any_variants_of(items: list[str], state: CollectionState | SotmState, player: int) -> bool:
    return False not in (any_variant(item, state, player) for item in items)


def freedom_five_reqs(state: CollectionState | SotmState, player: int) -> bool:
    return has_all_of(["Progeny",
                       "Rook City",
                       "Megalopolis",
                       "Prime Wardens Argent Adept",
                       "Prime Wardens Captain Cosmic",
                       "Prime Wardens Fanatic",
                       "Prime Wardens Haka",
                       "Prime Wardens Tempest",
                       "Dark Watch Expatriette",
                       "Dark Watch Mister Fixer",
                       "Dark Watch Nightmist",
                       "Dark Watch Setback",
                       "Dark Watch Harpy",
                       "Legacy",
                       "Bunker",
                       "Absolute Zero",
                       "Tachyon",
                       "Wraith"], state, player)


def general_access_rule(state: CollectionState, player: int):
    return ([d.category == SotmCategory.Hero and any_variant(d.name, state, player) for d in data].count(True) >= 3
            and True in (d.category == SotmCategory.Environment and state.has(d.name, player) for d in data)
            and (team_villain_count(state, player)
                 or True in ((d.category == SotmCategory.Villain or d.category == SotmCategory.VillainVariant)
                             and state.has(d.name, player) for d in data)))

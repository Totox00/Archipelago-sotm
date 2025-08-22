import math
from itertools import chain
from typing import Dict, Set, Optional, NamedTuple

from BaseClasses import MultiWorld, Region, Item, Tutorial, ItemClassification, CollectionState
from Options import Toggle, OptionError

from worlds.AutoWorld import World, WebWorld

from .Items import SotmItem
from .Locations import SotmLocation
from .Options import SotmOptions, sotm_option_groups
from .Data import SotmSource, SotmData, SotmCategory, data, difficulties, SotmState, sources, FillerType, \
    damage_types, filler, base_to_variants, packs
from .Id import item_name_to_id, location_name_to_id


class SotmWeb(WebWorld):
    bug_report_page = "https://github.com/Totox00/ap-sotm-client/issues"
    theme = "ocean"
    option_groups = sotm_option_groups
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Sentinels of the Multiverse randomizer client on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Toto00"]
    )]


class LocationDensity(NamedTuple):
    villain_normal: int
    villain_advanced: int
    villain_challenge: int
    villain_ultimate: int
    environment: int
    hero: int
    variant_unlock: int


class VillainPoints(NamedTuple):
    normal: int
    advanced: int
    challenge: int
    ultimate: int


class StartingItems(NamedTuple):
    heroes: int
    villains: int
    environments: int
    contenders: int
    gladiators: int


class FillerOption:
    name: str
    type: FillerType
    is_trap: bool
    specificity: int
    remaining: Optional[int] | list[int] | list[None]
    min: Optional[int]

    def __init__(self, name, type, is_trap, specificity, remaining, min):
        self.name = name
        self.type = type
        self.is_trap = is_trap
        self.specificity = specificity
        self.remaining = remaining
        self.min = min


class SotmWorld(World):
    """
    Sentinels of the Multiverse is a cooperative, fixed-deck card game with a comic book flavor designed by
    Christopher Badell, Paul Bender, and Adam Debottaro, and published by Greater Than Games.
    Each player plays as a hero, against a villain, in an environment.
    """

    game = "Sentinels of the Multiverse"
    options_dataclass = SotmOptions
    options: SotmOptions
    topology_present: bool = False
    web = SotmWeb()

    enabled_sources: Set[SotmSource]

    available_villains: list[SotmData]
    available_gladiators: list[SotmData]
    available_heroes: list[SotmData]
    available_contenders: list[SotmData]
    available_environments: list[SotmData]
    available_variants: list[SotmData]
    available_variant_unlocks: list[SotmData]

    state: SotmState
    included_villains: list[SotmData]
    included_gladiators: list[SotmData]
    included_heroes: list[SotmData]
    included_contenders: list[SotmData]
    included_environments: list[SotmData]
    included_variants: list[SotmData]
    possible_variants: list[SotmData]

    start_heroes: list[str]
    start_villains: list[str]
    start_environments: list[str]
    start_contenders: list[str]
    start_gladiators: list[str]

    total_pool_size: int
    total_locations: int
    total_items: int
    team_villains: int

    required_scions: int
    required_villains: int
    required_variants: int

    total_possible_villain_points: int
    max_points_per_villain: int
    location_density: LocationDensity
    villain_points: VillainPoints
    starting_items: StartingItems
    pool_size: list[int]

    filler_options: list[FillerOption]
    filler_weights: list[int]
    filler_weights_pos: list[int]

    required_client_version = (0, 4, 0)
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = SotmItem.get_item_name_groups(item_name_to_id)
    location_name_groups = SotmLocation.get_location_name_groups()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.state = SotmState()
        self.total_items = 0
        self.total_locations = 0
        self.enabled_sources = set()
        self.included_villains = []
        self.included_gladiators = []
        self.included_heroes = []
        self.included_contenders = []
        self.included_environments = []
        self.included_variants = []
        self.possible_variants = []

    def generate_early(self):
        for pack, pack_data in packs.items():
            if pack_data["name"] in self.options.enabled_sets.value:
                for source in pack_data["contains"]:
                    self.enabled_sources.add(source)
        for source, source_data in sources.items():
            if source_data["name"] in self.options.enabled_sets.value:
                self.enabled_sources.add(source)

        self.location_density = LocationDensity(
            self.options.location_density.value["villain"]["normal"],
            self.options.location_density.value["villain"]["advanced"],
            self.options.location_density.value["villain"]["challenge"],
            self.options.location_density.value["villain"]["ultimate"],
            self.options.location_density.value["environment"],
            self.options.location_density.value["hero"],
            self.options.location_density.value["variant_unlock"]
        )

        self.villain_points = VillainPoints(
            self.options.villain_points.value["normal"],
            self.options.villain_points.value["advanced"],
            self.options.villain_points.value["challenge"],
            self.options.villain_points.value["ultimate"]
        )

        self.starting_items = StartingItems(
            self.options.starting_items["heroes"],
            self.options.starting_items["villains"],
            self.options.starting_items["environments"],
            self.options.starting_items["contenders"],
            self.options.starting_items["gladiators"]
        )

        available = [d for d in data if (d.name not in self.options.exclude_from_pool.value)
                     and (False not in ((source in self.enabled_sources) for source in d.sources))]
        full_state = SotmState()
        full_state.items.update(d.name for d in available)
        self.available_villains = [d for d in available if d.category in
                                   (SotmCategory.Villain, SotmCategory.VillainVariant, SotmCategory.TeamVillain)]
        self.available_gladiators = [d for d in available if d.category == SotmCategory.Gladiator]
        self.available_heroes = [d for d in available if d.category == SotmCategory.Hero]
        self.available_contenders = [d for d in available if d.category == SotmCategory.Contender]
        self.available_environments = [d for d in available if d.category == SotmCategory.Environment]
        self.available_variants = [d for d in available if d.category == SotmCategory.Variant]
        self.available_variant_unlocks = [d for d in available
                                          if d.category in (SotmCategory.Variant, SotmCategory.VillainVariant)
                                          and d.rule is not None and d.rule(full_state, self.player)]
        self.total_pool_size = len(available)

        self.max_points_per_villain = (self.villain_points.normal + self.villain_points.advanced
                                       + self.villain_points.challenge + self.villain_points.ultimate)
        self.total_possible_villain_points = len(self.available_villains) * self.max_points_per_villain

        self.required_villains = min(self.options.required_villains.value, self.total_possible_villain_points)
        self.required_variants = min(self.options.required_variants.value, len(self.available_variant_unlocks))

        self.resolve_pool_size()

        # We can take a shortcut if pool size is maximum
        available = [self.available_villains, self.available_environments, self.available_heroes,
                     self.available_variants, self.available_contenders, self.available_gladiators]
        for i in range(6):
            if self.pool_size[i] == len(available[i]):
                for d in reversed(available[i]):
                    self.include_data(d)

        # Add starting items to pool
        starting_names = [item for item in self.options.start_inventory.value]
        for d in self.available():
            if d.name in starting_names:
                starting_names.remove(d.name)
                self.include_data(d)

        if len(starting_names) > 0:
            raise OptionError(
                f"Item {starting_names[0]} is marked as a starting item but does not exist with enabled sources")

        for item in self.options.include_in_pool.value:
            item_data = self.find_data(item)
            if item_data is None:
                raise OptionError(f"Unable to find data for item {item}")
            self.include_data(item_data)
        for variant in self.options.include_variants_in_pool.value:
            variant_data = self.find_data(variant)
            if variant_data is None:
                raise OptionError(f"Unable to find data for variant {variant}")
            self.include_variant_unlock(variant_data)

        # Add items until there are enough for the required variant counts
        while len(self.possible_variants) < self.required_variants:
            needed = self.min_needed_for_variant(self.random.choice(self.available_variant_unlocks))
            for d in needed:
                self.include_data(d)

        # Ensure that if there are team villains, there are at least 3
        self.team_villains = len([v for v in self.included_villains if v.category == SotmCategory.TeamVillain])
        self.ensure_team_villains()

        # Add villains until there are enough for the starting and required villain counts
        needed_villains = max(self.starting_items.villains,
                              math.ceil(self.required_villains / self.total_possible_villain_points))
        while len(self.included_villains) < needed_villains:
            self.include_data(chosen := self.random.choice(self.available_villains))
            if chosen.category == SotmCategory.TeamVillain:
                self.team_villains += 1
                self.ensure_team_villains()

        # Starting villains cannot be team villains
        while (len([d for d in self.included_villains if d.category != SotmCategory.TeamVillain])
               < self.starting_items.villains):
            available_villains = [d for d in self.available_villains if d.category != SotmCategory.TeamVillain]
            self.include_data(self.random.choice(available_villains))

        # Add heroes and hero variants until there are enough for the start hero count
        # Make sure there are not too few due to some being variants of the same hero
        while len(self.included_heroes) + len(self.included_variants) < self.starting_items.heroes:
            chosen = self.random.choice(self.available_heroes)
            if not self.state.has(f"Any {chosen.name}", self.player):
                self.include_data(chosen)

        # Add contenders, gladiators, and environments until there are enough for the starting counts
        for (included, starting, available) in (
            (self.included_contenders, self.starting_items.contenders, self.available_contenders),
            (self.included_gladiators, self.starting_items.gladiators, self.available_gladiators),
            (self.included_environments, self.starting_items.environments, self.available_environments),
        ):
            while len(included) < starting:
                self.include_data(self.random.choice(available))

        # Oblivaeon requires 5 environments if part of goal
        if self.options.required_scions.value > 0:
            while len(self.included_environments) < 5:
                self.include_data(self.random.choice(self.available_environments))

        # Add random items to included items until pool size is satisfied
        available = [self.available_villains, self.available_environments, self.available_heroes,
                     self.available_variants, self.available_contenders, self.available_gladiators]
        included = [self.included_villains, self.included_environments, self.included_heroes,
                    self.included_variants, self.included_contenders, self.included_gladiators]

        for i in range(6):
            while self.pool_size[i] > len(included[i]) and len(available[i]) > 0:
                chosen = self.random.choice(available[i])
                self.include_data(chosen)
                if chosen.category == SotmCategory.TeamVillain:
                    self.team_villains += 1
                    self.ensure_team_villains()
                elif chosen.category == SotmCategory.Contender:
                    self.ensure_contenders()
                elif chosen.category == SotmCategory.Gladiator:
                    self.ensure_gladiators()

        # Add random items from included items to precollected until start counts are satisfied
        start_hero_bases = []
        start_hero_count = 0
        self.start_heroes = []
        self.start_villains = []
        self.start_environments = []
        self.start_contenders = []
        self.start_gladiators = []
        for name in self.options.start_inventory.value:
            d = next((d for d in data if d.name == name), None)
            if d is not None:
                match d.category:
                    case SotmCategory.Hero:
                        if d.name not in start_hero_bases:
                            start_hero_bases.append(d.name)
                            start_hero_count += 1
                            self.start_heroes.append(d.name)
                    case SotmCategory.Variant:
                        if d.base not in start_hero_bases:
                            start_hero_bases.append(d.base)
                            start_hero_count += 1
                            self.start_heroes.append(d.name)
                    case SotmCategory.Villain | SotmCategory.VillainVariant:
                        self.start_villains.append(d.name)
                    case SotmCategory.Environment:
                        self.start_environments.append(d.name)
                    case SotmCategory.Contender:
                        self.start_contenders.append(d.name)
                    case SotmCategory.Gladiator:
                        self.start_gladiators.append(d.name)

        for _ in range(start_hero_count, self.starting_items.heroes):
            choices = ([d for d in self.included_heroes if d.name not in start_hero_bases]
                       + [d for d in self.included_variants if d.base not in start_hero_bases])
            chosen = self.random.choice(choices)
            self.multiworld.push_precollected(self.create_item_from_data(chosen))
            self.start_heroes.append(chosen.name)
            if chosen.category == SotmCategory.Hero:
                start_hero_bases.append(chosen.name)
            else:
                start_hero_bases.append(chosen.base)

        included_non_team_villains = [d for d in self.included_villains if d.category != SotmCategory.TeamVillain]
        for (included, starting, start_count) in (
            (included_non_team_villains, self.start_villains, self.starting_items.villains),
            (self.included_environments, self.start_environments, self.starting_items.environments),
            (self.included_contenders, self.start_contenders, self.starting_items.contenders),
            (self.included_gladiators, self.start_gladiators, self.starting_items.gladiators),
        ):
            for _ in range(len(starting), start_count):
                choices = [d for d in included if d.name not in starting]
                chosen = self.random.choice(choices)
                self.multiworld.push_precollected(self.create_item_from_data(chosen))
                starting.append(chosen.name)

        self.parse_filler_weights()

    def available(self) -> list[SotmData]:
        return (self.available_villains
                + self.available_heroes
                + self.available_contenders
                + self.available_gladiators
                + self.available_environments
                + self.available_variants)

    def included(self) -> list[SotmData]:
        return (self.included_villains
                + self.included_heroes
                + self.included_contenders
                + self.included_gladiators
                + self.included_environments
                + self.included_variants)

    def include_data(self, d: SotmData) -> bool:
        if d.name in self.state.items:
            return True

        match d.category:
            case SotmCategory.Villain | SotmCategory.VillainVariant | SotmCategory.TeamVillain:
                if d not in self.available_villains:
                    return False
                self.available_villains.remove(d)
                self.included_villains.append(d)
            case SotmCategory.Environment:
                if d not in self.available_environments:
                    return False
                self.available_environments.remove(d)
                self.included_environments.append(d)
            case SotmCategory.Hero:
                if d not in self.available_heroes:
                    return False
                self.available_heroes.remove(d)
                self.included_heroes.append(d)
            case SotmCategory.Variant:
                if d not in self.available_variants:
                    return False
                self.available_variants.remove(d)
                self.included_variants.append(d)
            case SotmCategory.Contender:
                if d not in self.available_contenders:
                    return False
                self.available_contenders.remove(d)
                self.included_contenders.append(d)
            case SotmCategory.Gladiator:
                if d not in self.available_gladiators:
                    return False
                self.available_gladiators.remove(d)
                self.included_gladiators.append(d)

        self.total_items += 1
        self.state.items.add(d.name)

        for v in self.available_variant_unlocks:
            if v.rule(self.state, self.player):
                self.possible_variants.append(v)
                self.available_variant_unlocks.remove(v)

        return True

    def include_variant_unlock(self, variant: SotmData):
        if variant in self.possible_variants:
            return
        for d in self.min_needed_for_variant(variant):
            self.include_data(d)

    def min_needed_for_variant(self, variant: SotmData) -> list[SotmData]:
        maybe_deps = [d for d in self.available() if d.name not in self.state.items and d.name in variant.dependencies]
        self.random.shuffle(maybe_deps)
        test_state = SotmState()
        test_state.items.update([d.name for d in maybe_deps])
        test_state.items.update(self.state.items)
        required = []
        for d in maybe_deps:
            test_state.items.remove(d.name)
            if not variant.rule(test_state, self.player):
                test_state.items.add(d.name)
                required.append(d)
        return required

    def ensure_team_villains(self):
        while 0 < self.team_villains < 3:
            available_villains = [d for d in self.available_villains if d.category == SotmCategory.TeamVillain]
            self.include_data(self.random.choice(available_villains))
            self.team_villains += 1

    def ensure_contenders(self):
        while 0 < len(self.included_contenders) < 3:
            self.include_data(self.random.choice(self.available_contenders))

    def ensure_gladiators(self):
        while 0 < len(self.included_gladiators) < 3:
            self.include_data(self.random.choice(self.available_gladiators))

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        general_access = Region("General Access", self.player, self.multiworld)
        self.multiworld.regions.append(general_access)

        menu.add_exits({"General Access", "General Access"},
                       {"General Access": lambda state: state.has("Unique Hero Thirds", self.player, 9)
                       and state.has("Environments", self.player)
                       and (state.has("Villains", self.player)
                            or state.has("Team Villains", self.player, 3)
                            or state.has("Gladiators", self.player, 3))})

        for included in chain(self.included_gladiators, self.included_villains):
            for (difficulty, count) in (("Normal", self.location_density.villain_normal),
                                        ("Advanced", self.location_density.villain_advanced)):
                min_heroes = self.options.villain_difficulties.get(included.name, None)
                if isinstance(min_heroes, dict):
                    min_heroes = min_heroes.get(difficulty, None)
                if min_heroes is None:
                    min_heroes = self.options.villain_difficulties.get(difficulty, None)
                self.total_locations += count
                for n in range(1, count + 1):
                    name = f"{included.name} - {difficulty} #{n}"
                    general_access.locations.append(
                        SotmLocation(self.player, name, self.location_name_to_id[name], included.category,
                                     general_access, included.name, min_heroes=min_heroes))

            if included.challenge and (included.challenge_rule is None or included.challenge_rule(self.state, 0)):
                for (difficulty, count) in (("Challenge", self.location_density.villain_challenge),
                                            ("Ultimate", self.location_density.villain_ultimate)):
                    min_heroes = self.options.villain_difficulties.get(included.name, None)
                    if isinstance(min_heroes, dict):
                        min_heroes = min_heroes.get(difficulty, None)
                    if min_heroes is None:
                        min_heroes = self.options.villain_difficulties.get(difficulty, None)
                    self.total_locations += count
                    for n in range(1, count + 1):
                        name = f"{included.name} - {difficulty} #{n}"
                        general_access.locations.append(
                            SotmLocation(self.player, name, self.location_name_to_id[name], included.category,
                                         general_access, included.name, included.challenge_rule, min_heroes))

        for (included, count) in ((self.included_heroes, self.location_density.hero),
                                  (self.included_variants, self.location_density.hero),
                                  (self.included_environments, self.location_density.environment)):
            for data in included:
                for n in range(1, count + 1):
                    name = f"{data.name} - Any Difficulty #{n}"
                    general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                    data.category, general_access, data.name))
                self.total_locations += count
        for variant in self.possible_variants:
            for n in range(1, self.location_density.variant_unlock + 1):
                name = f"{variant.name} - Unlock #{n}"
                general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                variant.category, general_access, rule=variant.rule))
            self.total_locations += self.location_density.variant_unlock

    def create_items(self):
        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]
        items = []

        for included in chain(self.included_villains, self.included_environments, self.included_gladiators):
            if included.name not in exclude:
                items.append(self.create_item_from_data(included))

        for included in chain(self.included_heroes, self.included_contenders, self.included_variants):
            if included.name not in exclude:
                items.append(self.create_item_from_data(included))

        if self.options.scions_are_relative.value == Toggle.option_true:
            self.required_scions = math.floor((self.total_locations - len(items))
                                              * self.options.required_scions.value / 1000)
        else:
            self.required_scions = self.options.required_scions.value

        for i in range(0, self.required_scions):
            items.append(SotmItem(self.player, "Scion of Oblivaeon", self.item_name_to_id["Scion of Oblivaeon"],
                                  SotmCategory.Scion, ItemClassification.progression_skip_balancing))

        for idx in range(len(self.filler_options)):
            chosen = self.filler_options[idx]
            if chosen.min:
                for _ in range(chosen.min):
                    if chosen.specificity == 0 or chosen.type == FillerType.Other:
                        if chosen.remaining:
                            chosen.remaining -= 1
                            if chosen.remaining == 0:
                                self.filler_weights[idx] = 0
                                self.filler_weights_pos[idx] = 0
                        items.append(SotmItem(self.player, chosen.name, self.item_name_to_id[chosen.name],
                                              SotmCategory.Trap if chosen.is_trap else SotmCategory.Filler))
                    else:
                        for selected in range(len(chosen.remaining)):
                            if any(chosen.remaining):
                                chosen.remaining[selected] -= 1
                                if sum(chosen.remaining) == 0:
                                    self.filler_weights[idx] = 0
                                    self.filler_weights_pos[idx] = 0
                            if chosen.type == FillerType.Hero:
                                if chosen.specificity == 1:
                                    specifier = f"Any {self.included_heroes[selected].name}"
                                else:
                                    specifier = f"{self.included_variants[selected].name}"
                            else:
                                specifier = f"{self.included_villains[selected].name}"
                            name = f"{chosen.name} ({specifier})"
                            items.append(SotmItem(self.player, name, self.item_name_to_id[name],
                                                  SotmCategory.Trap if chosen.is_trap else SotmCategory.Filler))

        for _ in range(0, self.total_locations - len(items)):
            name, is_trap = self.resolve_filler()
            items.append(SotmItem(self.player, name, self.item_name_to_id[name],
                                  SotmCategory.Trap if is_trap else SotmCategory.Filler))

        self.multiworld.itempool.extend(items)

    def create_item_from_data(self, d: SotmData) -> Item:
        return SotmItem(self.player, d.name, self.item_name_to_id[d.name], d.category, base=d.base)

    def create_item(self, name: str) -> Item:
        if name == "Scion of Oblivaeon":
            return SotmItem(self.player, name, self.item_name_to_id[name], SotmCategory.Scion)
        else:
            item_data = self.find_data(name)
            if item_data is None:
                id = self.item_name_to_id.get(name, None)
                if id is None:
                    raise OptionError(f"Item {name} does not exist")
                return SotmItem(self.player, name, id, SotmCategory.Trap if (id >> 48) & 1 > 0 else SotmCategory.Filler)
            return SotmItem(self.player, name, self.item_name_to_id[name], item_data.category, base=item_data.base)

    def find_data(self, name: str) -> Optional[SotmData]:
        r = next((d for d in self.included() if d.name == name), None)
        if r is not None:
            return r
        return next((d for d in self.available() if d.name == name), None)

    def get_filler_item_name(self) -> str:
        name, is_trap = self.resolve_filler(True)
        return name

    def parse_filler_weights(self):
        self.filler_options = []
        self.filler_weights = []
        self.filler_weights_pos = []
        for current_filler in self.options.filler_weights.value:
            f_type = next((f for f in filler if f.name == current_filler.get("name")), None)
            if not f_type:
                raise OptionError(f"Filler {current_filler.name} does not exist")
            if current_filler.get("variant") == "pos":
                variant = 2
            elif current_filler.get("variant") == "neg":
                variant = 1
            elif current_filler.get("variant") == "both":
                variant = 3
            else:
                variant = (2 if f_type.name_pos else 0) | (1 if f_type.name_neg else 0)
            specificity = current_filler.get("specificity", 0)
            max = current_filler.get("max", None)
            min = current_filler.get("min", None)
            match f_type.type:
                case FillerType.Hero:
                    length = len(self.included_heroes)
                    if specificity == 2:
                        length += len(self.included_variants)
                case FillerType.Villain:
                    length = len(self.included_villains)
                case _:
                    length = 1
            weight = current_filler.get("weight")
            if (variant & 1) > 0:
                if not f_type.name_neg:
                    raise OptionError(f"Filler {f_type.name} does not have a negative version")
                self.filler_options.append(FillerOption(f_type.name_neg, f_type.type, True,
                                                        specificity, [max] * length if specificity > 0 else max, min))
                self.filler_weights.append(weight)
                self.filler_weights_pos.append(0)
            if (variant & 2) > 0:
                if not f_type.name_pos:
                    raise OptionError(f"Filler {f_type.name} does not have a positive version")
                self.filler_options.append(FillerOption(f_type.name_pos, f_type.type, False,
                                                        specificity, [max] * length if specificity > 0 else max, min))
                self.filler_weights.append(weight)
                self.filler_weights_pos.append(weight)

    def resolve_filler(self, force_pos: bool = False) -> (str, bool):
        [idx] = self.random.choices(range(len(self.filler_options)),
                                    self.filler_weights_pos if force_pos else self.filler_weights)
        chosen = self.filler_options[idx]
        if chosen.specificity == 0 or chosen.type == FillerType.Other:
            if chosen.remaining:
                chosen.remaining -= 1
                if chosen.remaining == 0:
                    self.filler_weights[idx] = 0
                    self.filler_weights_pos[idx] = 0
            return chosen.name, chosen.is_trap
        else:
            if any(chosen.remaining):
                [selected] = self.random.choices(range(len(chosen.remaining)), chosen.remaining)
                chosen.remaining[selected] -= 1
                if sum(chosen.remaining) == 0:
                    self.filler_weights[idx] = 0
                    self.filler_weights_pos[idx] = 0
            else:
                selected = self.random.randint(0, len(chosen.remaining) - 1)
            if chosen.type == FillerType.Hero:
                if chosen.specificity == 1:
                    specifier = f"Any {self.included_heroes[selected].name}"
                else:
                    if selected >= len(self.included_heroes):
                        selected -= len(self.included_heroes)
                        specifier = f"{self.included_variants[selected].name}"
                    else:
                        specifier = f"{self.included_heroes[selected].name}"
            else:
                specifier = f"{self.included_villains[selected].name}"
        return f"{chosen.name} ({specifier})", chosen.is_trap

    def resolve_pool_size(self):
        self.pool_size = []
        for (type, available) in (("villains", self.available_villains), ("environments", self.available_environments),
                                  ("heroes", self.available_heroes), ("variants", self.available_variants),
                                  ("contenders", self.available_contenders), ("gladiators", self.available_gladiators)):
            value = self.options.pool_size.value[type]
            if isinstance(value, dict):
                self.pool_size.append(self.random.randint(self.pool_size_value(value["min"], available),
                                                          self.pool_size_value(value["max"], available)))
            else:
                self.pool_size.append(self.pool_size_value(value, available))

    def pool_size_value(self, value: int | str, available: list) -> int:
        if isinstance(value, int):
            return value
        if value.endswith("%"):
            return math.floor(max(min(float(value[:-1]), 100.0), 0.0) / 100 * len(available))
        if value.endswith("%+"):
            return math.floor(max(min(float(value[:-2]), 100.0), 0.0) / 100 * self.total_pool_size)
        raise OptionError(f"Invalid pool size value {value}")

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: (self.villain_goal(state)
                                                                           and self.variant_goal(state)
                                                                           and self.scion_goal(state))

    def villain_goal(self, state) -> bool:
        if self.required_villains == 0:
            return True

        team_count = state.prog_items[self.player]["Team Villains"]

        return ((state.prog_items[self.player]["Villains"] + team_count if team_count >= 3 else 0)
                * self.max_points_per_villain >= self.required_villains)

    def variant_goal(self, state) -> bool:
        if self.required_variants == 0:
            return True
        return [v.rule(state, self.player) for v in self.possible_variants].count(True) >= self.required_variants

    def scion_goal(self, state) -> bool:
        if self.required_scions == 0:
            return True

        return (state.has("Scion of Oblivaeon", self.player, self.required_scions)
                and state.has("Environments", self.player, 5)
                and state.has("Unique Hero Thirds", self.player,
                              self.options.villain_difficulties.get("Oblivaeon", 3) * 3))

    def collect(self, state: CollectionState, item: SotmItem):
        changed = super().collect(state, item)
        match item.category:
            case SotmCategory.Hero:
                state.prog_items[self.player][f"Any {item.name}"] += 1
                if state.prog_items[self.player][f"Any {item.name}"] == 1:
                    state.prog_items[self.player]["Unique Hero Thirds"] += 3
                changed = True
            case SotmCategory.Variant:
                state.prog_items[self.player][f"Any {item.base}"] += 1
                if state.prog_items[self.player][f"Any {item.base}"] == 1:
                    state.prog_items[self.player]["Unique Hero Thirds"] += 3
                changed = True
            case item.category.Environment:
                state.prog_items[self.player]["Environments"] += 1
            case item.category.Villain | item.category.VillainVariant:
                state.prog_items[self.player]["Villains"] += 1
            case item.category.TeamVillain:
                state.prog_items[self.player]["Team Villains"] += 1
            case item.category.Contender:
                state.prog_items[self.player]["Unique Hero Thirds"] += 1
            case item.category.Gladiator:
                state.prog_items[self.player]["Gladiators"] += 1
                changed = True
        return changed

    def remove(self, state: CollectionState, item: SotmItem):
        changed = super().collect(state, item)
        match item.category:
            case SotmCategory.Hero:
                state.prog_items[self.player][f"Any {item.name}"] -= 1
                if state.prog_items[self.player][f"Any {item.name}"] == 0:
                    state.prog_items[self.player]["Unique Hero Thirds"] -= 3
                changed = True
            case SotmCategory.Variant:
                state.prog_items[self.player][f"Any {item.base}"] -= 1
                if state.prog_items[self.player][f"Any {item.base}"] == 0:
                    state.prog_items[self.player]["Unique Hero Thirds"] -= 3
                changed = True
            case item.category.Environment:
                state.prog_items[self.player]["Environments"] -= 1
            case item.category.Villain | item.category.VillainVariant:
                state.prog_items[self.player]["Villains"] -= 1
            case item.category.TeamVillain:
                state.prog_items[self.player]["Team Villains"] -= 1
            case item.category.Contender:
                state.prog_items[self.player]["Unique Hero Thirds"] -= 1
            case item.category.Gladiator:
                state.prog_items[self.player]["Gladiators"] -= 1
                changed = True
        return changed

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            "d": [
                self.required_scions,
                self.required_variants,
                self.required_villains,
                self.villain_points.normal,
                self.villain_points.advanced,
                self.villain_points.challenge,
                self.villain_points.ultimate,
                self.location_density.villain_normal,
                self.location_density.villain_advanced,
                self.location_density.villain_challenge,
                self.location_density.villain_ultimate,
                self.location_density.hero,
                self.location_density.environment,
                self.location_density.variant_unlock,
                self.options.filler_duration.value,
                {"false": 0, "individual": 1, "team": 2}[self.options.death_link.value]
            ]
        }

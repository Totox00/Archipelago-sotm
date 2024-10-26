import math
from typing import Dict, Set, Optional, NamedTuple

from BaseClasses import MultiWorld, Region, Item, Tutorial, ItemClassification
from Options import Toggle, OptionError

from worlds.AutoWorld import World, WebWorld

from .Items import SotmItem
from .Locations import SotmLocation
from .Options import SotmOptions, sotm_option_groups
from .Data import SotmSource, SotmData, SotmCategory, general_access_rule, data, difficulties, SotmState, \
    sources, FillerType, damage_types, filler, base_to_variants
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
    variant: int


class FillerOption:
    name: str
    type: FillerType
    is_trap: bool
    specificity: int
    damage_type: str
    remaining: Optional[int] | list[int] | list[None]
    min: Optional[int]

    def __init__(self, name, type, is_trap, specificity, damage_type, remaining, min):
        self.name = name
        self.type = type
        self.is_trap = is_trap
        self.specificity = specificity
        self.damage_type = damage_type
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
    data_version = 1
    base_id = 27181774

    enabled_sources: Set[SotmSource]

    available_villains: list[SotmData]
    available_heroes: list[SotmData]
    available_environments: list[SotmData]
    available_variants: list[SotmData]
    available_variant_unlocks: list[SotmData]

    state: SotmState
    included_villains: list[SotmData]
    included_heroes: list[SotmData]
    included_environments: list[SotmData]
    included_variants: list[SotmData]
    possible_variants: list[SotmData]

    total_pool_size: int
    total_locations: int
    total_items: int
    team_villains: int

    required_scions: int
    required_villains: int
    required_variants: int

    total_possible_villain_points: int
    max_points_per_villain: int
    total_possible_villain_points_duo_offset: int
    location_density: LocationDensity

    filler_options: list[FillerOption]
    filler_weights: list[int]
    filler_weights_pos: list[int]

    required_client_version = (0, 0, 1)
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = SotmItem.get_item_name_groups()
    location_name_groups = SotmLocation.get_location_name_groups()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.state = SotmState()
        self.total_items = 0
        self.total_locations = 0
        self.enabled_sources = set()
        self.included_villains = []
        self.included_heroes = []
        self.included_environments = []
        self.included_variants = []
        self.possible_variants = []

    def generate_early(self):
        for source, source_data in sources.items():
            if source_data["name"] in self.options.enabled_sets.value:
                self.enabled_sources.add(source)

        self.location_density = LocationDensity(
            self.options.location_density.value["villain"]["normal"],
            self.options.location_density.value["villain"]["advanced"],
            self.options.location_density.value["villain"]["challenge"],
            self.options.location_density.value["villain"]["ultimate"],
            self.options.location_density.value["environment"],
            self.options.location_density.value["variant"]
        )

        available = [d for d in data if (d.name not in self.options.exclude_from_pool.value)
                     and (False not in ((source in self.enabled_sources) for source in d.sources))]
        full_state = SotmState()
        full_state.items.update(d.name for d in available)
        self.available_villains = [d for d in available if d.category in
                                   (SotmCategory.Villain, SotmCategory.VillainVariant, SotmCategory.TeamVillain)]
        self.available_heroes = [d for d in available if d.category == SotmCategory.Hero]
        self.available_environments = [d for d in available if d.category == SotmCategory.Environment]
        self.available_variants = [d for d in available if d.category in
                                   (SotmCategory.Variant, SotmCategory.VillainVariant)]

        self.available_variant_unlocks = [d for d in self.available_variants
                                          if d.rule is not None and d.rule(full_state, self.player)]
        self.total_pool_size = len(available)

        self.max_points_per_villain = (
            self.options.villain_points.value["normal"]
            + self.options.villain_points.value["advanced"]
            + self.options.villain_points.value["challenge"]
            + self.options.villain_points.value["ultimate"]
        )
        self.total_possible_villain_points = len(self.available_villains) * self.max_points_per_villain

        self.total_possible_villain_points_duo_offset = (self.options.villain_points.value["challenge"]
                                                         + self.options.villain_points.value["ultimate"])

        if True in (v.name in ("Spite: Agent of Gloom", "Skinwalker Gloomweaver") for v in self.available_villains):
            self.total_possible_villain_points -= (self.options.villain_points.value["challenge"]
                                                   + self.options.villain_points.value["ultimate"])

        self.required_villains = min(self.options.required_villains.value, self.total_possible_villain_points)
        self.required_variants = min(self.options.required_variants.value, len(self.available_variant_unlocks))

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
        while len(self.possible_variants) < self.options.required_variants.value:
            needed = self.min_needed_for_variant(self.random.choice(self.available_variant_unlocks))
            for d in needed:
                self.include_data(d)

        # Ensure that if there are team villains, there are at least 3
        self.team_villains = len([v for v in self.included_villains if v.category == SotmCategory.TeamVillain])
        self.ensure_team_villains()

        # Add villains until there are enough for the starting and required villain counts
        while len(self.included_villains) < max(
                math.ceil(self.options.required_villains.value
                          / self.total_possible_villain_points)
                + (self.total_possible_villain_points_duo_offset
                   if [d.name in ("Spite: Agent of Gloom", "Skinwalker Gloomweaver")
                       for d in self.included_villains].count(True) == 2 else 0),
                self.options.starting_items.value["villains"]):
            self.include_data(chosen := self.random.choice(self.available_villains))
            if chosen.category == SotmCategory.TeamVillain:
                self.team_villains += 1
                self.ensure_team_villains()

        # Starting villains cannot be team villains
        while (len([d for d in self.included_villains if d.category != SotmCategory.TeamVillain])
               < self.options.starting_items.value["villains"]):
            available_villains = [d for d in self.available_villains if d.category != SotmCategory.TeamVillain]
            self.include_data(self.random.choice(available_villains))

        # Add environments until there are enough for the starting environment count
        while len(self.included_environments) < self.options.starting_items.value["environments"]:
            self.include_data(self.random.choice(self.available_environments))

        # Oblivaeon requires 5 environments if part of goal
        if self.options.required_scions.value > 0:
            while len(self.included_environments) < 5:
                self.include_data(self.random.choice(self.available_environments))

        # Add heroes and hero variants until there are enough for the start hero count
        # Make sure there are not too few due to some being variants of the same hero
        while (len(self.included_heroes) + len(self.included_variants)
               < self.options.starting_items.value["heroes"]):
            chosen = self.random.choice(self.available_heroes)
            if not self.state.has(f"Any {chosen.name}", self.player):
                self.include_data(chosen)

        # Add random items to included items until pool size is satisfied
        # Adjust for items added previously so weights reflect the full pool
        # Special case for full pool to avoid rounding errors (at least I think that's the cause?)
        if self.options.pool_size.value == 100:
            for d in self.available():
                self.include_data(d)
        else:
            adjust_villains = len(self.included_villains)
            adjust_environments = len(self.included_environments)
            adjust_heroes = len(self.included_heroes)
            adjust_variants = len(self.included_variants)

            types = ["villain", "environment", "hero", "variant"]
            weights = [self.options.item_weights.value[t] for t in types]

            while (self.total_items / self.total_pool_size) * 100 < self.options.pool_size.value:
                roll = self.random.choices(types, weights)

                chosen = None
                match roll:
                    case "villain":
                        if adjust_villains > 0:
                            adjust_villains -= 1
                        elif len(self.available_villains) > 0:
                            chosen = self.random.choice(self.available_villains)
                    case "environment":
                        if adjust_environments > 0:
                            adjust_environments -= 1
                        elif len(self.available_environments) > 0:
                            chosen = self.random.choice(self.available_environments)
                    case "hero":
                        if adjust_heroes > 0:
                            adjust_heroes -= 1
                        elif len(self.available_heroes) > 0:
                            chosen = self.random.choice(self.available_heroes)
                    case "variant":
                        if adjust_variants > 0:
                            adjust_variants -= 1
                        elif len(self.available_variants) > 0:
                            chosen = self.random.choice(self.available_variants)

                if chosen:
                    self.include_data(chosen)
                    if chosen.category == SotmCategory.TeamVillain:
                        self.team_villains += 1
                        if self.team_villains == 1:
                            adjust_villains += 2
                        elif self.team_villains == 2:
                            adjust_villains += 1

                        self.ensure_team_villains()

        # Add random items from included items to precollected until start counts are satisfied
        start_hero_bases = []
        start_hero_count = 0
        start_villains = []
        start_environments = []
        for name in self.options.start_inventory.value:
            d = next((d for d in data if d.name == name), None)
            if d is not None:
                match d.category:
                    case SotmCategory.Hero:
                        if d.name not in start_hero_bases:
                            start_hero_bases.append(d.name)
                            start_hero_count += 1
                    case SotmCategory.Variant:
                        if d.base not in start_hero_bases:
                            start_hero_bases.append(d.base)
                            start_hero_count += 1
                    case SotmCategory.Villain | SotmCategory.VillainVariant:
                        start_villains.append(d.name)
                    case SotmCategory.Environment:
                        start_environments.append(d.name)

        for _ in range(start_hero_count, self.options.starting_items.value["heroes"]):
            choices = ([d for d in self.included_heroes if d.name not in start_hero_bases]
                       + [d for d in self.included_variants if d.base not in start_hero_bases])
            chosen = self.random.choice(choices)
            self.multiworld.push_precollected(self.create_item_from_data(chosen))
            if chosen.category == SotmCategory.Hero:
                start_hero_bases.append(chosen.name)
            else:
                start_hero_bases.append(chosen.base)

        included_not_team_villains = [d for d in self.included_villains if d.category != SotmCategory.TeamVillain]
        for _ in range(len(start_villains), self.options.starting_items.value["villains"]):
            choices = [d for d in included_not_team_villains if d.name not in start_villains]
            chosen = self.random.choice(choices)
            self.multiworld.push_precollected(self.create_item_from_data(chosen))
            start_villains.append(chosen.name)

        for _ in range(len(start_environments), self.options.starting_items.value["environments"]):
            choices = [d for d in self.included_environments if d.name not in start_environments]
            chosen = self.random.choice(choices)
            self.multiworld.push_precollected(self.create_item_from_data(chosen))
            start_environments.append(chosen.name)

        self.parse_filler_weights()

    def available(self) -> list[SotmData]:
        return (self.available_villains + self.available_heroes + self.available_environments
                + [d for d in self.available_variants if d.category != SotmCategory.VillainVariant])

    def included(self) -> list[SotmData]:
        return (self.included_villains + self.included_heroes + self.included_environments
                + [d for d in self.included_variants if d.category != SotmCategory.VillainVariant])

    def include_data(self, d: SotmData) -> bool:
        if d.name in self.state.items:
            return True

        match d.category:
            case SotmCategory.Villain | SotmCategory.VillainVariant | SotmCategory.TeamVillain:
                if d not in self.available_villains:
                    return False
                self.available_villains.remove(d)
                self.included_villains.append(d)
                self.total_items += 1
                self.total_locations += (self.location_density.villain_normal
                                         + self.location_density.villain_advanced
                                         + self.location_density.villain_challenge
                                         + self.location_density.villain_ultimate)
            case SotmCategory.Environment:
                if d not in self.available_environments:
                    return False
                self.available_environments.remove(d)
                self.included_environments.append(d)
                self.total_items += 1
                self.total_locations += self.location_density.environment
            case SotmCategory.Hero:
                if d not in self.available_heroes:
                    return False
                self.available_heroes.remove(d)
                self.included_heroes.append(d)
                self.total_items += 1
            case SotmCategory.Variant:
                if d not in self.available_variants:
                    return False
                self.available_variants.remove(d)
                self.included_variants.append(d)
                self.total_items += 1

        self.state.items.add(d.name)

        if ((d.name == "Spite: Agent of Gloom" and "Gloomweaver Skinwalker" not in self.state.items)
                or (d.name == "Gloomweaver Skinwalker" and "Spite: Agent of Gloom" not in self.state.items)):
            self.total_locations -= (self.location_density.villain_challenge + self.location_density.villain_ultimate)

        for v in self.available_variant_unlocks:
            if v.rule(self.state, self.player):
                self.possible_variants.append(v)
                self.available_variant_unlocks.remove(v)
                self.total_locations += self.location_density.variant

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

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        general_access = Region("General Access", self.player, self.multiworld)
        self.multiworld.regions.append(general_access)

        menu.add_exits({"General Access", "General Access"},
                       {"General Access": lambda state: general_access_rule(state, self.player)})

        for base, variants in base_to_variants.items():
            if base in self.state.items or any(v in self.state.items for v in variants):
                event_loc = SotmLocation(self.player, f"Any {base}", None, SotmCategory.Event, menu,
                                         rule=lambda state, player, b=base, v=variants:
                                         state.has(b, player) or state.has_any(v, player))
                event_loc.place_locked_item(SotmItem(self.player, f"Any {base}", None, SotmCategory.Event))
                menu.locations.append(event_loc)

        duo = 0

        for villain in self.included_villains:
            for n in range(1, self.location_density.villain_normal + 1):
                name = f"{villain.name} - Normal #{n}"
                general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                villain.category, general_access, villain.name))
            for n in range(1, self.location_density.villain_advanced + 1):
                name = f"{villain.name} - Advanced #{n}"
                general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                villain.category, general_access, villain.name))

            if villain.name == "Spite: Agent of Gloom" or villain.name == "Skinwalker Gloomweaver":
                duo += 1
                if duo == 2:
                    for n in range(1, self.location_density.villain_challenge + 1):
                        name = f"Spite: Agent of Gloom and Skinwalker Gloomweaver - Challenge #{n}"
                        (general_access.locations
                         .append(SotmLocation(self.player, name, self.location_name_to_id[name], villain.category,
                                              general_access, rule=lambda state, player: state.has_all(
                                              ["Spite: Agent of Gloom", "Skinwalker Gloomweaver"], player))))
                    for n in range(1, self.location_density.villain_ultimate + 1):
                        name = f"Spite: Agent of Gloom and Skinwalker Gloomweaver - Ultimate #{n}"
                        (general_access.locations
                         .append(SotmLocation(self.player, name, self.location_name_to_id[name], villain.category,
                                              general_access, rule=lambda state, player: state.has_all(
                                              ["Spite: Agent of Gloom", "Skinwalker Gloomweaver"], player))))
            else:
                for n in range(1, self.location_density.villain_challenge + 1):
                    name = f"{villain.name} - Challenge #{n}"
                    general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                    villain.category, general_access, villain.name))
                for n in range(1, self.location_density.villain_ultimate + 1):
                    name = f"{villain.name} - Ultimate #{n}"
                    general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                    villain.category, general_access, villain.name))

        for environment in self.included_environments:
            for n in range(1, self.location_density.environment + 1):
                name = f"{environment.name} - Any Difficulty #{n}"
                general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                environment.category, general_access, environment.name))

        for variant in self.possible_variants:
            for n in range(1, self.location_density.variant + 1):
                name = f"{variant.name} - Unlock #{n}"
                general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                variant.category, general_access, rule=variant.rule))

    def create_items(self):
        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]
        items = []

        for villain in self.included_villains:
            if villain.name not in exclude:
                items.append(self.create_item_from_data(villain))

        for environment in self.included_environments:
            if environment.name not in exclude:
                items.append(self.create_item_from_data(environment))

        for hero in self.included_heroes:
            if hero.name not in exclude:
                items.append(self.create_item_from_data(hero))

        for variant in self.included_variants:
            if variant.name not in exclude:
                if variant.category == SotmCategory.Variant:
                    items.append(self.create_item_from_data(variant))

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
                        name = chosen.name.replace("[TYPE]", chosen.damage_type)
                        items.append(SotmItem(self.player, name, self.item_name_to_id[name],
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
                            name = f"{chosen.name.replace('[TYPE]', chosen.damage_type)} ({specifier})"
                            items.append(SotmItem(self.player, name, self.item_name_to_id[name],
                                                  SotmCategory.Trap if chosen.is_trap else SotmCategory.Filler))

        for _ in range(0, self.total_locations - len(items)):
            name, is_trap = self.resolve_filler()
            items.append(SotmItem(self.player, name, self.item_name_to_id[name],
                                  SotmCategory.Trap if is_trap else SotmCategory.Filler))

        self.multiworld.itempool.extend(items)

    def create_item_from_data(self, d: SotmData) -> Item:
        return SotmItem(self.player, d.name, self.item_name_to_id[d.name], d.category)

    def create_item(self, name: str) -> Item:
        if name == "Scion of Oblivaeon":
            category = SotmCategory.Scion
        else:
            category = next((d.category for d in data if d.name == name), SotmCategory.Filler)

        return SotmItem(self.player, name, self.item_name_to_id[name], category)

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
            else:
                variant = 3
            specificity = current_filler.get("specificity", 0)
            typed = current_filler.get("typed", False)
            max = current_filler.get("max", None)
            min = current_filler.get("min", None)
            match f_type.type:
                case FillerType.Hero:
                    length = len(self.included_heroes) if specificity == 1 else len(self.included_variants)
                case FillerType.Villain:
                    length = len(self.included_villains)
                case _:
                    length = 1
            weight = current_filler.get("weight")
            if typed:
                for damage_type in damage_types:
                    if (variant & 1) > 0:
                        if not f_type.name_neg:
                            raise OptionError(f"Filler {f_type.name} does not have a negative version")
                        self.filler_options.append(FillerOption(f_type.name_neg, f_type.type, True,
                                                                specificity, damage_type, [max] * length, min))
                        self.filler_weights.append(weight)
                        self.filler_weights_pos.append(0)
                    if (variant & 2) > 0:
                        if not f_type.name_pos:
                            raise OptionError(f"Filler {f_type.name} does not have a positive version")
                        self.filler_options.append(FillerOption(f_type.name_pos, f_type.type, False,
                                                                specificity, damage_type, [max] * length, min))
                        self.filler_weights.append(weight)
                        self.filler_weights_pos.append(weight)
            else:
                if (variant & 1) > 0:
                    if not f_type.name_neg:
                        raise OptionError(f"Filler {f_type.name} does not have a negative version")
                    self.filler_options.append(FillerOption(f_type.name_neg, f_type.type, True,
                                                            specificity, "",
                                                            [max] * length if specificity > 0 else max, min))
                    self.filler_weights.append(weight)
                    self.filler_weights_pos.append(0)
                if (variant & 2) > 0:
                    if not f_type.name_pos:
                        raise OptionError(f"Filler {f_type.name} does not have a positive version")
                    self.filler_options.append(FillerOption(f_type.name_pos, f_type.type, False,
                                                            specificity, "",
                                                            [max] * length if specificity > 0 else max, min))
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
            return chosen.name.replace("[TYPE]", chosen.damage_type), chosen.is_trap
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
                    specifier = f"{self.included_variants[selected].name}"
            else:
                specifier = f"{self.included_villains[selected].name}"
        return f"{chosen.name.replace('[TYPE]', chosen.damage_type)} ({specifier})", chosen.is_trap

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: (self.villain_goal(state)
                                                                           and self.variant_goal(state)
                                                                           and self.scion_goal(state))

    def villain_goal(self, state) -> bool:
        if self.required_villains == 0:
            return True

        offset = (self.total_possible_villain_points_duo_offset
                  if state.has("Spite: Agent of Gloom", self.player)
                  and state.has("Skinwalker Gloomweaver", self.player) else 0)

        return (([state.has(v.name, self.player) for v in self.included_villains].count(True)
                * self.max_points_per_villain - offset) >= self.required_villains)

    def variant_goal(self, state) -> bool:
        if self.required_variants == 0:
            return True

        return ([v.rule(state, self.player) for v in self.possible_variants].count(True)
                >= self.required_variants)

    def scion_goal(self, state) -> bool:
        if self.required_scions == 0:
            return True
        return (state.has("Scion of Oblivaeon", self.player, self.required_scions)
                and [state.has(v.name, self.player) for v in self.included_environments].count(True) >= 5)

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            "required_scions": self.required_scions,
            "required_variants": self.required_variants,
            "required_villains": self.required_villains,
            "villain_difficulty_points": [
                self.options.villain_points.value["normal"],
                self.options.villain_points.value["advanced"],
                self.options.villain_points.value["challenge"],
                self.options.villain_points.value["ultimate"]
            ],
            "locations_per": [
                self.location_density.villain_normal,
                self.location_density.villain_advanced,
                self.location_density.villain_challenge,
                self.location_density.villain_ultimate,
                self.location_density.environment,
                self.location_density.variant
            ],
            "death_link": {"false": 0, "individual": 1, "team": 2}[self.options.death_link.value]
        }

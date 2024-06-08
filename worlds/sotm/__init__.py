import math
from typing import Dict, Set, Optional

from BaseClasses import MultiWorld, Region, Item, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld

from .Items import SotmItem
from .Locations import SotmLocation
from .Options import SotmOptions, sotm_option_groups
from .Data import SotmSource, SotmData, SotmCategory, general_access_rule, data, has_all_of, difficulties, SotmState, \
    any_variant, fanmade_sources, has_fanmade


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
    total_possible_villain_points_duo_offset: int

    required_client_version = (0, 0, 1)
    item_name_to_id = SotmItem.get_name_to_id()
    location_name_to_id = SotmLocation.get_name_to_id()
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
        if self.options.enable_rook_city == Toggle.option_true:
            self.enabled_sources.add(SotmSource.RookCity)
        if self.options.enable_infernal_relics == Toggle.option_true:
            self.enabled_sources.add(SotmSource.InfernalRelics)
        if self.options.enable_shattered_timelines == Toggle.option_true:
            self.enabled_sources.add(SotmSource.ShatteredTimelines)
        if self.options.enable_wrath_of_the_cosmos == Toggle.option_true:
            self.enabled_sources.add(SotmSource.WrathOfTheCosmos)
        if self.options.enable_vengeance == Toggle.option_true:
            self.enabled_sources.add(SotmSource.Vengeance)
        if self.options.enable_villains_of_the_multiverse == Toggle.option_true:
            self.enabled_sources.add(SotmSource.VillainsOfTheMultiverse)
        if self.options.enable_oblivaeon == Toggle.option_true:
            self.enabled_sources.add(SotmSource.Oblivaeon)
        if self.options.enable_unity == Toggle.option_true:
            self.enabled_sources.add(SotmSource.Unity)
        if self.options.enable_the_scholar == Toggle.option_true:
            self.enabled_sources.add(SotmSource.TheScholar)
        if self.options.enable_guise == Toggle.option_true:
            self.enabled_sources.add(SotmSource.Guise)
        if self.options.enable_stuntman == Toggle.option_true:
            self.enabled_sources.add(SotmSource.Stuntman)
        if self.options.enable_benchmark == Toggle.option_true:
            self.enabled_sources.add(SotmSource.Benchmark)
        if self.options.enable_the_void_guard == Toggle.option_true:
            self.enabled_sources.add(SotmSource.TheVoidGuard)
        if self.options.enable_ambuscade == Toggle.option_true:
            self.enabled_sources.add(SotmSource.Ambuscade)
        if self.options.enable_miss_information == Toggle.option_true:
            self.enabled_sources.add(SotmSource.MissInformation)
        if self.options.enable_wager_master == Toggle.option_true:
            self.enabled_sources.add(SotmSource.WagerMaster)
        if self.options.enable_chokepoint == Toggle.option_true:
            self.enabled_sources.add(SotmSource.Chokepoint)
        if self.options.enable_silver_gulch_1883 == Toggle.option_true:
            self.enabled_sources.add(SotmSource.SilverGulch1883)
        if self.options.enable_the_final_wasteland == Toggle.option_true:
            self.enabled_sources.add(SotmSource.TheFinalWasteland)
        if self.options.enable_omnitron_iv == Toggle.option_true:
            self.enabled_sources.add(SotmSource.OmnitronIV)
        if self.options.enable_the_celestial_tribunal == Toggle.option_true:
            self.enabled_sources.add(SotmSource.TheCelestialTribunal)
        if self.options.enable_the_cauldron == Toggle.option_true:
            self.enabled_sources.add(SotmSource.TheCauldron)
        if self.options.enable_cauldron_promos == Toggle.option_true:
            self.enabled_sources.add(SotmSource.CauldronPromos)

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

        self.total_possible_villain_points = len(self.available_villains) * (
            self.options.villain_points_normal.value
            + self.options.villain_points_advanced.value
            + self.options.villain_points_challenge.value
            + self.options.villain_points_ultimate.value
        )

        self.total_possible_villain_points_duo_offset = (self.options.villain_points_challenge.value
                                                         + self.options.villain_points_ultimate.value)

        if True in (v.name in ("Spite: Agent of Gloom", "Skinwalker Gloomweaver") for v in self.available_villains):
            self.total_possible_villain_points -= (self.options.villain_points_challenge.value
                                                   + self.options.villain_points_ultimate.value)

        self.required_villains = min(self.options.required_villains.value, self.total_possible_villain_points)
        self.required_variants = min(self.options.required_variants.value, len(self.available_variant_unlocks))

        # Add starting items to pool
        starting_names = [item for item in self.options.start_inventory.value]
        for d in self.available():
            if d.name in starting_names:
                starting_names.remove(d.name)
                self.include_data(d)

        if len(starting_names) > 0:
            raise RuntimeError(
                f"Item {starting_names[0]} is marked as a starting item but does not exist with enabled sources")

        for item in self.options.include_in_pool.value:
            item_data = self.find_data(item)
            if item_data is None:
                raise RuntimeError(f"Unable to find data for item {item}")
            self.include_data(item_data)
        for variant in self.options.include_variants_in_pool.value:
            variant_data = self.find_data(variant)
            if variant_data is None:
                raise RuntimeError(f"Unable to find data for variant {variant}")
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
                self.options.start_villains.value):
            self.include_data(chosen := self.random.choice(self.available_villains))
            if chosen.category == SotmCategory.TeamVillain:
                self.team_villains += 1
                self.ensure_team_villains()

        # Starting villains cannot be team villains
        while (len([d for d in self.included_villains if d.category != SotmCategory.TeamVillain])
               < self.options.start_villains.value):
            available_villains = [d for d in self.available_villains if d.category != SotmCategory.TeamVillain]
            self.include_data(self.random.choice(available_villains))

        # Add environments until there are enough for the starting environment count
        while len(self.included_environments) < self.options.start_environments.value:
            self.include_data(self.random.choice(self.available_environments))

        # Oblivaeon requires 5 environments if part of goal
        if self.options.required_scions.value > 0:
            while len(self.included_environments) < 5:
                self.include_data(self.random.choice(self.available_environments))

        # Add heroes and hero variants until there are enough for the start hero count
        # Make sure there are not too few due to some being variants of the same hero
        offset = 0
        while len(self.included_heroes) + len(self.included_variants) < self.options.start_heroes.value + offset:
            chosen = self.random.choice(self.available_heroes)
            if chosen.category == SotmCategory.Hero:
                if any_variant(chosen.name, self.state, self.player):
                    offset += 1
            else:
                if any_variant(chosen.base, self.state, self.player):
                    offset += 1
            self.include_data(chosen)

        # Add random items to included items until pool size is satisfied
        # Adjust for items added previously so weights reflect the full pool
        adjust_villains = len(self.included_villains)
        adjust_environments = len(self.included_environments)
        adjust_heroes = len(self.included_heroes)
        adjust_variants = len(self.included_variants)
        weights = [self.options.villain_weight.value, self.options.environment_weight.value,
                   self.options.hero_weight.value, self.options.variant_weight.value]
        weight_boundaries = [sum(weights[0:i]) for i in range(1, 5)]
        while (self.total_items / self.total_pool_size) * 100 < self.options.pool_size.value:
            roll = self.random.randint(0, weight_boundaries[3] - 1)
            chosen = None
            if roll < weight_boundaries[0]:
                if adjust_villains > 0:
                    adjust_villains -= 1
                elif len(self.available_villains) > 0:
                    chosen = self.random.choice(self.available_villains)
            elif roll < weight_boundaries[1]:
                if adjust_environments > 0:
                    adjust_environments -= 1
                elif len(self.available_environments) > 0:
                    chosen = self.random.choice(self.available_environments)
            elif roll < weight_boundaries[2]:
                if adjust_heroes > 0:
                    adjust_heroes -= 1
                elif len(self.available_heroes) > 0:
                    chosen = self.random.choice(self.available_heroes)
            else:
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

        for _ in range(start_hero_count, self.options.start_heroes.value):
            choices = ([d for d in self.included_heroes if d.name not in start_hero_bases]
                       + [d for d in self.included_variants if d.base not in start_hero_bases])
            chosen = self.random.choice(choices)
            self.multiworld.push_precollected(self.create_item_from_data(chosen))
            if chosen.category == SotmCategory.Hero:
                start_hero_bases.append(chosen.name)
            else:
                start_hero_bases.append(chosen.base)

        included_not_team_villains = [d for d in self.included_villains if d.category != SotmCategory.TeamVillain]
        for _ in range(len(start_villains), self.options.start_villains.value):
            choices = [d for d in included_not_team_villains if d.name not in start_villains]
            chosen = self.random.choice(choices)
            self.multiworld.push_precollected(self.create_item_from_data(chosen))
            start_villains.append(chosen.name)

        for _ in range(len(start_environments), self.options.start_environments.value):
            choices = [d for d in self.included_environments if d.name not in start_environments]
            chosen = self.random.choice(choices)
            self.multiworld.push_precollected(self.create_item_from_data(chosen))
            start_environments.append(chosen.name)

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
                self.total_locations += (self.options.locations_per_villain_normal.value
                                         + self.options.locations_per_villain_advanced.value
                                         + self.options.locations_per_villain_challenge.value
                                         + self.options.locations_per_villain_ultimate.value)
            case SotmCategory.Environment:
                if d not in self.available_environments:
                    return False
                self.available_environments.remove(d)
                self.included_environments.append(d)
                self.total_items += 1
                self.total_locations += self.options.locations_per_environment.value
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
            self.total_locations -= (self.options.locations_per_villain_challenge.value
                                     + self.options.locations_per_villain_ultimate.value)

        for v in self.available_variant_unlocks:
            if v.rule(self.state, self.player):
                self.possible_variants.append(v)
                self.available_variant_unlocks.remove(v)
                self.total_locations += self.options.locations_per_variant.value

        return True

    def include_variant_unlock(self, variant: SotmData):
        if variant in self.possible_variants:
            return
        for d in self.min_needed_for_variant(variant):
            self.include_data(d)

    def min_needed_for_variant(self, variant: SotmData) -> list[SotmData]:
        min_needed = [d for d in self.available()]
        test_state = SotmState()
        test_state.items.update([d.name for d in min_needed])
        while True:
            can_be_removed = []
            for d in min_needed:
                if d.name not in self.state.items:
                    test_state.items.remove(d.name)
                    if variant.rule(test_state, self.player):
                        can_be_removed.append(d)
                    test_state.items.add(d.name)
            if len(can_be_removed) == 0:
                return [d for d in min_needed if d.name not in self.state.items]
            else:
                removed = self.random.choice(can_be_removed)
                min_needed.remove(removed)
                test_state.items.remove(removed.name)

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

        duo = 0

        for villain in self.included_villains:
            for n in range(1, self.options.locations_per_villain_normal.value + 1):
                name = f"{villain.name} - Normal #{n}"
                general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                villain.category, general_access, villain.name))
            for n in range(1, self.options.locations_per_villain_advanced.value + 1):
                name = f"{villain.name} - Advanced #{n}"
                general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                villain.category, general_access, villain.name))

            if villain.name == "Spite: Agent of Gloom" or villain.name == "Skinwalker Gloomweaver":
                duo += 1
                if duo == 2:
                    for n in range(1, self.options.locations_per_villain_challenge.value + 1):
                        name = f"Spite: Agent of Gloom and Skinwalker Gloomweaver - Challenge #{n}"
                        (general_access.locations
                         .append(SotmLocation(self.player, name, self.location_name_to_id[name], villain.category,
                                              general_access, rule=lambda state, player: has_all_of(
                                                  ["Spite: Agent of Gloom", "Skinwalker Gloomweaver"], state, player))))
                    for n in range(1, self.options.locations_per_villain_ultimate.value + 1):
                        name = f"Spite: Agent of Gloom and Skinwalker Gloomweaver - Ultimate #{n}"
                        (general_access.locations
                         .append(SotmLocation(self.player, name, self.location_name_to_id[name], villain.category,
                                              general_access, rule=lambda state, player: has_all_of(
                                                  ["Spite: Agent of Gloom", "Skinwalker Gloomweaver"], state, player))))
            else:
                for n in range(1, self.options.locations_per_villain_challenge.value + 1):
                    name = f"{villain.name} - Challenge #{n}"
                    general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                    villain.category, general_access, villain.name))
                for n in range(1, self.options.locations_per_villain_ultimate.value + 1):
                    name = f"{villain.name} - Ultimate #{n}"
                    general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                    villain.category, general_access, villain.name))

        for environment in self.included_environments:
            for n in range(1, self.options.locations_per_environment.value + 1):
                name = f"{environment.name} - Any Difficulty #{n}"
                general_access.locations.append(SotmLocation(self.player, name, self.location_name_to_id[name],
                                                environment.category, general_access, environment.name))

        for variant in self.possible_variants:
            for n in range(1, self.options.locations_per_variant.value + 1):
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
            total_portion = self.options.required_scions.value + self.options.extra_scions.value
            if total_portion > 1000:
                total_portion = 1000
            total_scions = math.floor((self.total_locations - len(items)) * total_portion / 1000)
            self.required_scions = math.floor(total_scions * self.options.required_scions.value
                                              / (self.options.required_scions.value + self.options.extra_scions.value))
        else:
            total_scions = self.options.required_scions.value + self.options.extra_scions.value
            self.required_scions = self.options.required_scions.value

        for i in range(0, total_scions):
            items.append(SotmItem(self.player, "Scion of Oblivaeon", self.item_name_to_id["Scion of Oblivaeon"],
                                  SotmCategory.Scion, ItemClassification.progression_skip_balancing
                                  if i < self.required_scions else ItemClassification.useful))

        for _ in range(0, self.total_locations - len(items)):
            items.append(self.create_item("1 Undo"))

        self.multiworld.itempool.extend(items)

    def create_item_from_data(self, d: SotmData) -> Item:
        if has_fanmade(d.sources) and (d.category == SotmCategory.Hero or d.category == SotmCategory.Variant):
            return SotmItem(self.player, d.name, self.item_name_to_id[d.name], d.category, ItemClassification.useful)

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
        return "1 Undo"

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: (self.villain_goal(state)
                                                                           and self.variant_goal(state)
                                                                           and self.scion_goal(state))

    def villain_goal(self, state) -> bool:
        if self.options.required_villains.value == 0:
            return True

        offset = (self.total_possible_villain_points_duo_offset
                  if state.has("Spite: Agent of Gloom", self.player)
                  and state.has("Skinwalker Gloomweaver", self.player) else 0)

        return ([state.has(v.name, self.player) for v in self.included_villains].count(True)
                * self.total_possible_villain_points - offset >= self.options.required_villains.value)

    def variant_goal(self, state) -> bool:
        if self.options.required_variants.value == 0:
            return True

        return ([v.rule(state, self.player) for v in self.possible_variants].count(True)
                >= self.options.required_variants.value)

    def scion_goal(self, state) -> bool:
        if self.required_scions == 0:
            return True
        return (state.has("Scion of Oblivaeon", self.player, self.required_scions)
                and [state.has(v.name, self.player) for v in self.included_environments].count(True) >= 5)

    def fill_slot_data(self) -> Dict[str, object]:
        return {
            "required_scions": self.required_scions,
            "required_variants": self.options.required_variants.value,
            "required_villains": self.options.required_villains.value,
            "villain_difficulty_points":
                [self.options.villain_points_normal.value, self.options.villain_points_advanced.value,
                 self.options.villain_points_challenge.value, self.options.villain_points_ultimate.value],
            "locations_per": [
                self.options.locations_per_villain_normal.value,
                self.options.locations_per_villain_advanced.value,
                self.options.locations_per_villain_challenge.value,
                self.options.locations_per_villain_ultimate.value,
                self.options.locations_per_environment.value,
                self.options.locations_per_variant.value]
        }

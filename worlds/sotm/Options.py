from dataclasses import dataclass

from schema import Schema, And, Optional

from Options import Toggle, Range, Choice, PerGameCommonOptions, ItemSet, OptionDict, OptionSet, OptionGroup, \
    OptionList
from worlds.sotm.Data import sources, data, SotmCategory, filler


class EnabledSets(OptionSet):
    """
    Specify all sets that content can be used for. Content from the base game is always included.
    """
    display_name = "Enabled Sets"
    default = frozenset(source["name"] for source in sources.values() if source["default"])
    valid_keys = [source["name"] for source in sources.values()]


class SeparateVariantItems(Choice):
    """Separates hero variants into their own items instead of being unlocked with the hero
    Not Starting makes it so your starting heroes are never variants
    Villain variants are always separate"""
    display_name = "Separate Variant Items"
    option_enable = "enable"
    option_disable = "disable"
    option_not_starting = "not_starting"
    default = "enable"


class RequiredVillains(Range):
    """The number of villains that must be defeated in order to goal"""
    display_name = "Required Villains"
    range_start = 0
    range_end = [d.category in (SotmCategory.Villain, SotmCategory.TeamVillain, SotmCategory.VillainVariant)
                 for d in data].count(True) * 40 - 20
    default = 0


class VillainPoints(OptionDict):
    """
    The number of points beating a villain counts as for the required villains. This is cumulative
    If you want a difficulty to award no additional points, set it to 0 (Do not delete the entry outright!).
    To make difficulty irrelevant, set normal to 1 and all else to 0.
    """
    display_name = "Villain Points"
    schema = Schema({
        difficulty: And(int, lambda n: n >= 0)
        for difficulty in ["normal", "advanced", "challenge", "ultimate"]
    })
    default = {
        "normal": 1,
        "advanced": 0,
        "challenge": 0,
        "ultimate": 0
    }


class RequiredVariants(Range):
    """The number of variant unlock conditions that must be fulfilled in order to goal"""
    display_name = "Required Variants"
    range_start = 0
    range_end = [d.category in (SotmCategory.Variant, SotmCategory.VillainVariant) for d in data].count(True)
    default = 0


class RequiredScions(Range):
    """The number of scions that must be received before fighting Oblivaeon"""
    display_name = "Required Scions"
    range_start = 0
    range_end = 1000
    default = 10


class ScionsAreRelative(Toggle):
    """Makes it so Required Scions instead dictates how large a portion of filler items are required scions
    1000 means that all are replaced"""
    display_name = "Scions are Relative"


class PoolSize(Range):
    """The minimum portion of the enabled content that is included in the rando
    Other options might cause this to be exceeded"""
    display_name = "Pool Size"
    range_start = 1
    range_end = 100
    default = 100


class IncludeInPool(ItemSet):
    """Items that will always be included in the pool.
    This should be used if plando or priority locations for specific items or locations are used"""
    display_name = "Include in Pool"


class IncludeVariantsInPool(ItemSet):
    """Variants that will always be unlockable given the items in the pool.
    This should be used if plando or priority locations for specific locations are used"""
    display_name = "Include Variants in Pool"


class ExcludeFromPool(ItemSet):
    """Items that will never be included in the pool."""
    display_name = "Exclude from Pool"


class ItemWeights(OptionDict):
    """
    Specify the weights determining the weights for different item types.
    If you want no items of a type to be added to the item pool, set it to 0 (Do not delete the entry outright!).
    This only dictates additional items added after items required for goal or that are specified to always be included.
    """
    display_name = "Item Weights"
    schema = Schema({
        item: And(int, lambda n: n >= 0)
        for item in ["villain", "environment", "hero", "variant"]
    })
    default = {
        "villain": 10,
        "environment": 20,
        "hero": 30,
        "variant": 60
    }


class FillerWeights(OptionList):
    """
    Specify a weighted list of filler configurations to use.
    Each entry must contain a name and a weight.
    The name must be one of the following:
    - StartHandsize
    - HeroHp
    - Mulligan
    - HeroDamageDealt
    - HeroDamageTaken
    - HeroCardPlay
    - HeroPower
    - HeroCardDraw
    - VillainHp
    - VillainDamageDealt
    - VillainDamageTaken
    - VillainCardPlays
    - VillainStartCardPlays
    - HeroCannotPlay
    - HeroCannotPower
    - HeroCannotDraw
    - HeroCannotDamage
    - Scion
    The weight must be >=0
    There are also several optional entries that can be included:
    - min: The minimum number of this filler that will be added to the pool.
      For an exact number the weight can be set to 0
    - max: The maximum number of this filler that will be added to the pool.
      The total weight of all filler with no max value must be >0
    - variant: Can be "pos", "neg", or "both". Defaults to "both".
      Specifies if the positive or negative variant of this filler is to be used.
      All filler types do not have both variants.
    - specificity: Can be 0, 1, or 2. Defaults to 0.
      Specifies if the filler affects
      0 - all items,
      1 - a specific hero/villain, or
      2 - a specific hero variant
    - typed: Can be true or false. Defaults to false.
      Specifies if the filler affects all damage or only damage of a specific type.
      Only does something for damage-related filler.
    """
    display_name = "Filler Weights"
    schema = Schema([{
        "name": lambda n: any(n == f.name for f in filler),
        "weight": And(int, lambda n: n >= 0),
        Optional("min"): And(int, lambda n: n >= 0),
        Optional("max"): And(int, lambda n: n >= 0),
        Optional("variant"): lambda s: s in ("pos", "neg", "both"),
        Optional("specificity"): And(int, lambda n: n in (0, 1, 2)),
        Optional("typed"): bool,
    }])
    default = [
        {
            "name": "HeroHp",
            "weight": 5
        },
        {
            "name": "StartHandsize",
            "weight": 4,
            "variant": "pos",
            "specificity": 1
        },
        {
            "name": "StartHandsize",
            "weight": 2,
            "variant": "neg",
            "specificity": 1,
            "max": 3
        },
        {
            "name": "Mulligan",
            "weight": 1,
            "variant": "pos",
            "specificity": 1
        },
        {
            "name": "HeroDamageDealt",
            "weight": 2,
            "variant": "pos",
            "specificity": 1,
            "max": 3
        },
        {
            "name": "HeroDamageDealt",
            "weight": 1,
            "variant": "neg",
            "specificity": 1,
            "max": 3
        },
        {
            "name": "HeroDamageTaken",
            "weight": 1,
            "variant": "pos",
            "specificity": 1,
            "max": 3
        },
        {
            "name": "HeroDamageTaken",
            "weight": 2,
            "variant": "neg",
            "specificity": 1,
            "max": 3
        },
        {
            "name": "HeroPower",
            "weight": 2,
            "variant": "pos",
            "specificity": 1,
            "max": 2
        },
        {
            "name": "HeroPower",
            "weight": 1,
            "variant": "neg",
            "specificity": 1,
            "max": 1
        },
        {
            "name": "HeroCardDraw",
            "weight": 3,
            "variant": "pos",
            "specificity": 1,
            "max": 2
        },
        {
            "name": "HeroCardDraw",
            "weight": 1,
            "variant": "neg",
            "specificity": 1,
            "max": 1
        },
        {
            "name": "VillainHp",
            "weight": 5
        },
        {
            "name": "VillainDamageTaken",
            "weight": 2,
            "variant": "pos",
            "max": 2
        },
        {
            "name": "VillainDamageTaken",
            "weight": 1,
            "variant": "neg",
            "max": 2
        },
        {
            "name": "VillainDamageDealt",
            "weight": 2,
            "max": 3
        },
        {
            "name": "VillainCardPlays",
            "weight": 1,
            "variant": "neg",
            "max": 1
        },
        {
            "name": "VillainStartCardPlays",
            "weight": 3,
            "variant": "neg",
            "max": 3
        }
    ]


class LocationDensity(OptionDict):
    """
    Specify the number of items placed at each location.
    If you want no items to be placed at a location, set it to 0 (Do not delete the entry outright!).
    Each location can have at most 5 items.
    """
    display_name = "Location Density"
    schema = Schema({
        "villain": {
            "normal": And(int, lambda n: 0 <= n <= 5),
            "advanced": And(int, lambda n: 0 <= n <= 5),
            "challenge": And(int, lambda n: 0 <= n <= 5),
            "ultimate": And(int, lambda n: 0 <= n <= 5)
        },
        "environment": And(int, lambda n: 0 <= n <= 5),
        "variant": And(int, lambda n: 0 <= n <= 5),
    })
    default = {
        "villain": {
            "normal": 1,
            "advanced": 1,
            "challenge": 1,
            "ultimate": 1
        },
        "environment": 1,
        "variant": 1,
    }


class StartingItems(OptionDict):
    """
    Specify the number of each type of item you start with.
    If you want to start with no items of a type, set it to 0 (Do not delete the entry outright!).
    No locations are available until you have at least 3 heroes, 1 environment, and either 1 villain or 3 team villains.
    """
    display_name = "Starting Items"
    schema = Schema({
        "heroes": And(int, lambda n: n >= 0),
        "villains": And(int, lambda n: n >= 0),
        "environments": And(int, lambda n: n >= 0),
    })
    default = {
        "heroes": 5,
        "villains": 2,
        "environments": 2
    }


class DeathLink(Choice):
    """
    When you die, everyone dies. Of course the reverse is true too.
    If set to "individual", a death is sent when a hero is incapacitated
    and a received death results in the incapacitation of the hero with the lowest hp.
    If set to "team", a death is sent when all heroes are incapacitated
    and a received death results in losing the current game.
    """
    display_name = "Death Link"
    option_false = "false"
    option_individual = "individual"
    option_team = "team"
    default = "false"


@dataclass
class SotmOptions(PerGameCommonOptions):
    enabled_sets: EnabledSets
    # Not yet implemented, current implementation is equivalent to if this is set to "enable"
    # separate_variant_items: SeparateVariantItems
    required_villains: RequiredVillains
    villain_points: VillainPoints
    required_variants: RequiredVariants
    required_scions: RequiredScions
    scions_are_relative: ScionsAreRelative
    pool_size: PoolSize
    include_in_pool: IncludeInPool
    include_variants_in_pool: IncludeVariantsInPool
    exclude_from_pool: ExcludeFromPool
    item_weights: ItemWeights
    filler_weights: FillerWeights
    location_density: LocationDensity
    starting_items: StartingItems
    death_link: DeathLink


sotm_option_groups = [
    OptionGroup("Item Pool", [EnabledSets, PoolSize, IncludeInPool, IncludeVariantsInPool, ExcludeFromPool,
                              ItemWeights, FillerWeights]),
    OptionGroup("Goal", [RequiredVillains, VillainPoints, RequiredVariants, RequiredScions, ScionsAreRelative]),
    OptionGroup("Misc", [LocationDensity, StartingItems, DeathLink]),
]

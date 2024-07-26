from dataclasses import dataclass

from schema import Schema, And

from Options import Toggle, Range, Choice, PerGameCommonOptions, ItemSet, OptionDict, OptionSet, OptionGroup
from worlds.sotm.Data import sources


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
    range_end = 74 * 40 - 20
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
    """The number of variants that must be defeated in order to goal"""
    display_name = "Required Variants"
    range_start = 0
    range_end = 67
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


class FillerWeights(OptionDict):
    """
    Specify the weights determining the weights for different item types.
    Unspecified types default to weight 0 and can be safely excluded, but the total weight must be >0.
    Each entry consists of a filler type and zero or more modifiers, separated by a ;
    Valid filler types are:
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
    "any" and "all" can also be used to refer to any filler other than extra Scions
    Valid modifiers are:
    - +: Only the helpful version of the filler (note that some modifiers do not have a helpful version)
    - -: Only the harmful version of the filler (note that some modifiers do not have a harmful version)
    - *: Filler only affects a specific hero or villain
    - **: Filler only affects a specific hero variant
    - T: Filler only affects a specific damage type
    """
    display_name = "Trap Weights"
    schema = Schema({str: And(int, lambda n: n >= 0)})
    default = {
        "HeroHp;*": 5,
        "StartHandsize;+*": 4,
        "StartHandsize;-*": 2,
        "Mulligan;+*": 1,
        "HeroDamageDealt;+*": 2,
        "HeroDamageDealt;-*": 1,
        "HeroDamageTaken;+*": 1,
        "HeroDamageTaken;-*": 2,
        "HeroPower;+*": 2,
        "HeroPower;-*": 1,
        "HeroCardDraw;+*": 3,
        "HeroCardDraw;-*": 1,
        "VillainHp;": 5,
        "VillainDamageTaken;+": 2,
        "VillainDamageTaken;-": 1,
        "VillainDamageDealt;": 2,
        "VillainCardPlays;-": 1,
        "VillainStartCardPlays;-": 3,
    }


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


sotm_option_groups = [
    OptionGroup("Item Pool", [EnabledSets, PoolSize, IncludeInPool, IncludeVariantsInPool, ExcludeFromPool,
                              ItemWeights, FillerWeights]),
    OptionGroup("Goal", [RequiredVillains, VillainPoints, RequiredVariants, RequiredScions, ScionsAreRelative]),
    OptionGroup("Misc", [LocationDensity, StartingItems]),
]

from dataclasses import dataclass

from schema import Schema, And, Optional, Or

from Options import Toggle, Range, Choice, PerGameCommonOptions, ItemSet, OptionDict, OptionSet, OptionGroup, \
    OptionList
from worlds.sotm.Data import sources, data, SotmCategory, filler, packs, enabled_sets_doc


class EnabledSets(OptionSet):
    display_name = "Enabled Sets"
    default = frozenset(["Official"])
    valid_keys = [source["name"] for source in sources.values()] + [pack["name"] for pack in packs.values()]


EnabledSets.__doc__ = enabled_sets_doc


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
    range_end = 65535
    default = 10


class ScionsAreRelative(Toggle):
    """Makes it so Required Scions instead dictates how large a portion of filler items are required scions
    1000 means that all are replaced"""
    display_name = "Scions are Relative"


class PoolSize(OptionDict):
    """The minimum quantity of each kind of item that is included in the rando
    Other options might cause this to be exceeded
    Use X% to include a portion of all available items of that kind
    Use a min and max value to use a random value in that range
    """
    display_name = "Pool Size"
    schema = Schema({
        item: Or(And(int, lambda n: n >= 0), str,
                 Schema({"min": Or(And(int, lambda n: n >= 0), str),
                         "max": Or(And(int, lambda n: n >= 0), str)}))
        for item in ["villains", "environments", "heroes", "variants", "contenders", "gladiators"]
    })
    default = {
        "villains": "100%",
        "environments": "100%",
        "heroes": "100%",
        "variants": "100%",
        "contenders": "100%",
        "gladiators": "100%"
    }


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
    """
    display_name = "Filler Weights"
    schema = Schema([{
        "name": lambda n: any(n == f.name for f in filler),
        "weight": And(int, lambda n: n >= 0),
        Optional("min"): And(int, lambda n: n >= 0),
        Optional("max"): And(int, lambda n: n >= 0),
        Optional("variant"): lambda s: s in ("pos", "neg", "both"),
        Optional("specificity"): And(int, lambda n: n in (0, 1, 2))
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


class FillerDuration(Range):
    """
    The number of games it will take before the effect of a filler or traps wears off.
    Only games where the filler or trap is relevant cause it to wear off.
    """
    display_name = "Filler Duration"
    range_start = 1
    range_end = 1024
    default = 5


class LocationDensity(OptionDict):
    """
    Specify the number of items placed at each location.
    If you want no items to be placed at a location, set it to 0 (Do not delete the entry outright!).
    Each location can have at most 64 items.
    """
    display_name = "Location Density"
    schema = Schema({
        "villain": {
            "normal": And(int, lambda n: 0 <= n <= 64),
            "advanced": And(int, lambda n: 0 <= n <= 64),
            "challenge": And(int, lambda n: 0 <= n <= 64),
            "ultimate": And(int, lambda n: 0 <= n <= 64)
        },
        "environment": And(int, lambda n: 0 <= n <= 64),
        "hero": And(int, lambda n: 0 <= n <= 64),
        "variant_unlock": And(int, lambda n: 0 <= n <= 64),
    })
    default = {
        "villain": {
            "normal": 1,
            "advanced": 1,
            "challenge": 1,
            "ultimate": 1
        },
        "environment": 1,
        "hero": 0,
        "variant_unlock": 1,
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
        "contenders": And(int, lambda n: n >= 0),
        "gladiators": And(int, lambda n: n >= 0),
    })
    default = {
        "heroes": 5,
        "villains": 2,
        "environments": 2,
        "contenders": 0,
        "gladiators": 0
    }


class VillainDifficulties(OptionDict):
    """
    Specify the minimum unique heroes logically required for beating villains on various difficulties.
    In the case of multiple definitions, the most specific one is used.
    """
    display_name = "Villain Difficulties"
    schema = Schema({
        str: Or(int, {
            Optional("Normal"): Or(int),
            Optional("Advanced"): Or(int),
            Optional("Challenge"): Or(int),
            Optional("Ultimate"): Or(int)
        })
    })
    default = {
        "Normal": 3, "Advanced": 3, "Challenge": 3, "Ultimate": 8, "Oblivaeon": 20,
        "The Chairman": {"Normal": 6, "Advanced": 6, "Challenge": 8, "Ultimate": 12},
        "The Matriarch": {"Normal": 5, "Advanced": 7, "Challenge": 7, "Ultimate": 10},
        "Iron Legacy": {"Normal": 8, "Advanced": 9, "Challenge": 9, "Ultimate": 10},
        "Progeny": {"Normal": 6, "Advanced": 7, "Challenge": 7, "Ultimate": 8}
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
    filler_weights: FillerWeights
    filler_duration: FillerDuration
    location_density: LocationDensity
    starting_items: StartingItems
    villain_difficulties: VillainDifficulties
    death_link: DeathLink


sotm_option_groups = [
    OptionGroup("Item Pool", [EnabledSets, PoolSize, IncludeInPool, IncludeVariantsInPool, ExcludeFromPool,
                              FillerWeights, FillerDuration]),
    OptionGroup("Goal", [RequiredVillains, VillainPoints, RequiredVariants, RequiredScions, ScionsAreRelative]),
    OptionGroup("Misc", [LocationDensity, StartingItems, VillainDifficulties, DeathLink]),
]

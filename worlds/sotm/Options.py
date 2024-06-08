from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle, Range, Choice, PerGameCommonOptions, ItemSet

try:
    from Options import OptionGroup
except ImportError:
    # In case this is used on 0.4.6
    class OptionGroup:
        name = "Placeholder"
        options = []

        def __init__(self, name, options):
            pass


class EnableRookCity(DefaultOnToggle):
    """Adds Rook City content to the pool"""
    display_name = "Enable Rook City"


class EnableInfernalRelics(DefaultOnToggle):
    """Adds Infernal Relics content to the pool"""
    display_name = "Enable Infernal Relics"


class EnableShatteredTimelines(DefaultOnToggle):
    """Adds Shattered Timelines content to the pool"""
    display_name = "Enable Shattered Timelines"


class EnableWrathOfTheCosmos(DefaultOnToggle):
    """Adds Wrath of the Cosmos content to the pool"""
    display_name = "Enable Wrath of the Cosmos"


class EnableVengeance(DefaultOnToggle):
    """Adds Vengeance content to the pool"""
    display_name = "Enable Vengeance"


class EnableVillainsOfTheMultiverse(DefaultOnToggle):
    """Adds Villains of the Multiverse content to the pool"""
    display_name = "Enable Villains of the Multiverse"


class EnableOblivaeon(DefaultOnToggle):
    """Adds Oblivaeon content to the pool"""
    display_name = "Enable Oblivaeon"


class EnableUnity(DefaultOnToggle):
    """Adds Unity to the pool
    This is part of Mini-Pack 1 in the digital version"""
    display_name = "Enable Unity"


class EnableTheScholar(DefaultOnToggle):
    """Adds The Scholar to the pool
    This is part of Mini-Pack 2 in the digital version"""
    display_name = "Enable The Scholar"


class EnableGuise(DefaultOnToggle):
    """Adds Guise to the pool
    This is part of Mini-Pack 3 in the digital version"""
    display_name = "Enable Guise"


class EnableStuntman(DefaultOnToggle):
    """Adds Stuntman to the pool
    This is part of Mini-Pack 4 in the digital version"""
    display_name = "Enable Stuntman"


class EnableBenchmark(DefaultOnToggle):
    """Adds Benchmark to the pool
    This is part of Mini-Pack 4 in the digital version"""
    display_name = "Enable Benchmark"


class EnableTheVoidGuard(DefaultOnToggle):
    """Adds The Void Guard to the pool
    This is part of Mini-Pack 5 in the digital version"""
    display_name = "Enable The Void Guard"


class EnableAmbuscade(DefaultOnToggle):
    """Adds Ambuscade to the pool
    This is part of Mini-Pack 1 in the digital version"""
    display_name = "Enable Ambuscade"


class EnableMissInformation(DefaultOnToggle):
    """Adds MissInformation to the pool
    This is part of Mini-Pack 2 in the digital version"""
    display_name = "Enable MissInformation"


class EnableWagerMaster(DefaultOnToggle):
    """Adds WagerMaster to the pool
    This is part of Mini-Pack 3 in the digital version"""
    display_name = "Enable WagerMaster"


class EnableChokepoint(DefaultOnToggle):
    """Adds Chokepoint to the pool
    This is part of Mini-Pack 4 in the digital version"""
    display_name = "Enable Chokepoint"


class EnableSilverGulch1883(DefaultOnToggle):
    """Adds Silver Gulch 1883 to the pool
    This is part of Mini-Pack 1 in the digital version"""
    display_name = "Enable Silver Gulch 1883"


class EnableTheFinalWasteland(DefaultOnToggle):
    """Adds The Final Wasteland to the pool
    This is part of Mini-Pack 2 in the digital version"""
    display_name = "Enable The Final Wasteland"


class EnableOmnitronIV(DefaultOnToggle):
    """Adds Omnitron IV to the pool
    This is part of Mini-Pack 3 in the digital version"""
    display_name = "Enable Omnitron IV"


class EnableTheCelestialTribunal(DefaultOnToggle):
    """Adds The Celestial Tribunal to the pool
    This is part of Mini-Pack 4 in the digital version"""
    display_name = "Enable The Celestial Tribunal"


class EnableTheCauldron(Toggle):
    """Adds content from the fan-made The Cauldron expansion to the pool"""
    display_name = "Enable The Cauldron"


class EnableCauldronPromos(Toggle):
    """Adds content from the fan-made Cauldron Promos expansion to the pool

    These are cauldron-themed variants for official heroes.
    Variants for The Cauldron content is included in the option above"""
    display_name = "Enable Cauldron Promos"


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


class VillainPointsNormal(Range):
    """The number of points beating a villain on Normal counts as for the required villains. This is cumulative"""
    display_name = "Villain Normal Points"
    range_start = 0
    range_end = 10
    default = 1


class VillainPointsAdvanced(Range):
    """The number of points beating a villain on Advanced counts as for the required villains. This is cumulative"""
    display_name = "Villain Advanced Points"
    range_start = 0
    range_end = 10
    default = 0


class VillainPointsChallenge(Range):
    """The number of points beating a villain on Challenge counts as for the required villains. This is cumulative"""
    display_name = "Villain Challenge Points"
    range_start = 0
    range_end = 10
    default = 0


class VillainPointsUltimate(Range):
    """The number of points beating a villain on Ultimate counts as for the required villains. This is cumulative"""
    display_name = "Villain Ultimate Points"
    range_start = 0
    range_end = 10
    default = 0


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


class ExtraScions(Range):
    """The number of additional scions in the pool"""
    display_name = "Extra Scions"
    range_start = 0
    range_end = 1000
    default = 0


class ScionsAreRelative(Toggle):
    """Changes it so the scion count options instead determine the portion of filler items that are replaced with scions
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


class VillainWeight(Range):
    """The weight that items added to the pool are villains"""
    display_name = "Villain Weight"
    range_start = 1
    range_end = 100
    default = 10


class EnvironmentWeight(Range):
    """The weight that items added to the pool are environments"""
    display_name = "Environment Weight"
    range_start = 1
    range_end = 100
    default = 20


class HeroWeight(Range):
    """The weight that items added to the pool are heroes"""
    display_name = "Hero Weight"
    range_start = 1
    range_end = 100
    default = 30


class VariantWeight(Range):
    """The weight that items added to the pool are variants"""
    display_name = "Hero Weight"
    range_start = 1
    range_end = 100
    default = 60


class LocationsPerVillainNormal(Range):
    """The quantity of locations done for each villain on normal difficulty"""
    display_name = "Locations Per Villain Normal"
    range_start = 0
    range_end = 5
    default = 1


class LocationsPerVillainAdvanced(Range):
    """The quantity of locations done for each villain on advanced difficulty"""
    display_name = "Locations Per Villain Advanced"
    range_start = 0
    range_end = 5
    default = 1


class LocationsPerVillainChallenge(Range):
    """The quantity of locations done for each villain on challenge difficulty"""
    display_name = "Locations Per Villain Challenge"
    range_start = 0
    range_end = 5
    default = 1


class LocationsPerVillainUltimate(Range):
    """The quantity of locations done for each villain on ultimate difficulty"""
    display_name = "Locations Per Villain Ultimate"
    range_start = 0
    range_end = 5
    default = 1


class LocationsPerEnvironment(Range):
    """The quantity of locations done for each environment on any difficulty"""
    display_name = "Locations Per Environment"
    range_start = 0
    range_end = 5
    default = 1


class LocationsPerVariant(Range):
    """The quantity of locations done for each variant unlock condition"""
    display_name = "Locations Per Variant"
    range_start = 0
    range_end = 5
    default = 1


class StartHeroes(Range):
    """The amount of heroes you start with"""
    display_name = "Start Heroes"
    range_start = 0
    range_end = 100
    default = 5


class StartVillains(Range):
    """The amount of villains you start with"""
    display_name = "Start Villains"
    range_start = 0
    range_end = 25
    default = 2


class StartEnvironment(Range):
    """The amount of environments you start with"""
    display_name = "Start Environments"
    range_start = 0
    range_end = 25
    default = 2


@dataclass
class SotmOptions(PerGameCommonOptions):
    enable_rook_city: EnableRookCity
    enable_infernal_relics: EnableInfernalRelics
    enable_shattered_timelines: EnableShatteredTimelines
    enable_wrath_of_the_cosmos: EnableWrathOfTheCosmos
    enable_vengeance: EnableVengeance
    enable_villains_of_the_multiverse: EnableVillainsOfTheMultiverse
    enable_oblivaeon: EnableOblivaeon
    enable_unity: EnableUnity
    enable_the_scholar: EnableTheScholar
    enable_guise: EnableGuise
    enable_stuntman: EnableStuntman
    enable_benchmark: EnableBenchmark
    enable_the_void_guard: EnableTheVoidGuard
    enable_ambuscade: EnableAmbuscade
    enable_miss_information: EnableMissInformation
    enable_wager_master: EnableWagerMaster
    enable_chokepoint: EnableChokepoint
    enable_silver_gulch_1883: EnableSilverGulch1883
    enable_the_final_wasteland: EnableTheFinalWasteland
    enable_omnitron_iv: EnableOmnitronIV
    enable_the_celestial_tribunal: EnableTheCelestialTribunal
    enable_the_cauldron: EnableTheCauldron
    enable_cauldron_promos: EnableCauldronPromos
    # Not yet implemented, current implementation is equivalent to if this is set to "enable"
    # separate_variant_items: SeparateVariantItems
    required_villains: RequiredVillains
    villain_points_normal: VillainPointsNormal
    villain_points_advanced: VillainPointsAdvanced
    villain_points_challenge: VillainPointsChallenge
    villain_points_ultimate: VillainPointsUltimate
    required_variants: RequiredVariants
    required_scions: RequiredScions
    extra_scions: ExtraScions
    scions_are_relative: ScionsAreRelative
    pool_size: PoolSize
    include_in_pool: IncludeInPool
    include_variants_in_pool: IncludeVariantsInPool
    exclude_from_pool: ExcludeFromPool
    villain_weight: VillainWeight
    environment_weight: EnvironmentWeight
    hero_weight: HeroWeight
    variant_weight: VariantWeight
    locations_per_villain_normal: LocationsPerVillainNormal
    locations_per_villain_advanced: LocationsPerVillainAdvanced
    locations_per_villain_challenge: LocationsPerVillainChallenge
    locations_per_villain_ultimate: LocationsPerVillainUltimate
    locations_per_environment: LocationsPerEnvironment
    locations_per_variant: LocationsPerVariant
    start_heroes: StartHeroes
    start_villains: StartVillains
    start_environments: StartEnvironment


sotm_option_groups = [
    OptionGroup("Official Content", [EnableRookCity,
                                     EnableInfernalRelics,
                                     EnableShatteredTimelines,
                                     EnableWrathOfTheCosmos,
                                     EnableVengeance,
                                     EnableVillainsOfTheMultiverse,
                                     EnableOblivaeon,
                                     EnableUnity,
                                     EnableTheScholar,
                                     EnableGuise,
                                     EnableStuntman,
                                     EnableBenchmark,
                                     EnableTheVoidGuard,
                                     EnableAmbuscade,
                                     EnableMissInformation,
                                     EnableWagerMaster,
                                     EnableChokepoint,
                                     EnableSilverGulch1883,
                                     EnableTheFinalWasteland,
                                     EnableOmnitronIV,
                                     EnableTheCelestialTribunal]),
    OptionGroup("Fan-made Content", [EnableTheCauldron, EnableCauldronPromos]),
    OptionGroup("Goal", [RequiredVillains, VillainPointsNormal, VillainPointsAdvanced, VillainPointsChallenge,
                         VillainPointsUltimate, RequiredVariants, RequiredScions, ExtraScions, ScionsAreRelative]),
    OptionGroup("Item Pool", [PoolSize, IncludeInPool, IncludeVariantsInPool, ExcludeFromPool,
                              VillainWeight, EnvironmentWeight, HeroWeight, VariantWeight]),
    OptionGroup("Location Density",
                [LocationsPerVillainNormal, LocationsPerVillainAdvanced, LocationsPerVillainChallenge,
                 LocationsPerVillainUltimate, LocationsPerEnvironment, LocationsPerVariant]),
    OptionGroup("Starting items", [StartHeroes, StartVillains, StartEnvironment])
]

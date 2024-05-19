import typing

from Options import Toggle, DefaultOnToggle, Option, Range, Choice


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


class SeparateVariantItems(Choice):
    """Separates hero variants into their own items instead of being unlocked with the hero
    Not Starting makes it so your starting heroes are never variants
    Villain variants are always separate"""
    display_name = "Separate Variant Items"
    option_enable = "enable"
    option_disable = "disable"
    option_not_starting = "not_starting"
    default = "enable"


class VillainDifficultyAffectsGoal(Toggle):
    """If enabled, villains beaten on higher difficulties will count for more if goal is set to villains
    This is cumulative
    Normal = 1
    Advanced = 1
    Challenge = 1
    Ultimate = 2"""
    display_name = "Villain Difficulty Affects Goal"


class RequiredVillains(Range):
    """The number of villains that must be defeated in order to goal"""
    display_name = "Required Villains"
    range_start = 0
    range_end = 74 * 5
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
    range_end = 100
    default = 10


class ExtraScions(Range):
    """The number of additional scions in the pool"""
    display_name = "Extra Scions"
    range_start = 0
    range_end = 100
    default = 0


class PoolSize(Range):
    """The minimum portion of the enabled content that is included in the rando
    Other options might cause this to be exceeded"""
    display_name = "Pool Size"
    range_start = 1
    range_end = 100
    default = 100


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
    display_name = "Locations Per Variant"
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
    range_start = 1
    range_end = 100
    default = 5


class StartVillains(Range):
    """The amount of villains you start with"""
    display_name = "Start Villains"
    range_start = 1
    range_end = 25
    default = 2


class StartEnvironment(Range):
    """The amount of environments you start with"""
    display_name = "Start Environments"
    range_start = 1
    range_end = 25
    default = 2


sotm_options: typing.Dict[str, Option] = {
    "enable_rook_city": EnableRookCity,
    "enable_infernal_relics": EnableInfernalRelics,
    "enable_shattered_timelines": EnableShatteredTimelines,
    "enable_wrath_of_the_cosmos": EnableWrathOfTheCosmos,
    "enable_vengeance": EnableVengeance,
    "enable_villains_of_the_multiverse": EnableVillainsOfTheMultiverse,
    "enable_oblivaeon": EnableOblivaeon,
    "enable_unity": EnableUnity,
    "enable_the_scholar": EnableTheScholar,
    "enable_guise": EnableGuise,
    "enable_stuntman": EnableStuntman,
    "enable_benchmark": EnableBenchmark,
    "enable_the_void_guard": EnableTheVoidGuard,
    "enable_ambuscade": EnableAmbuscade,
    "enable_miss_information": EnableMissInformation,
    "enable_wager_master": EnableWagerMaster,
    "enable_chokepoint": EnableChokepoint,
    "enable_silver_gulch_1883": EnableSilverGulch1883,
    "enable_the_final_wasteland": EnableTheFinalWasteland,
    "enable_omnitron_iv": EnableOmnitronIV,
    "enable_the_celestial_tribunal": EnableTheCelestialTribunal,
    "enable_the_cauldron": EnableTheCauldron,
    # Not yet implemented, current implementation is equivalent to if this is set to "enable"
    # "separate_variant_items": SeparateVariantItems,
    "villain_difficulty_affects_goal": VillainDifficultyAffectsGoal,
    "required_villains": RequiredVillains,
    "required_variants": RequiredVariants,
    "required_scions": RequiredScions,
    "extra_scions": ExtraScions,
    "pool_size": PoolSize,
    "locations_per_villain_normal": LocationsPerVillainNormal,
    "locations_per_villain_advanced": LocationsPerVillainAdvanced,
    "locations_per_villain_challenge": LocationsPerVillainChallenge,
    "locations_per_villain_ultimate": LocationsPerVillainUltimate,
    "locations_per_environment": LocationsPerEnvironment,
    "locations_per_variant": LocationsPerVariant,
    "start_heroes": StartHeroes,
    "start_villains": StartVillains,
    "start_environments": StartEnvironment,
}

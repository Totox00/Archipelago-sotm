from settings import Group


class SotmSettings(Group):
    class MaxLocationDensity(int):
        """The maximum accepted value of location_density.
        Minimum value is 1
        Maximum value is 64
        Default value is 5"""

    max_location_density: MaxLocationDensity | int = 5

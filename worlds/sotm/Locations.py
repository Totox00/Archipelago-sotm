from typing import Optional, Callable

from BaseClasses import Location, CollectionState

from .Data import data, SotmCategory, SotmState


class SotmLocation(Location):
    game: str = "Sentinels of the Multiverse"
    category: SotmCategory

    def __init__(
            self,
            player: int,
            name: str,
            address: Optional[int],
            category: SotmCategory,
            parent,
            req: Optional[str] = None,
            rule: Optional[Callable[[CollectionState | SotmState, int], bool]] = None,
            min_heroes: Optional[int] = None):
        super().__init__(player, name, address, parent)
        self.category = category

        if rule is not None:
            if min_heroes is None:
                self.access_rule = lambda state: rule(state, player)
            else:
                self.access_rule = lambda state: (rule(state, player)
                                                  and state.has("Unique Hero Thirds", player, min_heroes * 3))
        elif min_heroes is None:
            if category == SotmCategory.TeamVillain:
                self.access_rule = lambda state: state.has(req, player) and state.has("Team Villains", player, 3)
            elif category == SotmCategory.Gladiator:
                self.access_rule = lambda state: state.has(req, player) and state.has("Gladiators", player, 3)
            else:
                self.access_rule = lambda state: state.has(req, player)
        else:
            if category == SotmCategory.TeamVillain:
                self.access_rule = lambda state: (state.has(req, player)
                                                  and state.has("Team Villains", player, 3)
                                                  and state.has("Unique Hero Thirds", player, min_heroes * 3))
            elif category == SotmCategory.Gladiator:
                self.access_rule = lambda state: (state.has(req, player)
                                                  and state.has("Gladiators", player, 3)
                                                  and state.has("Unique Hero Thirds", player, min_heroes * 3))
            else:
                self.access_rule = lambda state: (state.has(req, player)
                                                  and state.has("Unique Hero Thirds", player, min_heroes * 3))

    @staticmethod
    def get_location_name_groups() -> dict:
        location_name_groups = {
            **{f"Environments #{n}": {f"{d.name} - Any Difficulty #{n}" for d in data
                                      if d.category == SotmCategory.Environment} for n in range(1, 6)},
            **{f"Variants #{n}": {f"{d.name} - Unlock #{n}" for d in data
                                  if d.category in (SotmCategory.Variant, SotmCategory.VillainVariant)}
               for n in range(1, 6)},
            **{f"Heroes #{n}": {f"{d.name} - Any Difficulty #{n}" for d in data
                                if d.category in (SotmCategory.Hero, SotmCategory.Variant)} for n in range(1, 6)}
        }

        for n in range(1, 6):
            for difficulty in ["Normal", "Advanced", "Challenge", "Ultimate"]:
                location_name_groups.update({f"Villains - {difficulty} #{n}": {
                    f"{d.name} - {difficulty} #{n}" for d in data
                    if d.category in (SotmCategory.Villain, SotmCategory.VillainVariant)}})
                location_name_groups.update({f"Team Villains - {difficulty} #{n}": {
                    f"{d.name} - {difficulty} #{n}" for d in data if d.category == SotmCategory.TeamVillain}})
                location_name_groups.update({f"Gladiators - {difficulty} #{n}": {
                    f"{d.name} - {difficulty} #{n}" for d in data if d.category == SotmCategory.Gladiator}})

        return location_name_groups

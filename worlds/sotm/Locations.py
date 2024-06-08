from typing import Optional, Callable

from BaseClasses import Location, CollectionState

from .Data import data, SotmCategory, difficulties, SotmState, team_villain_count, has_fanmade


class SotmLocation(Location):
    game: str = "Sentinels of the Multiverse"
    category: SotmCategory

    def __init__(
            self,
            player: int,
            name: str,
            address: int,
            category: SotmCategory,
            parent,
            req: Optional[str] = None,
            rule: Optional[Callable[[CollectionState | SotmState, int], bool]] = None):
        super().__init__(player, name, address, parent)
        self.category = category
        if rule is not None:
            self.access_rule = lambda state: rule(state, player)
        elif category == SotmCategory.TeamVillain:
            self.access_rule = lambda state: state.has(req, player) and team_villain_count(state, player)
        else:
            self.access_rule = lambda state: state.has(req, player)

    @staticmethod
    def get_name_to_id() -> dict:
        next_id = 27181774
        output = {}

        duo = 0

        for location_data in data:
            match location_data.category:
                case SotmCategory.VillainVariant:
                    if location_data.name == "Spite: Agent of Gloom" or location_data.name == "Skinwalker Gloomweaver":
                        for difficulty in ["Normal", "Advanced"]:
                            for n in range(1, 6):
                                output.update({f"{location_data.name} - {difficulty} #{n}": next_id})
                                next_id += 1

                        duo += 1
                        if duo == 2:
                            duo_name = "Spite: Agent of Gloom and Skinwalker Gloomweaver"
                            for difficulty in ["Challenge", "Ultimate"]:
                                for n in range(1, 6):
                                    output.update({f"{duo_name} - {difficulty} #{n}": next_id})
                                    next_id += 1
                    else:
                        for difficulty in difficulties:
                            for n in range(1, 6):
                                output.update({f"{location_data.name} - {difficulty} #{n}": next_id})
                                next_id += 1
                    for n in range(1, 6):
                        output.update({f"{location_data.name} - Unlock #{n}": next_id})
                        next_id += 1
                case SotmCategory.Villain | SotmCategory.TeamVillain:
                    for difficulty in difficulties:
                        for n in range(1, 6):
                            output.update({f"{location_data.name} - {difficulty} #{n}": next_id})
                            next_id += 1
                case SotmCategory.Environment:
                    for n in range(1, 6):
                        output.update({f"{location_data.name} - Any Difficulty #{n}": next_id})
                        next_id += 1
                case SotmCategory.Variant:
                    if location_data.name != "Completionist Guise" and not has_fanmade(location_data.sources):
                        for n in range(1, 6):
                            output.update({f"{location_data.name} - Unlock #{n}": next_id})
                            next_id += 1
        return output

    @staticmethod
    def get_location_name_groups() -> dict:
        location_name_groups = {
            **{f"Environments #{n}": {f"{d.name} - Any Difficulty #{n}" for d in data
                                      if d.category == SotmCategory.Environment} for n in range(1, 6)},
            **{f"Variants #{n}": {f"{d.name} - Unlock #{n}" for d in data
                                  if d.category == SotmCategory.Variant or d.category == SotmCategory.VillainVariant}
               for n in range(1, 6)},
        }
        villain_names = [d.name for d in data if
                         d.category == SotmCategory.Villain or d.category == SotmCategory.VillainVariant]
        team_villain_names = [d.name for d in data if d.category == SotmCategory.TeamVillain]

        for n in range(1, 6):
            for difficulty in ["Normal", "Advanced"]:
                location_name_groups.update({f"Villains - {difficulty} #{n}": {
                    f"{name} - {difficulty} #{n}" for name in villain_names}})
            for difficulty in ["Challenge", "Ultimate"]:
                next_group = {
                     f"{name} - {difficulty} #{n}" for name
                     in villain_names if
                     name != "Spite: Agent of Gloom" and name != "Skinwalker Gloomweaver"}
                next_group.add(f"Spite: Agent of Gloom and Skinwalker Gloomweaver - {difficulty} #{n}")
                location_name_groups.update({f"Villains - {difficulty} #{n}": next_group})
            for difficulty in difficulties:
                location_name_groups.update({f"Team Villains - {difficulty} #{n}": {
                    f"{name} - {difficulty} #{n}" for name in team_villain_names}})

        return location_name_groups

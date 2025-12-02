from typing import Optional

from BaseClasses import Item, ItemClassification

from .Data import data, SotmCategory, base_to_variants


class SotmItem(Item):
    game: str = "Sentinels of the Multiverse"

    def __init__(
            self,
            player: int,
            name: str,
            code: Optional[int],
            category: SotmCategory,
            classification: Optional[ItemClassification] = None,
            base: Optional[str] = None,
            villain_points: int = 0):
        if classification is None:
            classification = ItemClassification.progression_deprioritized_skip_balancing
            if category in (SotmCategory.Villain, SotmCategory.VillainVariant):
                classification = ItemClassification.progression
            if category in (SotmCategory.TeamVillain, SotmCategory.Gladiator):
                classification = ItemClassification.progression_skip_balancing
            if category == SotmCategory.Filler:
                classification = ItemClassification.filler
            elif category == SotmCategory.Trap:
                classification = ItemClassification.trap
        super().__init__(name, classification, code, player)
        self.category = category
        self.base = base
        self.villain_points = 0 if category == SotmCategory.TeamVillain else villain_points
        self.team_villain_points = villain_points if category == SotmCategory.TeamVillain else 0

    @staticmethod
    def get_item_name_groups(item_name_to_id: dict[str, int]) -> dict:
        ret = {
            "Heroes": {d.name for d in data if d.category == SotmCategory.Hero},
            "Contenders": {d.name for d in data if d.category == SotmCategory.Contender},
            "Environments": {d.name for d in data if d.category == SotmCategory.Environment},
            "Villains": {d.name for d in data if d.category == SotmCategory.Villain
                         or d.category == SotmCategory.VillainVariant},
            "Team Villains": {d.name for d in data if d.category == SotmCategory.TeamVillain},
            "Gladiators": {d.name for d in data if d.category == SotmCategory.Gladiator},
            "Variants": {d.name for d in data if d.category == SotmCategory.Variant},
            "Filler": {name for name, id in item_name_to_id.items() if id >> 48 & 0b1111 == 0b1000},
            "Traps": {name for name, id in item_name_to_id.items() if id >> 48 & 0b1111 == 0b1001}
        }

        for base, variants in base_to_variants.items():
            ret[f"Any {base}"] = {base, *variants}

        return ret

from typing import Optional

from BaseClasses import Item, ItemClassification

from .Data import data, SotmCategory


class SotmItem(Item):
    game: str = "Sentinels of the Multiverse"

    def __init__(
            self,
            player: int,
            name: str,
            code: Optional[int],
            category: SotmCategory,
            classification: Optional[ItemClassification] = None):
        if classification is None:
            classification = ItemClassification.progression_skip_balancing
            if category == SotmCategory.Filler:
                classification = ItemClassification.filler
            elif category == SotmCategory.Trap:
                classification = ItemClassification.trap
        super().__init__(name, classification, code, player)
        self.category = category

    @staticmethod
    def get_item_name_groups() -> dict:
        return {
            "Heroes": {d.name for d in data if d.category == SotmCategory.Hero},
            "Environments": {d.name for d in data if d.category == SotmCategory.Environment},
            "Villains": {d.name for d in data if d.category == SotmCategory.Villain
                         or d.category == SotmCategory.VillainVariant},
            "Team Villains": {d.name for d in data if d.category == SotmCategory.TeamVillain},
            "Variants": {d.name for d in data if d.category == SotmCategory.Variant},
        }

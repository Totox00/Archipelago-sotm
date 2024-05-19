from typing import Optional

from BaseClasses import Item, ItemClassification

from .Data import data, SotmData, SotmSource, SotmCategory


class SotmItem(Item):
    game: str = "Sentinels of the Multiverse"

    def __init__(
            self,
            player: int,
            name: str,
            code: int,
            category: SotmCategory,
            classification: Optional[ItemClassification] = None):
        if classification is None:
            classification = ItemClassification.progression_skip_balancing
            if category == SotmCategory.Filler:
                classification = ItemClassification.filler
        super().__init__(name, classification, code, player)
        self.category = category

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 27181774
        return {item_data.name: item_id for item_id, item_data in enumerate(data + [
            SotmData("Scion of Oblivaeon", SotmSource.Oblivaeon, SotmCategory.Scion),
            SotmData("1 Undo", SotmSource.Base, SotmCategory.Filler)
        ], base_id)}

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

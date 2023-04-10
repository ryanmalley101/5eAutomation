from PyQt6.QtWidgets import QLabel, QPushButton
from srd.srd_datastructs import AbilityDescription, BaseAttack, CreatureStatblock
from PyQt6.QtCore import Qt


class AbilityButton(QPushButton):
    def __init__(self, ability: AbilityDescription, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ability = ability
        label = QLabel(f"<b>{ability.name}</b>: {ability.description}", self).setTextFormat(Qt.TextFormat.RichText)
        self.setFlat(True)
        self.setObjectName(ability.name)


class AttackButton(QPushButton):
    def __init__(self, attack: BaseAttack, creature: CreatureStatblock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = attack
        print(attack.rich_text(creature))
        label = QLabel(attack.rich_text(creature), self).setTextFormat(Qt.TextFormat.RichText)
        self.setFlat(True)
        self.setObjectName(attack.name)

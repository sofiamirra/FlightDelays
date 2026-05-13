"""Creiamo apposito oggetto, anzichè una tupla, per poter accedere più facilmente agli attributi"""
from dataclasses import dataclass
from model.airport import Airport

@dataclass
class Tratta:
    aeroportoP: Airport
    aeroportoA: Airport
    peso: int

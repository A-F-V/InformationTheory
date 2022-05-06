from itertools import product
from typing import Callable
from code_types import Symbol, SymbolCode, BinaryEnsemble, CompressionCode, CodeWord


class Ensemble:
    def __init__(self, alphabet: list[CodeWord], p: Callable([CodeWord], float), name: str):
        self.alphabet = alphabet
        self.p = p
        self.name = name

    @staticmethod
    def from_mass(alphabet: list[CodeWord], pmass: list[float], name: str):
        return Ensemble(alphabet, lambda c: pmass[alphabet.index(c)], name)

    @staticmethod
    def ask_for_ensemble():
        output = {}
        while input("Do you want to add another symbol? (y/n) ") == "y":
            symbol = input("Symbol: ")
            prop = float(input("Weight: "))
            output[symbol] = prop
        alphabet = list(output.keys())
        pmass = list(output.values())
        return Ensemble.from_mass(alphabet, pmass, "Ensemble")


class NEnsemble:
    """The joint ensemble formed by applying ensemble E n times.
    """

    def __init__(self, ensemble: Ensemble, times: int, name="Joint Ensemble"):
        self.alphabet = list(map(lambda y: "".join(y), product(ensemble.alphabet, repeat=times)))
        self.source_ensemble = ensemble
        super().__init__(self.alphabet, self._p, name)

    def _p(self, c: CodeWord):
        letter_counts = [len(list(filter(lambda y: y == x, c))) for x in self.source_ensemble.alphabet]
        return sum([self.source_ensemble.p(self.source_ensemble.alphabet[i])**letter_counts[i] for i in range(len(self.source_ensemble.alphabet))])


class BinaryNEnsemble(NEnsemble):
    """A Binary Symbol Code class where each bit has constant and independent probability of appearing
    """

    def __init__(self, p0, p1, times, name="Binary Ensemble"):
        super().__init__(['0', '1'], [p0, p1], times, name)

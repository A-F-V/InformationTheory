from itertools import product
from math import log2


class SymbolCode:
    """A Class for Symbol Codes
    """

    def __init__(self, alphabet, probabilities, name="Symbol Code"):
        self.alphabet = alphabet
        self.probabilities = probabilities
        assert len(alphabet) == len(probabilities)
        paired = sorted(zip(self.alphabet, self.probabilities))
        self.name = name
        self.p = dict(paired)

    def Entropy(self):
        return sum(map(lambda x: -self.p[x]*log2(self.p[x]), self.alphabet))

    def ExpectedLength(self):
        return sum(map(lambda x: self.p[x]*len(x), self.alphabet))

    def __str__(self):
        paired = sorted(self.p.items())
        output = f"{self.name}:\n" + "\n".join(["{}: {:.5f}".format(x[0], x[1]) for x in paired])
        output += f"\nEntropy: {self.Entropy():.4f}\nExpected Length: {self.ExpectedLength():.4f}\n"
        return output


class BinaryEnsemble(SymbolCode):
    """A Binary Symbol Code class where each bit has constant and independent probability of appearing
    """

    def __init__(self, p0, p1, times, name="Binary Ensemble"):
        alphabet = list(map(lambda y: "".join(y), product(['0', '1'], repeat=times)))
        self.p0 = p0
        self.p1 = p1
        probabilities = [self._p(x) for x in alphabet]
        super().__init__(alphabet, probabilities, name)

    def _p(self, x):
        zero_count = len(list(filter(lambda y: y == '0', x)))
        one_count = len(x) - zero_count
        return (self.p0**zero_count)*(self.p1**one_count)

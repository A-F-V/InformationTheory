
from math import log2
from abc import abstractmethod
from typing import Callable, Dict, NewType, Literal



# We only conside symbols as only lower case letter, digits and $
Symbol = Literal['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '$']

CodeWord = NewType('SymbolWord', str)


# class StreamCode:
#    def __init__(self, alphabet: list[Symbol], probabilities: Callable[[CodeWord], float], name="Stream Code"):
#        self.alphabet = alphabet
#        self.p = probabilities  # From Symbol+ to Symbol+
#        self.name = name

class ErrorCorrectingCode:
    """A class for error correcting codes. 
    """

    def __init__():
        pass
    
class SymbolCode:
    """A Class for Symbol Codes. Symbols/Codewords are stored with their relative probabilities
    """

    def __init__(self, alphabet: list[CodeWord], probabilities: Callable[[CodeWord], float], name="Symbol Code"):

        self.alphabet = sorted(alphabet)
        #self.probabilities = probabilities
        self.p = probabilities
        self.name = name

    def Entropy(self):
        return sum(map(lambda x: -self.p(x)*log2(self.p(x)), self.alphabet))

    def ExpectedLength(self):
        return sum(map(lambda x: self.p(x)*len(x), self.alphabet))

    def __str__(self):
        output = f"{self.name}:\n" + "\n".join(["{}: {:.5f}".format(symbolWord, self.p(symbolWord))
                                               for symbolWord in self.alphabet])
        output += f"\nEntropy: {self.Entropy():.4f}\nExpected Length: {self.ExpectedLength():.4f}\n"
        return output


class CompressionCode(SymbolCode):
    def __init__(self, code: SymbolCode, alphabet: list[CodeWord], probabilities: Callable[[CodeWord], float], name="Compression Code"):
        self.source_code = code
        super().__init__(alphabet, probabilities, name)

    def EncodeMessage(self, message: list[CodeWord]):
        return [self.EncodeSymbol(x) for x in message]

    def DecodeMessage(self, message: list[CodeWord]):
        return [self.DecodeSymbol(x) for x in message]

    @abstractmethod
    def EncodeSymbol(self, symbol: CodeWord):
        pass

    @abstractmethod
    def DecodeMessage(self, symbol: CodeWord):
        pass


from code_types import SymbolCode, CompressionCode, CodeWord
from heapq import heappush, heappop, heapify


class HuffmanCode(CompressionCode):
    """A Huffman Code class. Maps a symbol code to a huffman code
    """

    def __init__(self, code: SymbolCode, name="Huffman Code"):
        self.source_code = code
        root = self._build_tree()  # GENERATE TREE
        translations = self._build_code_translations(root)  # LABEL TREE WITh 0s and 1s
        self.translation = {x[0]: x[1] for x in translations}  # TRANSLATE TO HUFFMAN CODE
        self.inverse_translation = {x[1]: x[0] for x in translations}  # TRANSLATE FROM HUFFMAN CODE
        self.alphabet = sorted(self.translation.values())
        # Probability of a huffman code word is the probability of the original word
        def _p(x): return self.source_code.p(self.inverse_translation[x])
        super().__init__(self.source_code, self.alphabet, _p, name)

    def _build_tree(self):
        """Build a Huffman Tree
        """
        # leaves
        nodes = [(self.source_code.p(self.source_code.alphabet[i]), self.source_code.alphabet[i])
                 for i in range(len(self.source_code.alphabet))]
        heapify(nodes)
        while(len(nodes) > 1):
            p1 = heappop(nodes)
            p2 = heappop(nodes)
            new_node = (p1[0]+p2[0], p1, p2)
            heappush(nodes, new_node)
        root = heappop(nodes)
        return root

    def _build_code_translations(self, root):
        """Build a translation table for the Huffman Code
        """
        translations = []

        def _translate(node, baggage=""):
            if len(node) == 2:  # is leaf
                translations.append((node[1], baggage))
            else:
                _translate(node[1], baggage+"0")
                _translate(node[2], baggage+"1")
        _translate(root)
        return translations

    def __str__(self):
        output = f"{self.name}:\n" + "\n".join(["{} -> {}: {:.4f}".format(x,
                                               self.translation[x], self.source_code.p(x)) for x in self.source_code.alphabet])
        output += f"\nEntropy: {self.Entropy():.4f}\nExpected Length: {self.ExpectedLength():.4f}\nCost: {self.Cost():.4f}\n"
        return output

    def Cost(self):
        return sum(map(lambda x: 2**(-len(x)), self.alphabet))

    def EncodeSymbol(self, symbol: CodeWord):
        return self.translation[symbol]

    def DecodeSymbol(self, symbol: CodeWord):
        return self.inverse_translation[symbol]

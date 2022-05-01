from huffman_code import HuffmanCode
from symbol_code import BinaryEnsemble

x2 = BinaryEnsemble(0.9, 0.1, 2, "X2")
x3 = BinaryEnsemble(0.9, 0.1, 3, "X3")
x4 = BinaryEnsemble(0.9, 0.1, 4, "X4")
x2p = BinaryEnsemble(0.6, 0.4, 2, "X2")
x4p = BinaryEnsemble(0.6, 0.4, 4, "X4")

h2 = HuffmanCode(x2, "H2")
h3 = HuffmanCode(x3, "H3")
h4 = HuffmanCode(x4, "H4")
h2p = HuffmanCode(x2p, "H2p")
h4p = HuffmanCode(x4p, "H4p")

print(h2)
print(h3)
print(h4)
print(h2p)
print(h4p)

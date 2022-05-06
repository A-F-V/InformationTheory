from decimal import Decimal
from code_types import StreamCode, Symbol, SymbolCode, BinaryEnsemble, CompressionCode, CodeWord
from symbol_ensemble import Ensemble


class ArithmeticCode():
    def __init__(self, ensemble: Ensemble, end_of_sequence_symbol="$",  name="Arithmetic Code"):
        self.eos = end_of_sequence_symbol
        self.ensemble = ensemble

    def _Cum(self, s: Symbol):
        """Returns the bottom and top probabilities of the symbol s if cummulated with the previous symbol.

        Args:
            s (Symbol): The symbol to find probs for

        Returns:
            tuple: lower and upper probs
        """
        bot = 0
        for sym in self.ensemble.alphabet:
            mas = self.ensemble.p(sym)
            if sym == s:
                return bot, bot+mas
            bot += mas

    def _optimal_string_in_range(self, u, v):
        return u

    def Encode(self, msg: str):
        if self.eos not in msg:
            msg += "$"
        prob = list(prob.items())
        u, v = Decimal(0), Decimal(1)
        for symbol in msg:
            Q, R = self._Cum(symbol)
            cur_width = v - u
            u, v = u + cur_width*Decimal(Q), u+cur_width*Decimal(R)
        # U and V are the ranges. Choose optimal string within range to output
        return self._optimal_string_in_range(u, v)

    def _msg_to_prob(msg: str):
        msg_orig = msg
        nbits = len(msg_orig)
        p = Decimal(int(msg, 2))
        p = p / Decimal(2**nbits)
        return p

    def Decode(self, msg: str):
        msg = self._msg_to_prob(msg)
        u, v = Decimal(0), Decimal(1)
        output = ""
        while len(output) == 0 or output[-1] != self.eos:
            width = v-u
            ua, va = u, u
            for sym in self.ensemble.alphabet:
                mas = self.ensemble.p(sym)
                ua, va = va, va+Decimal(mas)*width
                if ua <= msg < va:
                    output += sym
                    u, v = ua, va
                    break
        return output

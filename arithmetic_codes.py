from decimal import Decimal


def generate_probability_distribution(prop: dict):
    orig = dict(prop)
    tot = sum(orig.values())
    return {k: v/tot for k, v in orig.items()}


def ask_for_dist():
    output = {}
    while input("Do you want to add another symbol? (y/n) ") == "y":
        symbol = input("Symbol: ")
        prop = float(input("Weight: "))
        output[symbol] = prop
    eos = float(input("End of sequence Weight: "))
    output["$"] = eos
    return output


def Cum(x, p):
    s = 0
    for sym, mas in p:
        if sym == x:
            return s, s+mas
        s += mas


def encode(msg, prob: dict):
    if "$" not in msg:
        msg += "$"
    prob = list(prob.items())
    u, v = Decimal(0), Decimal(1)
    for c in msg:
        Q, R = Cum(c, prob)
        u, v = u + (v-u)*Decimal(Q), u+(v-u)*Decimal(R)
    return u


def decode(msg, prob: dict):
    u, v = Decimal(0), Decimal(1)
    output = ""
    prob = list(prob.items())
    while len(output) == 0 or output[-1] != "$":
        width = v-u
        ua, va = u, u
        for sym, mas in prob:
            ua, va = va, va+Decimal(mas)*width
            if ua <= msg < va:
                output += sym
                u, v = ua, va
                break
    return output


p = generate_probability_distribution(ask_for_dist())
ac = encode(input("Message: "), p)
print(decode(ac, p))
# extensions:
# - Choose shortest bit string



from pyrsistent import b


def lempel_ziv_enc(data, bit_num, alphabet=None):
    i = 0
    max_num = 2**bit_num
    lookup = {alphabet[i]: i for i in range(len(alphabet))}
    output = []
    def full(): return len(lookup) == max_num
    while i < len(data):
        # find S and X
        s = data[i]
        j = 1
        while i+j < len(data) and s+data[i+j] in lookup:
            s += data[i+j]
            j += 1
        x = data[i+j] if i+j < len(data) else ""

        # add to dict if not full
        if full():
            output.append(lookup[s])
            i += j
        else:
            lookup[s+x] = len(lookup)
            output.append(lookup[s])
            i += j
    return "".join(map(lambda x: "{0:0{1}b}".format(x, bit_num), output))


def lempel_ziv_dec(data, bit_num, alphabet=None):
    max_num = 2**bit_num
    lookup = {i: alphabet[i] for i in range(len(alphabet))}
    data = [int(data[i: i+bit_num], 2) for i in range(0, len(data), bit_num)]
    output = ""
    def full(): return len(lookup) == max_num

    # PROPERTY: LZ will create a new code at each iteration for the first 2^bit_num - len(alphabet) iterations
    # 4 cases (NotFULL + NO X, NotFull + X , Full + X, Full + NO X)
    last_insert = None
    for it in range(len(data)):

       # if it == 0:
       #     s = lookup[data[it]]
       #     output += s
       #     lookup[len(lookup)] = s

       # elif it > 0 and not full():
       #     X_prev = lookup[data[it]][0]
       #     lookup[data[it-1]] = lookup[data[it-1]]+X_prev
       #     s = lookup[data[it]]
       #     output += s
       #     lookup[len(lookup)] = s

       # elif it == max_num-len(alphabet)+1:
       #     X_prev = lookup[data[it]][0]
       #     lookup[data[it-1]] = lookup[data[it-1]]+X_prev
       #     s = lookup[data[it]]
       #     output += s

       # else:
       #     s = lookup[data[it]]
       #     output += s

        if it > 0 and it <= max_num-len(alphabet):  # retrospective correction for X
            X_prev = lookup[data[it]][0]
            lookup[last_insert] = lookup[last_insert]+X_prev
        s = lookup[data[it]]
        output += s
        if not full():
            last_insert = len(lookup)
            lookup[len(lookup)] = s

    return output


alpha = ["a", "b", "#"]
mes = "aaaaabaaaabaa#"
enc = lempel_ziv_enc(mes, 3, alpha)
dec = lempel_ziv_dec(enc, 3, alpha)
print(mes)
print(enc)
print(dec)

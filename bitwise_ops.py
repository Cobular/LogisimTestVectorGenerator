def bitwise_not(inp: list[bool]) -> list[bool]:
    return [not i for i in inp]


def bitwise_xor(a: list[bool], b: list[bool]) -> list[bool]:
    return [a[i] ^ b[i] for i in range(len(a))]


def bitwise_or(a: list[bool], b: list[bool]) -> list[bool]:
    return [a[i] | b[i] for i in range(len(a))]


def bitwise_and(a: list[bool], b: list[bool]) -> list[bool]:
    return [a[i] & b[i] for i in range(len(a))]


def bitwise_add(a: list[bool], b: list[bool], cin: bool) -> list[bool]:
    carry = cin
    res = []

    for i in reversed(range(len(a))):
        res.insert(0, a[i] ^ b[i] ^ carry)
        carry = (a[i] & b[i]) | (a[i] & carry) | (b[i] & carry)

    return res
from typing import List

from TestVector import TestVector
from custom_types import InputOutputShapeElement, InputOutputCase
from utils import create_one_hot_inputs, flattenInputOutputCase, \
    create_all_inputs, flattenInputOutputCaseToString, \
    flattenInputOutputElementToString, int_to_byte_arr


def TaskOneGenerator(input_case: InputOutputCase) -> List[bool]:
    flatInputBytes: list[bool] = flattenInputOutputCase(input_case)

    counter = 0
    for index, val in enumerate(flatInputBytes):
        if val is True:
            counter = 7 - index
            break

    return [bool(int(j)) for j in "{0:03b}".format(counter)]


task1 = TestVector(
    [InputOutputShapeElement(label="A", width=8)],
    [InputOutputShapeElement(label="X", width=3)],
    TaskOneGenerator,
    create_one_hot_inputs,
    "test_vectors/da1p1.txt"
)


def TaskTwoGenerator(input_case: InputOutputCase) -> List[bool]:
    flatInputBytes: str = flattenInputOutputCaseToString(input_case)

    inputValue = int(flatInputBytes, 2)

    raw_input_bits = [False] * (2 ** len(flatInputBytes))
    raw_input_bits[127 - inputValue] = True

    return raw_input_bits


task2 = TestVector(
    [InputOutputShapeElement(label="A", width=7)],
    [
        InputOutputShapeElement(label="X1", width=64),
        InputOutputShapeElement(label="X0", width=64),
    ],
    TaskTwoGenerator,
    create_all_inputs,
    "test_vectors/da1p2.txt"
)


def TaskThreeGenerator(input_case: InputOutputCase) -> List[bool]:
    aBytes: str = flattenInputOutputElementToString(input_case[0])
    bBytes: str = flattenInputOutputElementToString(input_case[1])

    counter = 0
    for aByte, bByte in zip(aBytes, bBytes):
        if aByte != bByte:
            counter += 1

    return int_to_byte_arr(counter, 3)


task3 = TestVector(
    [
        InputOutputShapeElement(label="A", width=4),
        InputOutputShapeElement(label="B", width=4)
    ],
    [
        InputOutputShapeElement(label="X", width=3),
    ],
    TaskThreeGenerator,
    create_all_inputs,
    "test_vectors/da1p3.txt"
)

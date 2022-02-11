import unittest
from typing import List

from custom_types import InputOutputShapeElement, InputOutputCase, \
    InputOutputCaseElement
from src.TestVector import TestVector
from utils import create_all_inputs, flattenInputOutputCaseToString


def TaskTwoGenerator(input_case: InputOutputCase) -> List[bool]:
    flatInputBytes: str = flattenInputOutputCaseToString(input_case)

    inputValue = int(flatInputBytes, 2)

    raw_input_bits = [False] * (2 ** len(flatInputBytes))
    raw_input_bits[127 - inputValue] = True

    return raw_input_bits


def RunTaskTwo(file: str = "test_vectors/da1p2.txt"):
    TestVector(
        [InputOutputShapeElement(label="A", width=7)],
        [
            InputOutputShapeElement(label="X1", width=64),
            InputOutputShapeElement(label="X0", width=64),
        ],
        TaskTwoGenerator,
        create_all_inputs,
        file
    )


class TaskTwoTests(unittest.TestCase):
    def test_zero(self):
        input_case = (InputOutputCaseElement(
            label="A", width=7, state=(False,) * 7
        ),)

        res = [False] * 128
        res[127] = True

        self.assertListEqual(
            TaskTwoGenerator(input_case), res
        )

    def test_one(self):
        input_case = (InputOutputCaseElement(
            label="A", width=7, state=(
                False, False, False, False, False, False, True
            )
        ),)

        res = [False] * 128
        res[127 - 1] = True

        self.assertListEqual(
            TaskTwoGenerator(input_case), res
        )

    def test_fifteen(self):
        input_case = (InputOutputCaseElement(
            label="A", width=7, state=(
                False, False, False, True, True, True, True
            )
        ),)

        res = [False] * 128
        res[127 - 15] = True

        self.assertListEqual(
            TaskTwoGenerator(input_case), res
        )

    def test_max(self):
        input_case = (InputOutputCaseElement(
            label="A", width=7, state=(True,) * 7
        ),)

        res = [False] * 128
        res[127 - 127] = True

        self.assertListEqual(
            TaskTwoGenerator(input_case), res
        )

import unittest
from typing import List

from custom_types import InputOutputCase, InputOutputShapeElement, \
    InputOutputCaseElement
from src.TestVector import TestVector
from utils import flattenInputOutputCase, create_one_hot_inputs


def TaskOneGenerator(input_case: InputOutputCase) -> List[bool]:
    flatInputBytes: list[bool] = flattenInputOutputCase(input_case)

    counter = 0
    for index, val in enumerate(flatInputBytes):
        if val is True:
            counter = 7 - index
            break

    return [bool(int(j)) for j in "{0:03b}".format(counter)]


def RunTaskOne(file: str = "test_vectors/da1p1.txt"):
    TestVector(
        [InputOutputShapeElement(label="A", width=8)],
        [InputOutputShapeElement(label="X", width=3)],
        TaskOneGenerator,
        create_one_hot_inputs,
        file
    )


class TaskOneTests(unittest.TestCase):
    def test_zero(self):
        input_case = (InputOutputCaseElement(
            label="A", width=8, state=(False,) * 8
        ),)

        self.assertListEqual(
            TaskOneGenerator(input_case), [False, False, False]
            )

    def test_one(self):
        input_case = (InputOutputCaseElement(
            label="A", width=8, state=(True,) * 8
        ),)

        self.assertListEqual(
            TaskOneGenerator(input_case), [True, True, True]
            )

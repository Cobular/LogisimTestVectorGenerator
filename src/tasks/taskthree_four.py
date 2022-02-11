import unittest
from typing import List

from custom_types import InputOutputCase, InputOutputShapeElement, \
    InputOutputCaseElement
from src.TestVector import TestVector
from utils import flattenInputOutputElementToString, int_to_byte_arr, \
    create_all_inputs


def TaskThreeGenerator(input_case: InputOutputCase) -> List[bool]:
    aBytes: str = flattenInputOutputElementToString(input_case[0])
    bBytes: str = flattenInputOutputElementToString(input_case[1])

    counter = 0
    for aByte, bByte in zip(aBytes, bBytes):
        if aByte != bByte:
            counter += 1

    return int_to_byte_arr(counter, 3)


def RunTaskThree(file: str = "test_vectors/da1p3.txt"):
    TestVector(
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


def RunTaskFour(file: str = "test_vectors/da1p4.txt"):
    RunTaskThree(file)


class TaskThreeTests(unittest.TestCase):
    def test_zero(self):
        input_case = (
            InputOutputCaseElement(
                label="A", width=4, state=(False, False, False, False)
            ),
            InputOutputCaseElement(
                label="B", width=4, state=(False, False, False, False)
            ),)

        res = [False, False, False]

        self.assertListEqual(
            TaskThreeGenerator(input_case), res
        )

    def test_one(self):
        input_case = (
            InputOutputCaseElement(
                label="A", width=4, state=(False, False, False, True)
            ),
            InputOutputCaseElement(
                label="B", width=4, state=(False, False, False, False)
            ),)

        res = [False, False, True]

        self.assertListEqual(
            TaskThreeGenerator(input_case), res
        )

    def test_max(self):
        input_case = (
            InputOutputCaseElement(
                label="A", width=4, state=(False, False, True, True)
            ),
            InputOutputCaseElement(
                label="B", width=4, state=(True, True, False, False)
            ),)

        res = [True, False, False]

        self.assertListEqual(
            TaskThreeGenerator(input_case), res
        )

    def test_med(self):
        input_case = (
            InputOutputCaseElement(
                label="A", width=4, state=(False, False, False, True)
            ),
            InputOutputCaseElement(
                label="B", width=4, state=(True, True, False, False)
            ),)

        res = [False, True, True]

        self.assertListEqual(
            TaskThreeGenerator(input_case), res
        )

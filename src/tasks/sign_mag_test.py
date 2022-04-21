import unittest

from custom_types import InputOutputCaseElement
from src.tasks.sign_mag import SignMagGenerator
from utils import int_array_to_bool_array


class TaskOneTests(unittest.TestCase):
    def test_zero(self):
        input_case = (
            InputOutputCaseElement(label="A", width=8, state=(False,) * 13),)
        self.assertListEqual(SignMagGenerator(input_case), [False] * 13)

    def test_one(self):
        input_case = (
            InputOutputCaseElement(label="A", width=8, state=(True,) * 13),)
        self.assertListEqual(
            SignMagGenerator(input_case), int_array_to_bool_array(
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            )
        )

    def test_neg_20(self):
        input_case = (
            InputOutputCaseElement(
                label="TWOS_COMP",
                width=13,
                state=tuple(
                    int_array_to_bool_array(
                        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0]
                    )
                ),
            ),
        )

        self.assertListEqual(
            SignMagGenerator(input_case),
            int_array_to_bool_array([1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]),
        )

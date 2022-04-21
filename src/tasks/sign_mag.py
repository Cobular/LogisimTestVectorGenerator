from typing import List

from custom_types import (
    InputOutputCase,
    InputOutputShapeElement,
)
from src.TestVector import TestVector
from bitwise_ops import bitwise_xor, bitwise_or, bitwise_and, bitwise_add
from utils import create_all_inputs, flattenInputOutputCase


def SignMagGenerator(input_case: InputOutputCase) -> List[bool]:
    flat_input_bytes: list[bool] = flattenInputOutputCase(input_case)

    first_byte_mask = [False] * 13
    first_byte_mask[0] = True

    # Catch the edge case where the input is minint
    if flat_input_bytes == first_byte_mask:
        return [True] * 13

    # 13 bytes of the mask
    mask: list[bool] = [flat_input_bytes[0] for i in
                        range(len(flat_input_bytes))]

    magnitude = bitwise_xor(bitwise_add(flat_input_bytes, mask, False), mask)

    return bitwise_or(
        magnitude, bitwise_and(flat_input_bytes, first_byte_mask)
        )


def RunSignMag(file: str = "test_vectors/sign_mag.txt"):
    TestVector(
        [InputOutputShapeElement(label="TWOS_COMP", width=13)],
        [InputOutputShapeElement(label="SIGN_MAG", width=13)],
        SignMagGenerator,
        create_all_inputs,
        file,
        print_header=False
    )

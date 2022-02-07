import math
from functools import reduce
from typing import List, Callable, Optional

from custom_types import InputOutputShapeElement, InputOutputCaseElement, \
    InputOutputCase


def flattenInputOutputCase(input_case: InputOutputCase) -> List[bool]:
    """
    Reduces a whole InputOutputCase to a bool array
    :param input_case:
    :return:
    """
    return list(
        reduce(
            lambda a, b: a + b,
            [inputOutputCaseElement.state for
             inputOutputCaseElement
             in input_case]
        )
    )


def flattenInputOutputCaseToString(input_case: InputOutputCase) -> str:
    """
    Reduces a whole InputOutputCase to one long string of 1 and 0
    :param input_case:
    :return:
    """
    func: Callable[[str, bool], str] = \
        lambda prev, current: prev + str(int(current))
    return reduce(
        func, flattenInputOutputCase(input_case), ""
    )


def flattenInputOutputElementToString(
    input_case: InputOutputCaseElement
) -> str:
    """
    Reduces an InputOutputCaseElement to a string of 1 and 0
    :param input_case:
    :return:
    """
    func: Callable[[str, bool], str] = \
        lambda prev, current: prev + str(int(current))
    return reduce(
        func, input_case.state, ""
    )


def create_all_inputs(
    input_shape: List[InputOutputShapeElement]
) -> List[InputOutputCase]:
    """
    Generates every one of the 2^n possible inputs for the input space
    :param input_shape:
    :return:
    """
    input_bits = 0
    for input in input_shape:
        input_bits += input.width
    total_inputs = 2 ** input_bits

    format_str = "{0:0" + str(input_bits) + "b}"

    inputs: List[InputOutputCase] = []
    for i in range(total_inputs):
        raw_input_bits = [bool(int(j)) for j in format_str.format(i)]
        inputCase: List[InputOutputCaseElement] = []
        for inputShapeCase in input_shape:
            inputCase.append(
                InputOutputCaseElement(
                    inputShapeCase.label,
                    inputShapeCase.width,
                    tuple(raw_input_bits[:inputShapeCase.width])
                )
            )
            raw_input_bits = raw_input_bits[inputShapeCase.width:]
        inputs.append(
            tuple(inputCase)
        )

    return inputs


def create_one_hot_inputs(
    input_shape: List[InputOutputShapeElement]
) -> List[InputOutputCase]:
    """
    Generates one-hot inputs for the whole input space
    :param input_shape: The shape of inputs you'd like this to generate for
    :return:
    """
    total_inputs = 0
    for input in input_shape:
        total_inputs += input.width

    inputs: List[InputOutputCase] = []
    for i in range(total_inputs):
        raw_input_bits = [False] * total_inputs
        raw_input_bits[i] = True
        inputCase: List[InputOutputCaseElement] = []
        for inputShapeCase in input_shape:
            inputCase.append(
                InputOutputCaseElement(
                    inputShapeCase.label,
                    inputShapeCase.width,
                    tuple(raw_input_bits[:inputShapeCase.width])
                )
            )
            raw_input_bits = raw_input_bits[inputShapeCase.width:]
        inputs.append(
            tuple(inputCase)
        )

    return inputs


def int_to_byte_str(inp: int, length: Optional[int] = None) -> str:
    """
    Converts the specified input number into a string representing the
    binary number equivalent.

    :param inp: The input number
    :param length: The length of the binary number you want (# of bits)
    :return: The result as a binary number
    """
    if length is None:
        length = math.ceil(math.log2(inp))
    format_str = "{0:0" + str(length) + "b}"
    return format_str.format(inp)


def int_to_byte_arr(inp: int, length: Optional[int] = None) -> List[bool]:
    """
    Converts the specified input number into a byte array of the binary
    number equivalent.

    :param inp: The input number
    :param length: The length of the binary number you want (# of bits)
    :return: The result as a binary number
    """
    if length is None:
        length = math.ceil(math.log2(inp))
    format_str = "{0:0" + str(length) + "b}"
    return [bool(int(byte)) for byte in format_str.format(inp)]

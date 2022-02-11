import unittest
from typing import List, Tuple

from

from custom_types import InputOutputCase, InputOutputShapeElement
from src.TestVector import TestVector
from utils import flattenInputOutputElementToString, int_to_byte_arr, \
    create_all_inputs, bitCollectionToString

EightBitIntList = List[bool, ...]
EightBitIntTuple = Tuple[bool, ...]


class InputError(Exception):
    pass


def add(a: EightBitIntTuple, b: EightBitIntTuple) -> Tuple[
    EightBitIntList, bool]:
    int_a = int(bitCollectionToString(a), 2)
    int_b = int(bitCollectionToString(b), 2)
    sum_res = int_to_byte_arr(int_a + int_b)
    flag = False
    if len(sum_res) > 8:
        flag = True
    add_res = [False] * 8
    for index, _ in enumerate(sum_res):
        if index >= len(add_res):
            break
        add_res[-(index + 1)] = sum_res[- (index + 1)]
    return add_res, flag


def sub(a: EightBitIntTuple, b: EightBitIntTuple) -> Tuple[
    EightBitIntList, bool]:
    pass


def mul(a: EightBitIntTuple, b: EightBitIntTuple) -> Tuple[
    EightBitIntList, bool]:
    int_a = int(bitCollectionToString(a), 2)
    int_b = int(bitCollectionToString(b), 2)
    mul_res = int_to_byte_arr(int_a * int_b)
    flag = False
    if len(mul_res) > 8:
        flag = True
    res = [False] * 8
    for index, _ in enumerate(mul_res):
        if index >= len(res):
            break
        res[-(index + 1)] = mul_res[- (index + 1)]
    return res, flag


def div(a: EightBitIntTuple, b: EightBitIntTuple) -> Tuple[
    EightBitIntList, bool]:
    int_a = int(bitCollectionToString(a), 2)
    int_b = int(bitCollectionToString(b), 2)
    rem_res = [False] * 8
    if int_b == 0:
        return rem_res, True
    pass


def rem(a: EightBitIntTuple, b: EightBitIntTuple) -> Tuple[
    EightBitIntList, bool]:
    int_a = int(bitCollectionToString(a), 2)
    int_b = int(bitCollectionToString(b), 2)
    rem_res = [False] * 8
    if int_b == 0:
        return rem_res, True
    rem_res = int_to_byte_arr(int_a % int_b)
    for index, _ in enumerate(rem_res):
        if index >= len(rem_res):
            break
        rem_res[-(index + 1)] = rem_res[- (index + 1)]
    return rem_res, False


def and_(a: EightBitIntTuple, b: EightBitIntTuple) -> Tuple[
    EightBitIntList, bool]:
    and_res = [a_elem and b_elem for a_elem, b_elem in zip(a, b)]
    flag = bitCollectionToString(and_res) == "00000000"
    return and_res, flag


def or_(a: EightBitIntTuple, b: EightBitIntTuple) -> Tuple[
    EightBitIntList, bool]:
    or_res = [a_elem or b_elem for a_elem, b_elem in zip(a, b)]
    flag = bitCollectionToString(or_res) == "00000000"
    return or_res, flag


def not_(a: EightBitIntTuple) -> Tuple[EightBitIntList, bool]:
    not_res = [not a_elem for a_elem in a]
    flag = bitCollectionToString(not_res) == "00000000"
    return not_res, flag


def TaskSevenGenerator(input_case: InputOutputCase) -> List[bool]:
    opCode: str = flattenInputOutputElementToString(input_case[0])
    aBytes = input_case[1].state
    bBytes = input_case[2].state

    overall_res: Tuple[EightBitIntList, bool]
    if opCode == "000":
        overall_res = add(aBytes, bBytes)
    elif opCode == "001":
        overall_res = sub(aBytes, bBytes)
    elif opCode == "010":
        overall_res = mul(aBytes, bBytes)
    elif opCode == "011":
        overall_res = div(aBytes, bBytes)
    elif opCode == "100":
        overall_res = rem(aBytes, bBytes)
    elif opCode == "101":
        overall_res = and_(aBytes, bBytes)
    elif opCode == "110":
        overall_res = or_(aBytes, bBytes)
    elif opCode == "111":
        overall_res = not_(aBytes)
    else:
        raise InputError("Incorrect Value for Opcode")

    return overall_res[0] + [overall_res[1]]


def RunTaskSeven(file: str = "test_vectors/da1p7.txt"):
    TestVector(
        [
            InputOutputShapeElement(label="OP", width=3),
            InputOutputShapeElement(label="A", width=8),
            InputOutputShapeElement(label="B", width=8)
        ],
        [
            InputOutputShapeElement(label="Z", width=8),
            InputOutputShapeElement(label="FLG", width=1),
        ],
        TaskSevenGenerator,
        create_all_inputs,
        file
    )


class TaskSevenTests(unittest.TestCase):
    def test_add_small(self):
        res = add(
            (False, False, False, False, False, False, True, True),
            (False, False, False, False, False, True, True, True)
        )
        self.assertIs(res[1], False)
        self.assertTupleEqual(
            res[0],
            (False, False, False, False, True, False, True, False)
        )

    def test_add_simple(self):
        res = add(
            (True, False, False, False, False, False, True, True),
            (False, False, False, True, False, True, True, True)
        )
        self.assertIs(res[1], False)
        self.assertTupleEqual(
            res[0],
            (True, False, False, True, True, False, True, False)
        )

    def test_add_overflow(self):
        res = add(
            (True, False, False, False, False, False, False, False),
            (True, False, False, False, False, False, False, False)
        )
        self.assertIs(res[1], True)
        self.assertTupleEqual(
            res[0],
            (False, False, False, False, False, False, False, False)
        )

    def test_rem_flag(self):
        res = rem(
            (False, False, False, False, False, False, True, False),
            (False, False, False, False, False, False, False, False),
        )
        self.assertIs(res[1], True)

    def test_rem_simple(self):
        res = rem(
            (True, False, False, True, True, False, True, False),
            (True, False, True, False, True, False, False, True),
        )
        self.assertIs(res[1], False)
        self.assertTupleEqual(
            res[0],
            (True, False, False, True, True, False, True, False)
        )

    def test_and_flag(self):
        res = and_(
            (False, False, False, False, False, False, True, False),
            (True, False, False, False, True, False, False, False),
        )
        self.assertIs(res[1], True)
        self.assertTupleEqual(
            res[0],
            (False, False, False, False, False, False, False, False)
        )

    def test_and_simple(self):
        res = and_(
            (True, False, False, True, True, False, True, False),
            (True, False, True, False, True, False, False, True),
        )
        self.assertIs(res[1], False)
        self.assertTupleEqual(
            res[0],
            (True, False, False, False, True, False, False, False)
        )

    def test_or_flag(self):
        res = or_(
            (False, False, False, False, False, False, False, False),
            (False, False, False, False, False, False, False, False),
        )
        self.assertIs(res[1], True)
        self.assertTupleEqual(
            res[0],
            (False, False, False, False, False, False, False, False)
        )

    def test_or_simple(self):
        res = or_(
            (False, False, False, False, False, False, True, True),
            (False, True, False, False, False, True, True, True),
        )
        self.assertIs(res[1], False)
        self.assertTupleEqual(
            res[0],
            (False, True, False, False, False, True, True, True)
        )

    def test_not_flag(self):
        res = not_(
            (True, True, True, True, True, True, True, True,),
        )
        self.assertIs(res[1], True)
        self.assertTupleEqual(
            res[0],
            (False, False, False, False, False, False, False, False)
        )

    def test_not_simple(self):
        res = not_(
            (True, True, False, True, False, True, True, False,),
        )
        self.assertIs(res[1], False)
        self.assertTupleEqual(
            res[0],
            (False, False, True, False, True, False, False, True)
        )

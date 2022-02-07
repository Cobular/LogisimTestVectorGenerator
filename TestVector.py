import csv
from typing import List, Dict

from custom_types import InputOutputShapeElement, InputOutputCaseElement, \
    InputOutputCase, RowGenerator, InputGenerator
from utils import flattenInputOutputElementToString


class TestVector:
    """The main class, instantiate to generate a complete test vector"""
    inputShape: List[InputOutputShapeElement]
    outputShape: List[InputOutputShapeElement]
    inputs: List[InputOutputCase]
    results: Dict[InputOutputCase, InputOutputCase]
    generator: RowGenerator

    def __init__(
        self,
        inputs: List[InputOutputShapeElement],
        outputs: List[InputOutputShapeElement],
        result_generator: RowGenerator,
        input_generator: InputGenerator,
        save_path: str
    ):
        """
        Creates and saves a TestVector
        :param inputs: The shape of the inputs this circuit will take
        :param outputs: The shape of the outputs this circuit will take
        :param result_generator: The function to call on each row to
        evaluate the result
        :param input_generator: The function to generate all valid inputs
        :param save_path: The path to save the test vector to
        """
        self.inputShape = inputs
        self.outputShape = outputs
        self.generator = result_generator

        self.inputs = input_generator(inputs)
        self.generate_rows()
        self.save_results(save_path)

    def generate_rows(self):
        results: Dict[InputOutputCase, InputOutputCase] = {}
        for inputCase in self.inputs:
            raw_result = self.generator(inputCase)
            this_case_res: List[InputOutputCaseElement] = []
            for outputShapeElement in self.outputShape:
                this_case_res.append(
                    InputOutputCaseElement(
                        label=outputShapeElement.label,
                        width=outputShapeElement.width,
                        state=tuple(raw_result[:outputShapeElement.width])
                    )
                )
                raw_result = raw_result[outputShapeElement.width:]
            results[inputCase] = tuple(this_case_res)
        self.results = results

    def save_results(self, path: str):
        with open(path, "w") as file:
            writer = csv.writer(file, delimiter=" ")
            header: List[str] = [f"{thing.label}[{thing.width}]" for thing in
                                 self.inputShape +
                                 self.outputShape]
            writer.writerow(header)

            body: List[List[str]] = []
            for inputs, outputs in self.results.items():
                this_row: List[str] = [flattenInputOutputElementToString(thing)
                                       for thing in inputs + outputs]
                body.append(this_row)
            writer.writerows(body)

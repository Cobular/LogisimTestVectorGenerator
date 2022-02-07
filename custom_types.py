from dataclasses import dataclass
from typing import Tuple, Callable, List


@dataclass(frozen=True)
class InputOutputShapeElement:
    """
    A dataclass to describe the shape of an input or output
    """
    label: str
    width: int


@dataclass(frozen=True)
class InputOutputCaseElement(InputOutputShapeElement):
    """
    A dataclass to describe an instance of an input or an output, complete
    with state.
    """
    state: Tuple[bool, ...]


# A case of a whole input or output, including possibly multiple in/out-puts
InputOutputCase = Tuple[InputOutputCaseElement, ...]

# The expected type of a function to generate a row solution
RowGenerator = Callable[[InputOutputCase], List[bool]]

# The expected type of a function to generate an input
InputGenerator = Callable[
    [List[InputOutputShapeElement]],
    List[InputOutputCase]
]

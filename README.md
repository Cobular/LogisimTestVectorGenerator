# Logisim-Evolution Test Vector Generator

_Logisim test vector generation made easy!_

Recently, the powerful digital circuit design learning tool Logisim 
received an update to support Test Vectors, essentially a file containing 
the spec for unit tests of your circuit. However, those must be manually 
generated, which is prone to mistakes and other weird issues and can be a 
PITA when you're taking about like 128 lines of cases.

Instead, we can just utilize Python to generate these test vectors for us, 
allowing for much more reliable and robust testing than would otherwise be 
possible!

This project facilitates the generation of these test vector files, 
allowing you to easily create your own functions to generate the inputs and 
outputs of your circuit while the project does the bulk of the work of 
coordinating these functions and formatting that whole mess into a test 
vector file. 

#### Liability Notice
I can't guarantee that this works perfectly or even properly. I plan to use 
it for the class project and plan to keep it updated as I catch bugs but I 
make no guarantees that this will always spit out the right answer or 
anything like that. Use at your own risk.

# Using
Just clone the project and run `python ./main.py` to generate all the 
described test vectors. It's dead simple!

## Example + Making your own
Let's look at a very simple spec for a circuit:

> Using Logisim and only NAND gates, implement an 8→3 encoder with input A[7:0] and output X[2:0].

Based on this spec, we can tell that we should:

1. Expect inputs to be one-hot
2. Expect outputs to be the binary-encoded representation of that one-hot value

Generating all these cases by hand would be totally possible, in fact here 
they are:

```
A[8] X[3]
10000000 111
01000000 110
00100000 101
00010000 100
00001000 011
00000100 010
00000010 001
00000001 000
```

Now let's look at the code to generate these:

```python
# 4
def TaskOneGenerator(input_case: InputOutputCase) -> List[bool]:
    flatInputBytes: list[bool] = flattenInputOutputCase(input_case)

    counter = 0
    for index, val in enumerate(flatInputBytes):
        if val is True:
            counter = 7 - index
            break

    return [bool(int(j)) for j in "{0:03b}".format(counter)]


task1 = TestVector(
    [InputOutputShapeElement(label="A", width=8)], # 1
    [InputOutputShapeElement(label="X", width=3)], # 2
    TaskOneGenerator, # 4
    create_one_hot_inputs, # 3
    "test_vectors/da1p1.txt"
)
```

You can see this has codified the whole spec of the problem! We have the 
input shape (1), the output shape (2), the spec for the inputs (3), and the 
spec for turning inputs into outputs (4)! This code will nicely and 
perfectly generate the test cases for the described problem.

## More Examples
Please see main.py, it has 2 additional and more complex examples.

## Contributions
This has been made for the Winter 2022 ECE M16 class at UCLA, and if you're 
in this class too, I'd love contributions with the rest of the generators! 
I haven't had time to make em yet but if you do, please please open a PR so 
we can all benefit! The problem spec explicitly encourages us to share and 
work together on test vectors, so this should be totally fair game! 

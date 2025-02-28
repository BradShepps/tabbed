import pytest
import random
import string
from typing import Callable, Generator, TypeVar
import re


# Fixture for returning a random number generator
@pytest.fixture
def rn_generator():
    """Returns a random number generator with the seed 1"""

    return random.Random(1)

# Numeric-related Fixtures
@pytest.fixture
def integer_generator(rn_generator):
    """This returns a generator of random integers with a set seed to be deterministic"""

    def integer_generator():
        while True:
            yield str(rn_generator.randint(-100000, 100000))
    return integer_generator()

@pytest.fixture
def float_generator(rn_generator):
    """This returns a generator of random floats with a set seed to be deterministic"""

    def float_generator():
        while True:
            yield str(rn_generator.uniform(-100000, 100000))
    return float_generator()

@pytest.fixture
def complex_generator(rn_generator):
    """This returns a generator of random complex numbers with a set seed to be deterministic"""

    def complex_generator():
        while True:
            real_part = rn_generator.uniform(-100000, 100000)
            imag_part = rn_generator.uniform(-100000, 100000)
            num = complex(real_part, imag_part)

            yield str(num)

    return complex_generator()

@pytest.fixture
def scientific_notation_float_generator(rn_generator):
    """Returns generator of valid float with scientific notation as a string"""

    def sci_not_float_gen():
        while True:
            significand = rn_generator.uniform(-10, 10)
            exponent = rn_generator.randint(-100, 100)
            if (rn_generator.random() > .5):
                yield str(significand) + "E" + str(exponent)
            else:
                yield str(significand) + "e" + str(exponent)
    
    return sci_not_float_gen()

@pytest.fixture
def numeric_generator(rn_generator, integer_generator, float_generator, complex_generator):
    """Returns a generator of numeric values, which can be integer, float, or complex"""

    def numeric_generator():
        while True:
            rand_num = rn_generator.random()
            if (rand_num < 1/3):
                yield next(integer_generator)
            elif (rand_num < 2/3):
                yield next(float_generator)
            else:
                yield next(complex_generator)
    return numeric_generator()

@pytest.fixture
def non_numeric_generator(rn_generator):
    """Returns a generator of random non-numeric strings"""

    def non_numeric_generator():
        while True:
            length = rn_generator.randint(1, 20)
            all_chars = string.printable.strip()

            rand_str = "".join(rn_generator.choices(all_chars, k=length))

            non_numeric_insert_pos = rn_generator.randint(0, length+1)

            non_numeric_punctuation = re.sub(r"[.,\+\-]", "", string.punctuation)
            non_numeric_ascii = re.sub(r"[jJeE]", "", string.ascii_letters)
            non_numeric_char = rn_generator.choice(non_numeric_ascii + non_numeric_punctuation)

            # Inserting a non-numeric character always ensures the whole string is non-numeric
            rand_non_numeric = rand_str[:non_numeric_insert_pos] + non_numeric_char + rand_str[non_numeric_insert_pos:]

            yield rand_non_numeric

    return non_numeric_generator()

@pytest.fixture
def string_generator(rn_generator):
    """Returns a generator of random strings"""

    def string_generator():
        while True:
            length = rn_generator.randint(0, 30)
            all_chars = string.printable.strip()
            rand_str = "".join(rn_generator.choices(all_chars, k=length))

            yield rand_str

    return string_generator()

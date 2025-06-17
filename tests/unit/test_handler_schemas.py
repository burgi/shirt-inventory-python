# pylint: disable = print-used,
from datetime import datetime

import pytest
from pydantic import ValidationError

from lambda_handlers.crud.handlers.schemas.input import ItemInput


def random_string(length: int = 8) -> str:
    """Generate a random string of fixed length."""
    import random
    import string
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def test_valid_item_input():
    ItemInput(name=random_string())


def test_invalid_item_input():
    with pytest.raises(ValidationError):
        ItemInput()


def test_invalid_item_input_over_max_length():
    with pytest.raises(ValidationError):
        ItemInput(name=random_string(21))

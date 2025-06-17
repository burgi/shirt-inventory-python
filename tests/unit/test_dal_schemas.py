# pylint: disable = print-used,
import pytest
from infra_automation_utils.random_utils import random_string
from pydantic import ValidationError

from lambda_handlers.crud.dal.schemas.item_schema import ShirtItem


def test_valid_item_entry_schema():
    ShirtItem(
        id=1,
        name=random_string(8),
        created_date=1638092065,
        updated_date=1638093065,
        target='developer',
        color='green',
        size=50,
    )


def test_invalid_entry_schema():
    with pytest.raises(ValidationError):
        ShirtItem(
            created_date='-1',
            updated_date=1638093065,
            target='developer',
        )


def test_invalid_updated_date_entry_schema():
    with pytest.raises(ValidationError):
        ShirtItem(
            created_date=1638093065,
            updated_date=3.3,
            target='developer',
        )


def test_invalid_entry_schema_over_max_length():
    with pytest.raises(ValidationError):
        ShirtItem(
            name=random_string(21),
            created_date=1638092065,
            updated_date=1638093065,
            target='developer',
        )


def test_invalid_item_entry():
    with pytest.raises(ValidationError):
        ShirtItem()


def test_invalid_item_entry_over_max_length():
    with pytest.raises(ValidationError):
        ShirtItem(name=random_string(21))

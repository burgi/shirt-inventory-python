# pylint: disable=no-name-in-module
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, constr, validator


def validate_posix_date(value: float) -> float:
    try:
        datetime.fromtimestamp(value)
    except ValueError as exc:
        raise ValueError(f'{value} is not a valid datetime') from exc
    return value


class ShirtTarget(StrEnum):
    MEN = 'MEN'
    WOMEN = 'WOMEN'
    BOYS = 'BOYS'
    GIRLS = 'GIRLS'


class ShirtItem(BaseModel):
    id: Any  # should be unique
    name: constr(min_length=1, max_length=20)
    created_date: float
    updated_date: float
    target: ShirtTarget
    color: str  # red, orange, yellow, green, blue, indigo and violet
    size: Any  # S/M/L/XL/XXL for adults, 1-10 for kids

    _validate_created_date = validator('created_date', allow_reuse=True)(validate_posix_date)
    _validate_updated_date = validator('updated_date', allow_reuse=True)(validate_posix_date)

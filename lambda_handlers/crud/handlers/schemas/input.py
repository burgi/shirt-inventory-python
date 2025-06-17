# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods,no-self-use
import json
from typing import Any, Optional

from pydantic import BaseModel, constr, validator

from lambda_handlers.crud.dal.schemas.item_schema import ShirtTarget


class ItemInput(BaseModel):
    name: constr(min_length=1, max_length=20)
    color: Optional[str] = 'blue'
    size: Optional[Any] = 'M'
    target: Optional[ShirtTarget] = ShirtTarget.MEN


class GetItemsInputPathParams(BaseModel):
    name: constr(min_length=1)


class GetInput(BaseModel):
    queryStringParameters: Optional[GetItemsInputPathParams] = None


class UpdateInput(BaseModel):
    queryStringParameters: Optional[GetItemsInputPathParams]
    body: ItemInput

    # this is a nice trick that will turn the string json body into a dict so it can be parsed into a ItemInput type
    # pydantic is a parser as much as it is a validator
    @validator('body', pre=True)
    def transform_body_to_dict(cls, value):
        return json.loads(value)

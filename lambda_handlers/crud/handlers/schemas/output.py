# pylint: disable=no-name-in-module,no-self-argument,too-few-public-methods,no-self-use
from typing import Optional

from pydantic import BaseModel, Field, constr


class ApiBasicError(BaseModel):
    code: constr(min_length=1) = Field(description='An application-specific error code.')
    message: constr(min_length=1) = Field(description='A human-readable explanation specific to this occurrence of the problem.')
    description: Optional[str] = Field(default='', description='Optional additional details of the specific error.')

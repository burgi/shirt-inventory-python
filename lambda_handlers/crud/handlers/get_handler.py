#pylint: disable=no-value-for-parameter, no-else-return, unused-variable, unnecessary-comprehension
import json
import logging
from http import HTTPStatus
from logging import Logger
from typing import Any, Dict, List

from aws_lambda_context import LambdaContext
from pydantic import ValidationError

from lambda_handlers.crud.dal.repository import ITEMS
from lambda_handlers.crud.dal.schemas.item_schema import ShirtItem
from lambda_handlers.crud.handlers.schemas.input import GetInput
from lambda_handlers.crud.handlers.utils.responses import build_error_response, build_response, build_response_from_str


def get_items_from_db() -> List[ShirtItem]:
    items = [val for val in ITEMS.values()]
    return items


def handle_get_requests(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:  #pylint: disable=unused-argument
    logger: Logger = logging.getLogger()

    # validate input
    try:
        get_input: GetInput = GetInput.model_validate_json(json.dumps(event))
    except (ValidationError, TypeError) as err:
        return build_error_response(err, HTTPStatus.BAD_REQUEST)

    if get_input.queryStringParameters:
        name = get_input.queryStringParameters.name

        # when getting all the items, they should be sorted by rainbow color and size:
        # color values sort order: red, orange, yellow, green, blue, indigo and violet
        # size values sort order: S/M/L/XL/XXL for adults, 1-10 for kids. Adults should come first
        logger.info('get_item got a request')

        items = get_items_from_db()
        ret_val: ShirtItem = None

        for item in items:
            if item.name == name:
                ret_val = item

        logger.info('finished handling get by name request successfully')
        return build_response(HTTPStatus.OK, ret_val.dict())

    else:
        logger.info('get_items got a request')
        items = [item.dict() for item in get_items_from_db()]
        return build_response_from_str(HTTPStatus.OK, json.dumps(items))

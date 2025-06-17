#pylint: disable=no-value-for-parameter, unused-import
import logging
import time
from http import HTTPStatus
from logging import Logger
from typing import Any, Dict

from aws_lambda_context import LambdaContext
from pydantic import ValidationError

from lambda_handlers.crud.dal.repository import ITEMS, FileRepository
from lambda_handlers.crud.dal.schemas.item_schema import ShirtItem, ShirtTarget
from lambda_handlers.crud.handlers.schemas.input import ItemInput
from lambda_handlers.crud.handlers.utils.exceptions import BadRequestException, InternalSystemException
from lambda_handlers.crud.handlers.utils.responses import build_error_response, build_response


def create_item_in_db(item_input: ItemInput) -> ShirtItem:
    # generate unique identifier
    new_id = max(ITEMS.keys(), default=0) + 1
    now: float = float(time.time())

    item_entry = ShirtItem(
        id=new_id,
        name=item_input.name,
        created_date=now,
        updated_date=now,
        target=ShirtTarget.MEN,
        color='blue',
        size=item_input.size,
    )

    ITEMS[item_entry.name] = item_entry

    return item_entry


# POST /api/item
def create_item(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:  #pylint: disable=unused-argument
    logger: Logger = logging.getLogger()

    # validate input
    try:
        item_input: ItemInput = ItemInput.model_validate_json(event.get('body', '{}'))
        logger.info('got a create request')
    except (ValidationError, TypeError) as err:
        return build_error_response(err, HTTPStatus.BAD_REQUEST)

    # input is valid, pass input to business logic and get a parsed return object to return to caller
    try:
        new_entry: ShirtItem = create_item_in_db(item_input)
    except BadRequestException as bex:
        logger.exception('unable to complete create action, bad request')
        return build_error_response(bex, HTTPStatus.BAD_REQUEST)
    except InternalSystemException as iex:
        logger.exception('unable to complete create action, internal server error')
        return build_error_response(iex, HTTPStatus.INTERNAL_SERVER_ERROR)

    logger.info('finished handling request successfully')
    return build_response(http_status=HTTPStatus.CREATED, body=new_entry.model_dump())

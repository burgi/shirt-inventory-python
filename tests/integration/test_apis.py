from http import HTTPStatus

from lambda_handlers.crud.dal.schemas.item_schema import ShirtItem
from lambda_handlers.crud.handlers.create_handler import create_item
from lambda_handlers.crud.handlers.get_handler import handle_get_requests
from lambda_handlers.crud.handlers.schemas.input import ItemInput
from tests.integration.test_utils import generate_api_gateway_request, generate_context

ITEM_NAME = 'item name'
COLOR = 'red'
SIZE = 'XL'


def test_create_and_get():
    create_body = ItemInput(name=ITEM_NAME, color=COLOR, size=SIZE)
    create_event = generate_api_gateway_request(
        uri='/api/item',
        method='POST',
        body=create_body.model_dump_json(),
    )
    response = create_item(
        event=create_event, context=generate_context('create_item'))
    assert response.get('statusCode') == HTTPStatus.CREATED
    new_item: ShirtItem = ShirtItem.model_validate_json(response.get('body'))
    assert new_item.name == ITEM_NAME

    get_event = generate_api_gateway_request(
        uri='/api/item',
        query_string_params={'name': ITEM_NAME},
    )
    response = handle_get_requests(
        event=get_event, context=generate_context('handle_get_requests'))
    assert response.get('statusCode') == HTTPStatus.OK
    item = ShirtItem.model_validate_json(response.get('body'))
    assert item.name == ITEM_NAME
    assert item.color == COLOR
    assert item.size == SIZE

import json
from http import HTTPStatus

from lambda_handlers.crud.handlers.create_handler import create_item
from lambda_handlers.crud.handlers.get_handler import handle_get_requests
from lambda_handlers.crud.handlers.schemas.input import ItemInput
from tests.integration.test_utils import generate_api_gateway_request, generate_context


def test_create_and_get_with_sort():
    with open('tests/integration/test_data.json') as f:
        test_data = json.load(f)
        unsorted_shirts = test_data['items']
        sorted_shirts_names = test_data['sorted_items']
    for item in unsorted_shirts:
        create_body = ItemInput(**item)
        create_event = generate_api_gateway_request(
            uri='/api/item',
            method='POST',
            body=create_body.model_dump_json(),
        )
        response = create_item(
            event=create_event, context=generate_context('create_item'))
        assert response.get('statusCode') == HTTPStatus.CREATED

    get_event = generate_api_gateway_request(uri='/api/item',)
    response = handle_get_requests(
        event=get_event, context=generate_context('handle_get_requests'))
    assert response.get('statusCode') == HTTPStatus.OK
    items = json.loads(response.get('body'))
    assert len(items) == 14
    for i in range(len(items)):
        assert items[i]['name'] == sorted_shirts_names[i]

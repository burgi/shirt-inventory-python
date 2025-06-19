from typing import Dict, List, Optional
from uuid import uuid4

from aws_lambda_context import LambdaClientContext, LambdaContext


def generate_api_gateway_request(
    uri: str,
    body: Optional[str] = '',
    method: Optional[str] = 'GET',
    path_params: Optional[Dict[str, str]] = None,
    origin=None,
    tenant_id=None,
    query_string_params: Optional[Dict[str, str]] = None,
    multi_value_query_string_params: Optional[Dict[str, List[str]]] = None,
) -> Dict:
    res = {
        'resource': f'/api/{uri}',
        'path': f'/api/{uri}',
        'httpMethod': method,
        'headers': {
            'Accept':
                '*/*',
            'Accept-Encoding':
                'gzip, deflate'
        },
        'multiValueHeaders': {
            'Accept': ['*/*'],
            'Accept-Encoding': ['gzip, deflate'],
            'User-Agent': ['python-requests/2.28.1'],
        },
        'requestContext': {
            'resourcePath': '/api/',
            'httpMethod': 'GET',
            'protocol': 'HTTP/1.1',
        },
        'body': body,
        'isBase64Encoded': False
    }
    if origin is not None:
        res['headers']['origin'] = origin

    if tenant_id is not None:
        res['headers']['tenant_id'] = tenant_id

    if path_params is not None:
        res['pathParameters'] = path_params

    if query_string_params is not None:
        res['queryStringParameters'] = query_string_params

    if multi_value_query_string_params is not None:
        res['multiValueQueryStringParameters'] = multi_value_query_string_params

    return res


def generate_context(handler_name: str) -> LambdaContext:
    context = LambdaContext()
    context.client_context = LambdaClientContext()
    context.client_context.custom = {}
    context.aws_request_id = str(uuid4())
    context.function_name = handler_name
    return context

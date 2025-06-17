import json
from http import HTTPStatus
from typing import Any, Dict, Optional

from lambda_handlers.crud.handlers.schemas.output import ApiBasicError


def build_response(http_status: HTTPStatus, body: Dict[str, Any]) -> Dict[str, Any]:
    return build_response_from_str(http_status=http_status, body=json.dumps(body))


def build_response_from_str(http_status: HTTPStatus, body: str) -> Dict[str, Any]:
    return {'statusCode': http_status, 'headers': {'Content-Type': 'application/json'}, 'body': body}


def build_error_response(err: Exception, status: Optional[HTTPStatus] = HTTPStatus.INTERNAL_SERVER_ERROR) -> Dict[str, Any]:
    return {
        'statusCode': status,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': ApiBasicError(code=status.value, message=status.phrase, description=str(err)).json(),
    }

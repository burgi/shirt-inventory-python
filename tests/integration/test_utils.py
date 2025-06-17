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
                'gzip, deflate',
            'Host':
                'usroinvppa.execute-api.us-east-1.amazonaws.com',
            'User-Agent':
                'python-requests/2.28.1',
            'x-amz-content-sha256':
                'amz-content-sha256',
            'x-amz-date':
                '20220807T111845Z',
            'X-Amz-Security-Token':
                'amz-security-token',
            'X-Amzn-Trace-Id':
                'Root=1-62ef9f96-38d3bdf74e975b49347bfcb7',
            'X-Auth':
                'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhFMDFFQTZDMkM1NkIxRkFDQ0REMzBDOEIxMDIxMkM5M0MyMkUwNDAiLCJ4NXQiOiJqZ0hxYkN4V3Nmck0zVERJc1FJU3lUd2k0RUEiLCJhcHBfaWQiOiJfX2lkYXB0aXZlX2N5YnJfdXNlcl9vaWRjIn0.eyJwcmVmZXJyZWRfdXNlcm5hbWUiOiJjb2ItcHJpbWFyeUBjeWJlcmFyay5jbG91ZC4xNjYwODMiLCJmYW1pbHlfbmFtZSI6ImNvYi1wcmltYXJ5IiwidGVuYW50X3N1YmRvbWFpbiI6Imh0dHBzOi8vY29iLXByaW1hcnkuc2hlbGwuY3liZXJhcmstZXZlcmVzdC1kZXYuY29tIiwidW5pcXVlX25hbWUiOiJjb2ItcHJpbWFyeUBjeWJlcmFyay5jbG91ZC4xNjYwODMiLCJpZGFwdGl2ZV90ZW5hbnRfaWQiOiJBRlI1MzI2IiwidGVuYW50X2lkIjoiNmY3MDRhNzctMzk5MC00OTI3LTkwNTgtMzI2YjE3ZDVlMWE2IiwidXNlcl9yb2xlcyI6WyJTeXN0ZW0gQWRtaW5pc3RyYXRvciIsIkRwYUFkbWluIiwiRXZlcnlib2R5IiwiZ2xvYmFsIGF1ZGl0b3IiXSwiaWF0IjoxNzAyNDY2NTI4LCJzdWIiOiJjMmM3YmNjNi05NTYwLTQ0ZTAtOGRmZi01YmUyMjFjZDM3ZWUiLCJhdXRoX3RpbWUiOjE3MDI0NTY1MDksInJ0X3JlZiI6IjJBRjAzRjJGNjUzODU2NkIxNzY3NzdBRTlGMDE1Q0UzNzA4MkJCQkYiLCJleHAiOjE3MDI0Njc0MjgsInVzZXJfdXVpZCI6ImMyYzdiY2M2LTk1NjAtNDRlMC04ZGZmLTViZTIyMWNkMzdlZSIsInNjb3BlIjoib3BlbmlkIGFwaSBwcm9maWxlIiwibGFzdF9sb2dpbiI6IjE3MDIzOTAyMjIiLCJhdWQiOiJfX2lkYXB0aXZlX2N5YnJfdXNlcl9vaWRjIiwiYXdzX3JlZ2lvbiI6InVzLWVhc3QtMSIsInN1YmRvbWFpbiI6ImNvYi1wcmltYXJ5IiwiY3NyZl90b2tlbiI6IkJ2U3Fid1NUWmt1bk5EclVzMTIwWVoxc3owRkZmdmRJcTdTbzhtLWxObXMxIiwiaW50ZXJuYWxfc2Vzc2lvbl9pZCI6IjBlNmI4YzBkLTIxY2UtNDg5OS1hM2IxLWNhODI3M2FmZDQwYSIsInBsYXRmb3JtX2RvbWFpbiI6InNoZWxsLmN5YmVyYXJrLWV2ZXJlc3QtZGV2LmNvbSIsImlzcyI6Imh0dHBzOi8vYWZyNTMyNi5pZC5pbnRlZ3JhdGlvbi1jeWJlcmFyay5jbG91ZC9fX2lkYXB0aXZlX2N5YnJfdXNlcl9vaWRjLyIsImF0X2hhc2giOiJpcl9rMmlVODBUNC1uVDk5ZkU2ZXJ3IiwibmFtZSI6ImNvYi1wcmltYXJ5IiwiZ2l2ZW5fbmFtZSI6ImNvYi1wcmltYXJ5IiwiRXh0ZXJuYWxVdWlkIjoiYzJjN2JjYzYtOTU2MC00NGUwLThkZmYtNWJlMjIxY2QzN2VlIn0.B06m3947Y7ruwoGfBQ3_T6jLLVR8NCp38S_Fhhz1zPCI09FecVUIAJSP55X8j3o6iKFtVxTIECI-uUOAdHYnk1A6iW1AqYlzqrjpDJ-t3R2Aw_4Mk_n_cEz03huT-VaKBK_f8QTSLSgy-kh_RDzNK09d6jXeCuQt5fxCltNjhisQJbHV9OCmNgnUQweoqpKdaZ-E_jK9lPpBHd7Mr_-OW4olhi69c7VVPsgXn5mAqzBrnqWPXq3AidZlEO5eppA4pHQSqeTCNtXUnPoXh0NIhzAX_ki1lHujmIjox3stdEfuwDL_wKOrpR-tYTMLO9oeopZj_lDrr95kxfhgllEHtg',
            'X-Forwarded-For':
                '194.90.225.101',
            'X-Forwarded-Port':
                '443',
            'X-Forwarded-Proto':
                'https'
        },
        'multiValueHeaders': {
            'Accept': ['*/*'],
            'Accept-Encoding': ['gzip, deflate'],
            'Host': ['usroinvppa.execute-api.us-east-1.amazonaws.com'],
            'User-Agent': ['python-requests/2.28.1'],
            'x-amz-content-sha256': ['amz-content-sha256'],
            'x-amz-date': ['20220807T111845Z'],
            'X-Amz-Security-Token': ['amz-security-token'],
            'X-Amzn-Trace-Id': ['Root=1-62ef9f96-38d3bdf74e975b49347bfcb7'],
            'X-Auth': [
                'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhFMDFFQTZDMkM1NkIxRkFDQ0REMzBDOEIxMDIxMkM5M0MyMkUwNDAiLCJ4NXQiOiJqZ0hxYkN4V3Nmck0zVERJc1FJU3lUd2k0RUEiLCJhcHBfaWQiOiJfX2lkYXB0aXZlX2N5YnJfdXNlcl9vaWRjIn0.eyJwcmVmZXJyZWRfdXNlcm5hbWUiOiJjb2ItcHJpbWFyeUBjeWJlcmFyay5jbG91ZC4xNjYwODMiLCJmYW1pbHlfbmFtZSI6ImNvYi1wcmltYXJ5IiwidGVuYW50X3N1YmRvbWFpbiI6Imh0dHBzOi8vY29iLXByaW1hcnkuc2hlbGwuY3liZXJhcmstZXZlcmVzdC1kZXYuY29tIiwidW5pcXVlX25hbWUiOiJjb2ItcHJpbWFyeUBjeWJlcmFyay5jbG91ZC4xNjYwODMiLCJpZGFwdGl2ZV90ZW5hbnRfaWQiOiJBRlI1MzI2IiwidGVuYW50X2lkIjoiNmY3MDRhNzctMzk5MC00OTI3LTkwNTgtMzI2YjE3ZDVlMWE2IiwidXNlcl9yb2xlcyI6WyJTeXN0ZW0gQWRtaW5pc3RyYXRvciIsIkRwYUFkbWluIiwiRXZlcnlib2R5IiwiZ2xvYmFsIGF1ZGl0b3IiXSwiaWF0IjoxNzAyNDY2NTI4LCJzdWIiOiJjMmM3YmNjNi05NTYwLTQ0ZTAtOGRmZi01YmUyMjFjZDM3ZWUiLCJhdXRoX3RpbWUiOjE3MDI0NTY1MDksInJ0X3JlZiI6IjJBRjAzRjJGNjUzODU2NkIxNzY3NzdBRTlGMDE1Q0UzNzA4MkJCQkYiLCJleHAiOjE3MDI0Njc0MjgsInVzZXJfdXVpZCI6ImMyYzdiY2M2LTk1NjAtNDRlMC04ZGZmLTViZTIyMWNkMzdlZSIsInNjb3BlIjoib3BlbmlkIGFwaSBwcm9maWxlIiwibGFzdF9sb2dpbiI6IjE3MDIzOTAyMjIiLCJhdWQiOiJfX2lkYXB0aXZlX2N5YnJfdXNlcl9vaWRjIiwiYXdzX3JlZ2lvbiI6InVzLWVhc3QtMSIsInN1YmRvbWFpbiI6ImNvYi1wcmltYXJ5IiwiY3NyZl90b2tlbiI6IkJ2U3Fid1NUWmt1bk5EclVzMTIwWVoxc3owRkZmdmRJcTdTbzhtLWxObXMxIiwiaW50ZXJuYWxfc2Vzc2lvbl9pZCI6IjBlNmI4YzBkLTIxY2UtNDg5OS1hM2IxLWNhODI3M2FmZDQwYSIsInBsYXRmb3JtX2RvbWFpbiI6InNoZWxsLmN5YmVyYXJrLWV2ZXJlc3QtZGV2LmNvbSIsImlzcyI6Imh0dHBzOi8vYWZyNTMyNi5pZC5pbnRlZ3JhdGlvbi1jeWJlcmFyay5jbG91ZC9fX2lkYXB0aXZlX2N5YnJfdXNlcl9vaWRjLyIsImF0X2hhc2giOiJpcl9rMmlVODBUNC1uVDk5ZkU2ZXJ3IiwibmFtZSI6ImNvYi1wcmltYXJ5IiwiZ2l2ZW5fbmFtZSI6ImNvYi1wcmltYXJ5IiwiRXh0ZXJuYWxVdWlkIjoiYzJjN2JjYzYtOTU2MC00NGUwLThkZmYtNWJlMjIxY2QzN2VlIn0.B06m3947Y7ruwoGfBQ3_T6jLLVR8NCp38S_Fhhz1zPCI09FecVUIAJSP55X8j3o6iKFtVxTIECI-uUOAdHYnk1A6iW1AqYlzqrjpDJ-t3R2Aw_4Mk_n_cEz03huT-VaKBK_f8QTSLSgy-kh_RDzNK09d6jXeCuQt5fxCltNjhisQJbHV9OCmNgnUQweoqpKdaZ-E_jK9lPpBHd7Mr_-OW4olhi69c7VVPsgXn5mAqzBrnqWPXq3AidZlEO5eppA4pHQSqeTCNtXUnPoXh0NIhzAX_ki1lHujmIjox3stdEfuwDL_wKOrpR-tYTMLO9oeopZj_lDrr95kxfhgllEHtg'
            ],
            'X-Forwarded-For': ['194.90.225.101'],
            'X-Forwarded-Port': ['443'],
            'X-Forwarded-Proto': ['https']
        },
        'requestContext': {
            'resourceId': 'il9xsq',
            'resourcePath': '/api/aws/organizations',
            'httpMethod': 'GET',
            'extendedRequestId': 'WfXfeEV2IAMFm_A=',
            'requestTime': '07/Aug/2022:11:18:46 +0000',
            'path': '/prod/api/aws/organizations',
            'accountId': '556604053180',
            'protocol': 'HTTP/1.1',
            'stage': 'prod',
            'domainPrefix': 'usroinvppa',
            'requestTimeEpoch': 1659871126028,
            'requestId': '7a981da2-6816-4556-adcf-67ba836cfd9b',
            'identity': {
                'cognitoIdentityPoolId':
                    None,
                'accountId':
                    '556604053180',
                'cognitoIdentityId':
                    None,
                'caller':
                    'caller:Afik.Grinstein@cyberark.com',
                'sourceIp':
                    '194.90.225.101',
                'principalOrgId':
                    'o-5o5ko47d2j',
                'accessKey':
                    'ASIAS27DWCGNTRCTACVH',
                'cognitoAuthenticationType':
                    None,
                'cognitoAuthenticationProvider':
                    None,
                'userArn':
                    'arn:aws:sts::556604053180:assumed-role/AWSReservedSSO_EverestDeveloperDev_79a1b399e9f35ee3/Afik.Grinstein@cyberark.com',
                'userAgent':
                    'python-requests/2.28.1',
                'user':
                    'user:Afik.Grinstein@cyberark.com'
            },
            'domainName': 'usroinvppa.execute-api.us-east-1.amazonaws.com',
            'apiId': 'usroinvppa'
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

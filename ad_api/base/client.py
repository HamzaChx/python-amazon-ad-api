import json
import logging
from cachetools import TTLCache
from requests import request
from ad_api.auth.credentials import Credentials
from ad_api.auth import AccessTokenClient, AccessTokenResponse
from .api_response import ApiResponse
from .base_client import BaseClient
from .exceptions import get_exception_for_content
from .marketplaces import Marketplaces
import os
import requests
from io import BytesIO
import gzip
from zipfile import ZipFile
import zipfile
from urllib.parse import urlparse, quote

log = logging.getLogger(__name__)
role_cache = TTLCache(maxsize=int(os.environ.get('AD_API_AUTH_CACHE_SIZE', 10)), ttl=3200)


class Client(BaseClient):
    access_token_client_class = AccessTokenClient
    credentials_class = Credentials
    grantless_scope = ''

    def __init__(
            self,
            account='default',
            marketplace: Marketplaces = Marketplaces[os.environ[
                'AD_API_DEFAULT_MARKETPLACE']] if 'AD_API_DEFAULT_MARKETPLACE' in os.environ else Marketplaces.EU,
            credentials=None,
            proxies=None,
            verify=True,
            timeout=None,
            debug=False
    ):

        super().__init__(account, credentials)
        self.endpoint = marketplace.endpoint
        self.debug = debug
        self._auth = self.access_token_client_class(
            account=account,
            credentials=credentials,
            credentials_class=self.credentials_class,
            proxies=proxies,
            verify=verify,
            timeout=timeout,
        )
        self.timeout = timeout
        self.proxies = proxies
        self.verify = verify

    @property
    def headers(self):
        return {
            'User-Agent': self.user_agent,
            'Amazon-Advertising-API-ClientId': self.credentials.client_id,
            'Authorization': 'Bearer %s' % self.auth.access_token,
            'Amazon-Advertising-API-Scope': self.credentials.profile_id,
            'Content-Type': 'application/json'
        }

    @property
    def auth(self) -> AccessTokenResponse:
        return self._auth.get_auth()

    @staticmethod
    def _download(self, params: dict = None, headers=None) -> ApiResponse:

        location = params.get("url")

        try:
            r = requests.get(
                location,
                headers=headers or self.headers,
                data=None,
                allow_redirects=True,
                timeout=self.timeout,
                proxies=self.proxies,
                verify=self.verify,
            )

        except requests.exceptions.InvalidSchema as e:
            error = {
                'success': False,
                'code': 400,
                'response': e
            }
            next_token = None
            return ApiResponse(error, next_token, headers=self.headers)
        except requests.exceptions.ConnectionError as e:
            error = {
                'success': False,
                'code': e.status_code,
                'response': e
            }
            next_token = None
            return ApiResponse(error, next_token, headers=self.headers)
        except requests.exceptions.RequestException as e:
            error = {
                'success': False,
                'code': 503,
                'response': e
            }
            next_token = None
            return ApiResponse(error, next_token, headers=self.headers)

        bytes = r.content
        mode = params.get("format")

        if mode is None:
            mode = "url"

        name = params.get("file")

        if name is None:
            o = urlparse(r.url)
            file_name = o.path[1:o.path.find('.')]
            name = file_name.replace("/", "-")

        if mode == "raw":

            next_token = None
            return ApiResponse(bytes, next_token, headers=r.headers)

        elif mode == "url":

            next_token = None
            return ApiResponse(r.url, next_token, headers=r.headers)

        elif mode == "data":

            if bytes[0:2] == b'\x1f\x8b':
                logging.info("Is gzip report")
                buf = BytesIO(bytes)
                f = gzip.GzipFile(fileobj=buf)
                read_data = f.read()
                next_token = None
                return ApiResponse(json.loads(read_data.decode('utf-8')), next_token, headers=r.headers)

            else:
                logging.info("Is bytes snapshot")
                next_token = None
                return ApiResponse(json.loads(r.text), next_token, headers=r.headers)

        elif mode == "json":
            if bytes[0:2] == b'\x1f\x8b':
                buf = BytesIO(bytes)
                f = gzip.GzipFile(fileobj=buf)
                read_data = f.read()
                fo = open(name + ".json", 'w')
                fo.write(read_data.decode('utf-8'))
                fo.close()
                next_token = None
                return ApiResponse(name + ".json", next_token, headers=r.headers)
            else:
                fo = open(name + ".json", 'w')
                fo.write(r.text)
                fo.close()
                next_token = None
                return ApiResponse(name + ".json", next_token, headers=r.headers)

        elif mode == "csv":
            if bytes[0:2] == b'\x1f\x8b':
                buf = BytesIO(bytes)
                f = gzip.GzipFile(fileobj=buf)
                read_data = f.read()
                fo = open(name + ".csv", 'w')
                fo.write(read_data.decode('utf-8'))
                fo.close()
                next_token = None
                return ApiResponse(name + ".csv", next_token, headers=r.headers)
            else:
                fo = open(name + ".csv", 'w')
                fo.write(r.text)
                fo.close()
                next_token = None
                return ApiResponse(name + ".csv", next_token, headers=r.headers)

        elif mode == "gzip":
            fo = gzip.open(name + ".json.gz", 'wb').write(r.content)
            next_token = None
            return ApiResponse(name + ".json.gz", next_token, headers=r.headers)

        elif mode == "zip":

            if bytes[0:2] == b'\x1f\x8b':
                buf = BytesIO(bytes)
                f = gzip.GzipFile(fileobj=buf)
                read_data = f.read()
                fo = open(name + ".json", 'w')
                fo.write(read_data.decode('utf-8'))
                fo.close()

                zipObj = ZipFile(name + '.zip', 'w', zipfile.ZIP_DEFLATED)
                zipObj.write(name + ".json")
                zipObj.close()
            else:
                fo = open(name + ".json", 'w')
                fo.write(r.text)
                fo.close()

                zipObj = ZipFile(name + '.zip', 'w', zipfile.ZIP_DEFLATED)
                zipObj.write(name + ".json")
                zipObj.close()

            if os.path.exists(name + ".json"):
                os.remove(name + ".json")

            next_token = None
            return ApiResponse(name + ".zip", next_token, headers=r.headers)

        else:

            error = {
                'success': False,
                'code': 400,
                'response': 'The mode "%s" is not supported perhaps you could use "data", "raw", "url", "json", "zip" or "gzip"' % (
                    mode)
            }
            next_token = None
            return ApiResponse(error, next_token, headers=self.headers)

        raise NotImplementedError("Unknown mode")

    def _request(self,
                 path: str,
                 data: str = None,
                 params: dict = None,
                 headers = None,
                 ) -> ApiResponse:

        if params is None:
            params = {}

        method = params.pop('method')

        if headers is False:
            base_header = self.headers.copy()
            base_header.pop("Content-Type")
            headers = base_header

        elif headers is not None:

            base_header = self.headers.copy()
            base_header.update(headers)
            headers = base_header

        request_data = data if method in ('POST', 'PUT', 'PATCH') else None
        res = request(
            method,
            self.endpoint + path,
            params=params,
            data=request_data,
            headers=headers or self.headers,
            timeout=self.timeout,
            proxies=self.proxies,
            verify=self.verify,
        )

        if self.debug:
            logging.info(headers or self.headers)

            if params:
                str_query = ""
                for key, value in params.items():
                    str_query += key + "=" + quote(str(value))
                message = method + " " + self.endpoint + path + "?" + str_query
            else:
                message = method + " " + self.endpoint + path

            logging.info(message)
            if data is not None:
                logging.info(data)

        return self._check_response(res)

    # @staticmethod
    def _check_response(self, res) -> ApiResponse:

        if self.debug:
            logging.info(vars(res))

        content = vars(res).get('_content')
        str_content = content.decode('utf8')

        if type(str_content) is str and str_content[0:50] == '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">' and vars(res).get('_content_consumed') is True:

            dictionary = {"status_code": vars(res).get('status_code'), "msg": "Unauthorized"}
            exception = get_exception_for_content(dictionary)
            raise exception(dictionary)

        if type(str_content) is str and str_content[0:15] == 'Invalid request' and vars(res).get('_content_consumed') is True:
            dictionary = {"status_code": vars(res).get('status_code'), "msg": str_content}
            exception = get_exception_for_content(dictionary)
            raise exception(dictionary)

        data = json.loads(str_content)

        if type(data) is dict and data.get('code') == 'UNAUTHORIZED':
            exception = get_exception_for_content(data)
            raise exception(data)

        if type(data) is dict and data.get('message') == 'Too Many Requests' and vars(res).get('_content_consumed') is True:
            exception = get_exception_for_content(data)
            raise exception(data)

        if type(data) is dict and data.get('code') == 'NOT_FOUND' and vars(res).get('_content_consumed') is True:
            dictionary = {"status_code": vars(res).get('status_code'), "code": data.get('code'), "details": data.get('details'), "requestId": data.get('requestId')}
            exception = get_exception_for_content(data)
            raise exception(dictionary)

        if type(data) is dict and data.get('code') == 'SERVER_IS_BUSY' and vars(res).get('_content_consumed') is True:
            dictionary = {"status_code": vars(res).get('status_code'), "code": data.get('code'), "details": data.get('details'), "requestId": data.get('requestId')}
            exception = get_exception_for_content(data)
            raise exception(dictionary)

        if type(data) is dict and data.get('message') == 'Unauthorized' and vars(res).get('_content_consumed') is True:
            dictionary = {"status_code": vars(res).get('status_code'), "message": "Unauthorized"}
            exception = get_exception_for_content(dictionary)
            raise exception(dictionary)

        if type(data) is dict and data.get('details') == 'Invalid authorization inputs' and vars(res).get('_content_consumed') is True:
            dictionary = {"status_code": vars(res).get('status_code'), "message": "Invalid authorization inputs"}
            exception = get_exception_for_content(dictionary)
            raise exception(dictionary)

        if type(data) is dict and data.get('message') == 'Missing Authentication Token' and vars(res).get('_content_consumed') is True:
            dictionary = {"status_code": vars(res).get('status_code'), "message": "Missing Authentication Token"}
            exception = get_exception_for_content(dictionary)
            raise exception(dictionary)

        if type(data) is dict and data.get('details') == 'Cannot consume content type' and vars(res).get('_content_consumed') is True:
            dictionary = {"status_code": vars(res).get('status_code'), "message": data.get('details')}
            exception = get_exception_for_content(dictionary)
            raise exception(dictionary)

        headers = vars(res).get('headers')
        status_code = vars(res).get('status_code')
        next_token = vars(res).get('_next')
        return ApiResponse(data, next_token, headers=headers)

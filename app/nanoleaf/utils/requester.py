import os

import requests

from app.nanoleaf import exceptions


class Requester:

    def __init__(self, ip_address: str = None, auth_token: str = None):
        if ip_address is None:
            ip_address = os.getenv("NANOLEAF_IP")

        if auth_token is None:
            auth_token = os.getenv("NANOLEAF_AUTH_TOKEN")

        self.base_url = f"http://{ip_address}:16021/api/v1/{auth_token}/"
        self.__ip_address = ip_address
        self.auth_token = auth_token

    @property
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, value):
        self.__ip_address = value

    def request(self, method: str, endpoint: str = "", data: dict = None):
        url = self.base_url + endpoint
        try:
            r = requests.request(method=method, url=url, json=data)
        except requests.exceptions.RequestException as e:
            print(e)
            return
        output = None if r.text == "" else r.json()
        self.__check(status=r.status_code, output=output)
        return output

    def __check(self, status, output):
        if status >= 400:
            raise self.__create_exception(status, output)
        return output

    def __create_exception(self, status, output):
        if status == 403:
            cls = exceptions.BadRequestException
        elif status == 401:
            cls = exceptions.InvalidCredentialsException
        elif status == 404:
            cls = exceptions.ResourceNotFoundException
        elif status == 422:
            cls = exceptions.UnprocessableEntityException
        elif status == 500:
            cls = exceptions.InternalServerError

        return cls(status, output)

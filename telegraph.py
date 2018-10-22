import requests
import json
from exceptions import exceptions_raise
from types import Account, Page, PageList, PageViews, NodeElement, Node
import os
import datetime
from uuid import uuid4
from io import BytesIO
import mimetypes
import re


def raw_fields_generator(args):
    return json.dumps(args)


def field_generator(**args):
    datargs = ''
    for length, item in enumerate(args.items(), 1):
        if item[1]:
            if length == len(args):
                datargs += '"{}"'.format(item[0])
            else:
                datargs += '"{}",'.format(item[0])
    return str('[{}]'.format(datargs))


class Telegraph:
    def __init__(self, session, token=''):
        self.session = session
        self.base_url = 'https://api.telegra.ph/'
        self.token = token

    @property
    def auth_url(self):
        r = self.get_account_info(auth_url=True)
        r['valid_to'] = datetime.datetime.now() + datetime.timedelta(minutes=5)
        return r

    def save_data(self, token, session_name):
        if not session_name:
            return
        with open("{}.token".format(session_name), 'w', encoding='utf-8') as tk:
            tk.write(token)

    def get_data(self, session_name):
        if not session_name:
            return self.token
        if os.path.isfile('{}.token'.format(session_name)):
            with open("{}.token".format(session_name), 'r', encoding='utf-8') as tk:
                return tk.read()
        else:
            self.save_data(self.token, self.session)
            return self.token

    def request(self, method, post_fields):
        for i, x in post_fields.copy().items():
            if x is None:
                del post_fields[i]
        j = requests.post(self.base_url + method, post_fields).json()
        if not j['ok']:
            raise exceptions_raise[j['error']]
        return j["result"]

    def start(self, short_name=None, author_name=None, author_url=None):
        if self.session:
            self.token = self.get_data(self.session)
            if not self.token:
                if short_name or author_name or author_url:
                    j = self.create_account(short_name, author_name, author_url)
                    self.token = j['access_token']
                    self.save_data(self.token, self.session)
                else:
                    j = self.create_account(input('short_name: '), input('author_name: '), input('author_url: '))
                    self.token = j['access_token']
                    self.save_data(self.token, self.session)

        else:
            if short_name or author_name or author_url:
                j = self.create_account(short_name, author_name, author_url)
                self.token = j['access_token']
            else:
                j = self.create_account(input('short_name: '), input('author_name: '), input('author_url: '))
                self.token = j['access_token']

    def create_account(self, short_name, author_name=None, author_url=None):
        params = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        return Account(**self.request('createAccount', params))

    def edit_account_info(self, short_name=None, author_name=None, author_url=None):
        access_token = self.token
        params = {
            'access_token': access_token,
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        return Account(**self.request('editAccountInfo', params))

    def get_account_info_raw(self, fields=()):
        access_token = self.token
        params = {
            'access_token': access_token,
            'fields': raw_fields_generator(fields),
        }
        return Account(**self.request('getAccountInfo', params))

    def get_account_info(self, short_name=False, author_name=False, author_url=False, auth_url=False, page_count=False,
                         access_token=''):
        if not access_token:
            access_token = self.token
        fields = field_generator(**locals())
        params = {
            'access_token': access_token,
            'fields': fields,
        }
        return Account(**self.request('getAccountInfo', params))

    def revoke_access_token(self):
        access_token = self.token
        params = {
            'access_token': access_token,
        }
        j = self.request('revokeAccessToken', params)
        self.token = j['access_token']
        if self.session:
            self.save_data(self.token, self.session)
        return j

    def create_page(self, title, content, author_name='', author_url='', return_content=False):
        access_token = self.token
        userdata = self.get_account_info_raw(['author_name', 'author_url'])
        if not author_name:
            author_name = userdata.author_name
        if not author_url:
            author_url = userdata.author_url

        params = {
            'access_token': access_token,
            'title': title,
            'author_name': author_name,
            'author_url': author_url,
            'content': str(content),
            'return_content': return_content,

        }
        return Page(**self.request('createPage', params))

    def edit_page(self, path, title=None, author_name=None, author_url=None, content=None, return_content=False,
                  access_token=''):
        if not access_token:
            access_token = self.token
        params = {
            'access_token': access_token,
            'path': path,
            'title': title,
            'content': content,
            'author_name': author_name,
            'author_url': author_url,
            'return_content': return_content,

        }
        return Page(**self.request('editPage', params))

    def get_page(self, path, return_content=False):
        params = {
            'path': re.sub('(http[s]?://)?telegra.ph/', '', path, flags=re.I),
            'return_content': return_content,

        }
        return Page(**self.request('getPage', params))

    def get_page_list(self, offset=0, limit=50):
        access_token = self.token
        params = {
            'access_token': access_token,
            'offset': offset,
            'limit': limit,

        }
        return PageList(**self.request('getPageList', params))

    def get_views(self, path, year=None, month=None, day=None, hour=None):
        params = {
            'path': path,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour

        }
        return PageViews(**self.request('getViews', params))

    @staticmethod
    def upload_image(image):
        if isinstance(image, str):
            with open(image, 'rb') as image_data:
                files = {'file': (f'{uuid4()}', image_data.read(), mimetypes.guess_type(image)[0])}

        elif isinstance(image, BytesIO):
            files = {'file': (f'{uuid4()}', image.read(), "image/png")}
        else:
            raise ValueError("Invalid image type")
        r = requests.post('https://telegra.ph/upload/', files=files)
        if not type(r.json()) is not list:
            return r.json()[0]['src']
        else:
            raise exceptions_raise[r.json()['error']]

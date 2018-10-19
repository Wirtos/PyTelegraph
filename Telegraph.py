from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
from Exceptions import exceptions_raise
import os
import datetime


def raw_fields_generator(args):
    datargs = ''
    for length, i in enumerate(args, 1):

        if length == len(args):
            datargs += '\"{}\"'.format(i)
        else:
            datargs += '\"{}\",'.format(i)
    return str('[{}]'.format(datargs))


def field_generator(**args):
    datargs = ''
    for length, i in enumerate(args.items(), 1):
        if i[1]:
            if length == len(args):
                datargs += '\"{}\"'.format(i[0])
            else:
                datargs += '\"{}\",'.format(i[0])
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
        final_request = Request(self.base_url + method, urlencode(post_fields).encode())
        j = urlopen(final_request).read()
        j = json.loads(j)
        if not j['ok']:
            raise exceptions_raise[j['error']]
        print(j['result'])
        return j['result']

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
        return self.request('createAccount', params)

    def edit_account_info(self, short_name='', author_name='', author_url='', access_token=''):
        if not access_token:
            access_token = self.token
        params = {
            'access_token': access_token,
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        return self.request('editAccountInfo', params)

    def get_account_info_raw(self, fields=(), access_token=''):
        if not access_token:
            access_token = self.token
        params = {
            'access_token': access_token,
            'fields': raw_fields_generator(fields),
        }
        return self.request('getAccountInfo', params)

    def get_account_info(self, short_name=False, author_name=False, author_url=False, auth_url=False, page_count=False,
                         access_token=''):
        if not access_token:
            access_token = self.token
        fields = field_generator(**locals())
        params = {
            'access_token': access_token,
            'fields': fields,
        }
        return self.request('getAccountInfo', params)

    def revoke_access_token(self, access_token=''):
        if not access_token:
            access_token = self.token
        params = {
            'access_token': access_token,
        }
        j = self.request('revokeAccessToken', params)
        self.token = j['access_token']
        if self.session:
            self.save_data(self.token, self.session)
        return j

    def create_page(self, title='', author_name='', author_url='', content='', return_content=False, access_token=''):
        # TODO: NODE PAGE CREATOR
        if not access_token:
            access_token = self.token
        params = {
            'access_token': access_token,
            'title': title,
            'author_name': author_name,
            'author_url': author_url,
            'content': content,
            'return_content': return_content,

        }
        return self.request('createPage', params)

    def edit_page(self, path='', title=None, author_name=None, author_url=None, content=None, return_content=False,
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
        return self.request('editPage', params)

    def get_page(self, path='', return_content=False):
        params = {
            'path': path,
            'return_content': return_content,

        }
        return self.request('getPage', params)

    def get_page_list(self, offset=0, limit=50, access_token=''):
        if not access_token:
            access_token = self.token
        params = {
            'access_token': access_token,
            'offset': offset,
            'limit': limit,

        }
        return self.request('getPageList', params)

    def get_views(self, path, year=None, month=None, day=None, hour=None):
        params = {
            'path': path,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour

        }
        return self.request('getViews', params)



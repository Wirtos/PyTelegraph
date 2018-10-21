from Base import Obj


class Account(Obj):
    __available_kwargs = ('short_name', 'author_name', 'author_url', 'access_token', 'auth_url', 'page_count')

    def __init__(self, **kwargs):
        for i in kwargs:
            if i not in self.__available_kwargs:
                raise ValueError('Invalid Account Object')
        super(Account, self).__init__(**kwargs)


class Page(Obj):
    __available_kwargs = (
    'path', 'url', 'title', 'description', 'author_name', 'author_url', 'image_url', 'content', 'views', 'can_edit')

    def __init__(self, **kwargs):
        for i in kwargs:
            if i not in self.__available_kwargs:
                raise ValueError('Invalid Page Object')
        super(Page, self).__init__(**kwargs)


class PageList(Obj):
    __available_kwargs = ('total_count', 'pages')

    def __init__(self, **kwargs):
        for i in kwargs:
            if i not in self.__available_kwargs:
                raise ValueError('Invalid PageList Object')
        super(PageList, self).__init__(**kwargs)
        self.__dict__['pages'] = [Page(**pg) for pg in kwargs['pages']]


class PageViews:
    __available_kwargs = ('path', 'year', 'month', 'day', 'hour')

    def __init__(self, **kwargs):
        for i in kwargs:
            if i not in self.__available_kwargs:
                raise ValueError('Invalid PageViews Object')
        super(PageViews, self).__init__(**kwargs)


class Node:
    __available_tags = ('a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure', 'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p', 'pre', 's', 'strong', 'u', 'ul', 'video')

    def __init__(self, string, tag):
        if tag not in self.__available_tags:
            raise ValueError('Invalid tag')
        self.tag = tag
        self.string = string

    def __str__(self):
        return self.generator()

    def generator(self):
        return f'<{self.tag}>{self.string}</{self.tag}>'


class NodeElement:
    pass

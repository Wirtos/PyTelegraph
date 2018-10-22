class Lst(list):
    """
    Like `Obj` but for lists.
    """
    def __init__(self, iterable=()):
        list.__init__(self, (Obj(**x) if isinstance(x, dict) else (
            Lst(x) if isinstance(x, list) else x) for x in iterable))

    def __getattr__(self, name):
        name = name.rstrip('_')
        obj = self.__dict__.get(name)
        if obj is None:
            obj = Obj()
            self.__dict__[name] = obj
        return obj

    def __repr__(self):
        return super().__repr__() + repr(self.to_dict())

    def to_dict(self):
        return [v.to_dict() if isinstance(v, (Obj, Lst)) else v
for v in self]

class Obj:
    """
    Class to avoid dictionary-like access and ``None`` values.
    For instance:
        >>> lonami = Obj(name='lonami', hobby='developer')
        >>> print(lonami.name, 'is', lonami.age or 20)
        >>>
        >>> lonami.friend.name = 'kate'
        >>> print(lonami.friend)
        >>>
    If you expect a different type you should use ``or value``, as
    empty `Obj` instances are considered to be ``False``.
    You can convert `Obj` instances back to ``dict`` with `.to_dict()`.
    If a member name is a reserved keyword, like ``from``, add a trailing
    underscore, like ``from_``.
    """
    def __init__(self, **kwargs):
        self.__dict__ = {k: Obj(**v) if isinstance(v, dict) else (
            Lst(v) if isinstance(v, list) else v) for k, v in kwargs.items()}

    def __getattr__(self, name):
        name = name.rstrip('_')
        obj = self.__dict__.get(name)
        if obj is None:
            obj = Obj()
            self.__dict__[name] = obj
        return obj

    def __getitem__(self, name):
        obj = self.__dict__.get(name)
        if obj is None:
            obj = Obj()
            self.__dict__[name] = obj
        return obj

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __iter__(self):
        return iter(())

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return repr(self.to_dict())

    def __bool__(self):
        return bool(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def __call__(self, *a, **kw):
        return Obj()

    def to_dict(self):
        return {k: v.to_dict() if isinstance(v, (Obj, Lst)) else v
                for k, v in self.__dict__.items()}

    @staticmethod
    def pretty_format(obj, indent=None):
        """
        Pretty formats the given object as a string which is returned.
        If indent is None, a single line will be returned.
        """
        if indent is None:
            if isinstance(obj, Obj):
                obj = obj.to_dict()

            if isinstance(obj, dict):
                return '{}({})'.format(obj.get('_', 'dict'), ', '.join(
                    '{}={}'.format(k, Obj.pretty_format(v))
                    for k, v in obj.items() if k != '_'
                ))
            elif isinstance(obj, str) or isinstance(obj, bytes):
                return repr(obj)
            elif hasattr(obj, '__iter__'):
                return '[{}]'.format(
                    ', '.join(Obj.pretty_format(x) for x in obj)
                )
            else:
                return repr(obj)
        else:
            result = []
            if isinstance(obj, Obj):
                obj = obj.to_dict()

            if isinstance(obj, dict):
                result.append(obj.get('_', 'dict'))
                result.append('(')
                if obj:
                    result.append('\n')
                    indent += 1
                    for k, v in obj.items():
                        if k == '_':
                            continue
                        result.append('\t' * indent)
                        result.append(k)
                        result.append('=')
                        result.append(Obj.pretty_format(v, indent))
                        result.append(',\n')
                    result.pop()  # last ',\n'
                    indent -= 1
                    result.append('\n')
                    result.append('\t' * indent)
                result.append(')')

            elif isinstance(obj, str) or isinstance(obj, bytes):
                result.append(repr(obj))

            elif hasattr(obj, '__iter__'):
                result.append('[\n')
                indent += 1
                for x in obj:
                    result.append('\t' * indent)
                    result.append(Obj.pretty_format(x, indent))
                    result.append(',\n')
                indent -= 1
                result.append('\t' * indent)
                result.append(']')

            else:
                result.append(repr(obj))

            return ''.join(result)

    def stringify(self):
        return Obj.pretty_format(self, indent=0)

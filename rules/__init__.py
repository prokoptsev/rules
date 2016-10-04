# coding: utf-8
from __future__ import unicode_literals

from .helpers import _NOTSET, get_by_path
from .exceptions import ValidateError, NotSetError


class Rule(object):
    def __init__(self, source,
                 to_field=None, required=False, allowed_none=True):
        self._value = None if not required and allowed_none else _NOTSET

        self.source = source
        self.to_field = to_field
        self.required = required
        self.allowed_none = allowed_none

    def __get__(self, obj, objtype):
        return self._value

    def __set__(self, obj, value):
        if value is _NOTSET and self.required:
            raise ValidateError("{} is required".format(self.source))
        if value is None and not self.allowed_none:
            raise ValidateError("{} not allowed None".format(self.source))

        value = self.cast(value)
        self.validate(value)
        self._value = value

    def validate(self, value):
        pass

    def cast(self, value):
        return value

    def find_value(self, data):
        return get_by_path(self.source, data)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.source)


class MetaRules(type):
    def __new__(cls, name, bases, attrs):
        fields = {
            attr_name: attr
            for attr_name, attr in attrs.iteritems() if isinstance(attr, Rule)
        }
        attrs['_fields'] = fields
        return super(MetaRules, cls).__new__(cls, name, bases, attrs)


class Rules(object):
    __metaclass__ = MetaRules
    _fields = None

    def __init__(self, data):
        for field_name, field in self._fields.iteritems():
            setattr(self, field_name, field.find_value(data))

    def apply(self, silent=True):
        attrs = {}
        errors = {}

        for field_name, field in self._fields.iteritems():
            value = getattr(self, field_name)
            if value is _NOTSET:
                errors[field_name] = "Not set value"
                continue

            to_field = field.to_field or field_name
            attrs[to_field] = value

        if errors and not silent:
            msg = "; ".join(
                '{}: "{}"'.format(k, v) for k, v in errors.iteritems()
                )
            raise NotSetError(msg)
        return attrs

    def __repr__(self):
        return "<{cls}: {fields}>".format(
            cls=self.__class__.__name__,
            fields=' '.join(
                "{}={}".format(k, v) for k, v in self._fields.iteritems())
        )

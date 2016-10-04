# coding: utf-8
from __future__ import unicode_literals
import unittest
from rules import get_by_path, _NOTSET, Rule, ValidateError, Rules, NotSetError, MetaRules


class UtilsTestCase(unittest.TestCase):
    def test_find_by_path(self):
        d = {"deep": {"dict": True}}
        self.assertEqual(get_by_path("deep.dict", d), True)
        self.assertEqual(get_by_path("deep.not.found", d), _NOTSET)
        self.assertEqual(get_by_path("not.exist", d), _NOTSET)


class RuleTestCase(unittest.TestCase):
    def test_init_rule(self):
        class Test(object):
            # default
            f1 = Rule(
                "f1", to_field="__f1", required=False, allowed_none=True)

            f2 = Rule(
                "f2", to_field="__f2", required=False, allowed_none=False)
            f3 = Rule(
                "f3", to_field="__f3", required=True, allowed_none=False)
            f4 = Rule(
                "f4", to_field="__f4", required=True, allowed_none=True)

        t = Test()
        self.assertEqual(t.f1, None)
        self.assertEqual(t.f2, _NOTSET)
        self.assertEqual(t.f3, _NOTSET)
        self.assertEqual(t.f4, _NOTSET)

        self.assertRaises(ValidateError, setattr, t, "f3", _NOTSET)
        self.assertRaises(ValidateError, setattr, t, "f4", _NOTSET)

        self.assertRaises(ValidateError, setattr, t, "f2", None)
        self.assertRaises(ValidateError, setattr, t, "f3", None)

    def test_find_value(self):
        r = Rule("d.e.e.p")
        data = {"d": {"e": {"e": {"p": True}}}}
        self.assertEqual(r.find_value(data), True)
        self.assertEqual(r.find_value({"not": "set"}), _NOTSET)

    def test_representation(self):
        self.assertEqual(repr(Rule("ofLife")), b'<Rule: ofLife>')


class RulesTestCase(unittest.TestCase):
    def test_metaclass(self):
        rule = Rule("Field")

        class Test(object):
            __metaclass__ = MetaRules
            field = rule

        self.assertTrue(hasattr(Test, "_fields"))
        self.assertEqual(Test._fields, {'field': rule})
        self.assertEqual(Test()._fields, {'field': rule})

    def test_representation(self):
        class Test(Rules):
            field = Rule("Id")
        self.assertEqual(repr(Test({})), b"<Test: field=<Rule: Id>>")

    def test_apply(self):
        FakeRule = type(b"FakeRule", (object,), {"to_field": None})

        rules = Rules({})
        rules._fields = {}

        rules._fields["field"] = FakeRule()
        rules.field = "field__value"

        special_field = FakeRule()
        special_field.to_field = "__special_field"
        rules._fields["special_field"] = special_field
        rules.special_field = "special_field__value"

        self.assertDictEqual(
            rules.apply(),
            {
                "field": "field__value",
                "__special_field": "special_field__value",
            }
        )

    def test_apply_error(self):
        rules = Rules({})
        rules._fields = {}
        rules.f = rules._fields['f'] = _NOTSET
        self.assertRaises(NotSetError, rules.apply, silent=False)
        self.assertEqual(rules.apply(silent=True), {})

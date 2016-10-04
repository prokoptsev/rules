# coding: utf-8
from __future__ import unicode_literals
import unittest

from rules import Rule, ValidateError, Rules


class AcceptanceTestCase(unittest.TestCase):
    def test_required(self):
        class TestRules(Rules):
            id_field = Rule("Id", required=True)

        td = TestRules({"Id": 1})
        self.assertDictEqual(td.apply(), {"id_field": 1})

        with self.assertRaises(ValidateError) as cm:
            TestRules({})
        self.assertEqual(cm.exception.message, 'Id is required')

        class TestRules(Rules):
            id_field = Rule("Id", required=False)

        td = TestRules({"Id": 1})
        self.assertDictEqual(td.apply(), {"id_field": 1})

        td = TestRules({})
        self.assertDictEqual(td.apply(), {})

    def test_allowed_none(self):
        class TestRules(Rules):
            id_field = Rule("Id", allowed_none=True)

        td = TestRules({"Id": None})
        self.assertDictEqual(td.apply(), {"id_field": None})

        class TestRules(Rules):
            id_field = Rule("Id", allowed_none=False)

        with self.assertRaises(ValidateError) as cm:
            TestRules({"Id": None})
        self.assertEqual(cm.exception.message, 'Id not allowed None')

        td = TestRules({})
        self.assertDictEqual(td.apply(), {})

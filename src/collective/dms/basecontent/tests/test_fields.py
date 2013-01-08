# -*- coding: utf8 -*-

import unittest2 as unittest

from zope.schema.interfaces import RequiredMissing, InvalidValue

from ecreall.helpers.testing.base import BaseTest

from collective.dms.basecontent.testing import DMS_TESTS_PROFILE_FUNCTIONAL


class TestFields(unittest.TestCase, BaseTest):
    """Tests adapters"""

    layer = DMS_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        super(TestFields, self).setUp()
        self.portal = self.layer['portal']

    def _getTargetClass(self):
        from collective.dms.basecontent._field import LocalRolesToPrincipals
        return LocalRolesToPrincipals

    def _makeOne(self, *args, **kw):
        field = self._getTargetClass()(*args, **kw)
        # this is needed to initialize the vocabulary
        return field.bind(self.portal)

    def test_value_type_default_value(self):
        """By default, the field's value_type attribute contains a vocabulary
           listing every available groups of the Plone site."""
        field = self._makeOne()
        value_type_terms = [term.value for term in field.value_type.vocabulary._terms]
        # by default, the proposed vocabulary is the list of existing groups
        self.assertEquals(set(value_type_terms), set(self.portal.portal_groups.listGroupNames()))

    def test_roles_to_assign_attribute(self):
        field = self._makeOne()
        # the roles_to_assign attribute is required, if empty, validate fails
        self.assertEquals(field.roles_to_assign, ())
        self.assertRaises(RequiredMissing, field.validate, [])
        # if we want to assign role but one does not exist, validate fails too
        field = self._makeOne(roles_to_assign=('Editor', 'WrongRole',))
        self.assertRaises(InvalidValue, field.validate, [])
        # if we have valid values, it works like a charm ;-)
        field = self._makeOne(roles_to_assign=('Editor', 'Reader',))
        field.validate([])

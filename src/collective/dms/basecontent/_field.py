# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Schema Fields
"""
__docformat__ = 'restructuredtext'


from zope.component import adapts
from zope.interface import implementer
from zope.interface import Interface

from zope.schema.interfaces import IList
from zope.schema import List, Choice, Tuple

from z3c.form.datamanager import AttributeField

import logging
logger = logging.getLogger('collective.dms.basecontent._field')

class ILocalRolesToPrincipals(IList):
    """Field that list principals depending on a vocabulary and that assign given
       local roles."""

    # this attribute will contains a tuple of principal to assign when the value is set
    roles_to_assign = Tuple(
          title=u"Roles to assign",
          description=u"""\
          Define roles that will be automatically asigned as local roles.
          """,
          required=True)


@implementer(ILocalRolesToPrincipals)
class LocalRolesToPrincipals(List):
    """Field that list principals depending on a vocabulary and that assign given
       local roles."""

    def __init__(self, roles_to_assign=(), value_type=Choice(vocabulary=u'plone.app.vocabularies.Groups',), **kw):
        self.roles_to_assign = roles_to_assign
        kw['value_type'] = value_type
        super(LocalRolesToPrincipals, self).__init__(**kw) 


class LocalRolesToPrincipalsDataManager(AttributeField):
    """A data manager which set local roles when saving the field."""
    adapts(Interface, ILocalRolesToPrincipals)

    def set(self, value):
        """See z3c.form.interfaces.IDataManager"""
        # set local roles before setting the value so we still have access to the old value
        roles_to_assign = self.field.roles_to_assign
        # ---1 --- first find assigned roles to remove
        # it is not that easy to remove local roles because no helper method exists
        # for removing some specific local roles, only a method for removing every local roles...
        old_value = self.field.get(self.context)
        # now check between old_value and value (new value) what is missing
        removed_principals = set(old_value).difference(set(value))
        # remove local_roles for removed_principals
        for local_role in self.context.get_local_roles():
            # a local_role is like ('Administrators', (u'Contributor', u'Reviewer'))
            principal = local_role[0]
            if principal in removed_principals:
                cleaned_local_roles = list(local_role[1])
                for role_to_assign in roles_to_assign:
                    try:
                        cleaned_local_roles.remove(role_to_assign)
                    except ValueError:
                        # if a role to remove was already removed (???) pass
                        logger.warn("Failed to remove role '%s' for principal '%s' on object '%s'" \
                                    % (role_to_assign, principal, '/'.join(self.context.getPhysicalPath())))
                # if there are still some local_roles, use manage_setLocalRoles
                if cleaned_local_roles:
                    self.context.manage_setLocalRoles(principal, cleaned_local_roles)
                else:
                    # either use manage_delLocalRoles
                    self.context.manage_delLocalRoles((principal,))
        # ---2 --- now add new local roles
        added_principals = set(value).difference(set(old_value))
        for added_principal in added_principals:
            self.context.manage_addLocalRoles(added_principal, roles_to_assign)
        # finally set the value
        super(LocalRolesToPrincipalsDataManager, self).set(value)


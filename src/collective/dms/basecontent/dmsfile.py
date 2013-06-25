from zope.interface import implements

from plone.dexterity.content import Item
from plone.dexterity.schema import DexteritySchemaPolicy

from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model

from . import _


class IDmsFile(model.Schema):
    """Schema for DmsFile"""
    model.primary('file')
    file = NamedBlobFile(
        title=_("File"),
        required=True,
    )

class DmsFile(Item):
    """DmsFile"""
    implements(IDmsFile)
    __ac_local_roles_block__ = True

class DmsFileSchemaPolicy(DexteritySchemaPolicy):
    """Schema Policy for DmsFile"""

    def bases(self, schemaName, tree):
        return (IDmsFile, )

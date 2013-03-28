from zope.interface import implements

from plone.dexterity.content import Item
from plone.dexterity.schema import DexteritySchemaPolicy

from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model

from . import _


class IDmsFile(model.Schema):
    """ """
    model.primary('file')
    file = NamedBlobFile(
        title=_("File"),
        required=True,
    )

class DmsFile(Item):
    """ """
    implements(IDmsFile)

class DmsFileSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsFile, )

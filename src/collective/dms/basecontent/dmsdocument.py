from zope import schema
from zope.component import adapts
from zope.interface import implements

from plone.app.content.interfaces import INameFromTitle

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from plone.supermodel import model

from . import _


class IDmsDocument(model.Schema):
    """ """

    notes = schema.Text(
        title=_(u"Notes"),
        required=False
        )

class DmsDocument(Container):
    """ """
    implements(IDmsDocument)


class DmsDocumentSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsDocument, )

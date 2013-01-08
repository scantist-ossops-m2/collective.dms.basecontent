from zope import schema
from zope.interface import implements

#from plone.app.content.interfaces import INameFromTitle

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from plone.supermodel import model

from collective.dms.basecontent.relateddocs import RelatedDocs

from . import _


class IDmsDocument(model.Schema):
    """ """

    notes = schema.Text(
        title=_(u"Notes"),
        required=False
        )

    related_docs = RelatedDocs(
        title=_(u"Related documents"),
        required=False,
        display_backrefs=True)

class DmsDocument(Container):
    """ """
    implements(IDmsDocument)

class DmsDocumentSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsDocument, )

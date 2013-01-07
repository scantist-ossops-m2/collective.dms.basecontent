from zope import schema
from zope.component import adapts
from zope.interface import implements

from plone.app.content.interfaces import INameFromTitle

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from plone.namedfile.field import NamedImage
from plone.supermodel import model

from . import _


class IBaseContent(model.Schema):
    """ """

    notes = schema.TextLine(
        title=_(u"Notes"),
        required=False
        )

class BaseContent(Container):
    """ """
    implements(IBaseContent)


class BaseContentSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IBaseContent, )

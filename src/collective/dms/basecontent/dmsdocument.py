from zope import schema
from zope.interface import implements

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from plone.supermodel import model

from collective.dms.basecontent.relateddocs import RelatedDocs

from . import _
from ._field import LocalRolesToPrincipals


class IDmsDocument(model.Schema):
    """ """

    notes = schema.Text(
        title=_(u"Notes"),
        required=False,
        )

    treating_groups = LocalRolesToPrincipals(
        title=_(u"Treating groups"),
        required=False,
        roles_to_assign=('Editor',),
        )

    recipient_groups = LocalRolesToPrincipals(
        title=_(u"Recipient groups"),
        required=False,
        roles_to_assign=('Reader',)
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

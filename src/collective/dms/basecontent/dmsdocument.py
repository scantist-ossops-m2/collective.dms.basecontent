from zope import schema
from zope.interface import implements
from zope.component import queryUtility
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from plone.supermodel import model
from five import grok
from collective.dms.basecontent.relateddocs import RelatedDocs

from . import _
from collective.z3cform.rolefield.field import LocalRolesToPrincipals

from zope.schema.interfaces import IVocabularyFactory


class IDmsDocument(model.Schema):
    """Schema for DmsDocument"""

    notes = schema.Text(
        title=_(u"Notes"),
        required=False,
    )

    treating_groups = LocalRolesToPrincipals(
        title=_(u"Treating groups"),
        required=False,
        roles_to_assign=('Editor',),
        value_type=schema.Choice(vocabulary=u'collective.dms.basecontent.treating_groups',)
    )

    recipient_groups = LocalRolesToPrincipals(
        title=_(u"Recipient groups"),
        required=False,
        roles_to_assign=('Reader',),
        value_type=schema.Choice(vocabulary=u'collective.dms.basecontent.recipient_groups')
    )

    related_docs = RelatedDocs(
        title=_(u"Related documents"),
        required=False,
        display_backrefs=True,
    )


class DmsDocument(Container):
    """DmsDocument"""
    implements(IDmsDocument)
    # disable local roles inheritance
    __ac_local_roles_block__ = True


class DmsDocumentSchemaPolicy(DexteritySchemaPolicy):
    """DmsDocument schema policy"""

    def bases(self, schemaName, tree):
        return (IDmsDocument, )


class TreatingGroupsVocabulary(grok.GlobalUtility):
    """Vocabulary for treating groups"""
    grok.name('collective.dms.basecontent.treating_groups')
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        principals = queryUtility(IVocabularyFactory, name=u'plone.principalsource.Principals')
        return principals(context)


class RecipientGroupsVocabulary(grok.GlobalUtility):
    """Vocabulary for recipient groups"""
    grok.name('collective.dms.basecontent.recipient_groups')
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        principals = queryUtility(IVocabularyFactory, name=u'plone.principalsource.Principals')
        return principals(context)

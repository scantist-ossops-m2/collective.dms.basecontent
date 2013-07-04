from BTrees.Length import Length

from five import grok

from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements

from plone import api
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.directives.form import default_value
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from plone.app.contenttypes.interfaces import IFile

from . import _
from zope.lifecycleevent.interfaces import IObjectAddedEvent


class IDmsFile(model.Schema, IFile):
    """Schema for DmsFile"""
    title = schema.TextLine(
        title=_(u'Version number'),
        required=False
    )
    form.mode(title='hidden')

    model.primary('file')
    file = NamedBlobFile(
        title=_(u"File"),
        required=True,
    )

class DmsFile(Item):
    """DmsFile"""
    implements(IDmsFile)
    __ac_local_roles_block__ = True
    signed = False

    def Title(self):
        if self.signed:
            return _(u"Signed version")
        else:
            return self.title


class DmsFileSchemaPolicy(DexteritySchemaPolicy):
    """Schema Policy for DmsFile"""

    def bases(self, schemaName, tree):
        return (IDmsFile, )


@default_value(field=IDmsFile['title'])
def titleDefaultValue(data):
    catalog = api.portal.get_tool('portal_catalog')
    container = data.context
    annotations = IAnnotations(container)
    if 'higher_version' not in annotations:
        version_number = 1
    else:
        version_number = annotations['higher_version'].value
    return unicode(version_number)


@grok.subscribe(IDmsFile, IObjectAddedEvent)
def update_higher_version(context, event):
    container = context.getParentNode()
    annotations = IAnnotations(container)
    if 'higher_version' not in annotations:
        annotations['higher_version'] = Length()
    annotations['higher_version'].change(1)

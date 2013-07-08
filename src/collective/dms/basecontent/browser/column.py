from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from five import grok
from z3c.table import interfaces
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate
import z3c.table.table
import z3c.table.column
from Products.CMFCore.WorkflowCore import WorkflowException

from collective.dms.basecontent import _

PMF = MessageFactory('plone')

grok.templatedir('templates')


class Column(z3c.table.column.Column, grok.MultiAdapter):
    grok.baseclass()
    grok.provides(interfaces.IColumn)


class DateColumn(Column):
    grok.baseclass()
    attribute = NotImplemented

    def renderCell(self, value):
        obj = value.getObject()
        date = getattr(obj, self.attribute, None)
        return self.table.format_date(date)


class PrincipalColumn(Column):
    grok.baseclass()
    attribute = NotImplemented

    def renderCell(self, item):
        try:
            value = getattr(item, self.attribute)
        except AttributeError:
            obj = item.getObject()
            value = getattr(obj, self.attribute, ())

        if callable(value):
            value = value()

        if not isinstance(value, (list, tuple)):
            value = (value,)

        gtool = getToolByName(self.context, 'portal_groups')
        mtool = getToolByName(self.context, 'portal_membership')
        principals = []
        for principal_id in value:
            user = mtool.getMemberById(principal_id)
            if user is not None:
                principals.append(user.getProperty('fullname', None) or user.getId())
            else:
                group = gtool.getGroupById(principal_id)
                if group is not None:
                    principals.append(group.getProperty('title', None) or group.getId())

        return ', '.join(principals).decode('utf-8')


class LinkColumn(z3c.table.column.LinkColumn, Column):
    grok.baseclass()

    def getLinkURL(self, item):
        """Setup link url."""
        if self.linkName is not None:
            return '%s/%s' % (item.getURL(), self.linkName)
        return item.getURL()


class TitleColumn(LinkColumn):
    grok.baseclass()
    header = PMF("Title")
    weight = 10

    def getLinkContent(self, item):
        return item.Title.decode('utf8')


class IconColumn(object):
    def getLinkContent(self, item):
        return u"""<img title="%s" src="%s" />""" % (
                translate(self.linkContent, context=self.request),
                '%s/%s' % (self.table.portal_url, self.iconName))


class DeleteColumn(IconColumn, LinkColumn):
    grok.baseclass()
    header = u""
    weight = 9
    linkName = "delete_confirmation"
    linkContent = PMF('Delete')
    linkCSS = 'edm-delete-popup'
    iconName = "delete_icon.png"
    linkContent = PMF(u"Delete")

    def renderCell(self, item):
        obj = item.getObject()
        sm = getSecurityManager()
        if not sm.checkPermission('Delete objects', obj):
            return u""

        return super(DeleteColumn, self).renderCell(item)


class DownloadColumn(IconColumn, LinkColumn):
    grok.baseclass()
    header = u""
    weight = 1
    linkName = "@@download"
    iconName = "download_icon.png"
    linkContent = _(u"Download file")


class ExternalEditColumn(IconColumn, LinkColumn):
    grok.baseclass()
    header = u""
    weight = 3
    linkName = "@@external_edit"
    iconName = "extedit_icon.png"
    linkContent = PMF(u"Edit with external application")

    def renderCell(self, item):
        obj = item.getObject()
        sm = getSecurityManager()
        if not sm.checkPermission('Modify portal content', obj):
            return u""

        if not obj.restrictedTraverse('@@externalEditorEnabled').available():
            return u""

        return super(ExternalEditColumn, self).renderCell(item)


class EditColumn(IconColumn, LinkColumn):
    grok.baseclass()
    header = u""
    weight = 2
    linkName = "edit"
    iconName = "edit.png"
    linkContent = PMF(u"Edit")
    linkCSS = 'overlay-form-reload'

    def renderCell(self, item):
        obj = item.getObject()
        sm = getSecurityManager()
        if not sm.checkPermission('Modify portal content', obj):
            return u""

        return super(EditColumn, self).renderCell(item)


class StateColumn(Column):
    grok.baseclass()
    header = PMF(u"State")
    weight = 50

    def renderCell(self, item):
        try:
            wtool = self.table.wtool
            state_title = wtool.getTitleForStateOnType(item.review_state,
                                                       item.portal_type)
            return translate(PMF(state_title), context=self.request)
        except WorkflowException:
            return u""

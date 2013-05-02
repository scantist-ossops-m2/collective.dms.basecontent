from five import grok
from zope.interface import Interface
from zope.cachedescriptors.property import CachedProperty
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

from collective.dms.basecontent import _
from collective.dms.basecontent.dmsdocument import IDmsDocument
from collective.dms.basecontent.browser import table
from collective.dms.basecontent.browser.table import Column, DateColumn, Table

grok.templatedir('templates')

PMF = MessageFactory('plone')


class BaseTable(Table):

    @CachedProperty
    def values(self):
        portal_type = self.viewlet.portal_type
        portal_catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.context.getPhysicalPath())
        query = {}
        query['path'] = {'query' : folder_path}
        query['portal_type'] = portal_type

        results = portal_catalog.searchResults(query)
        return results


class FilesTable(BaseTable):
    pass


class TasksTable(BaseTable):
    pass


class TitleColumn(Column):
    grok.name('dms.title')
    grok.adapts(IDmsDocument, Interface, BaseTable)
    header = PMF("Title")
    weight = 10

    def renderCell(self, value):
        return u"""<a href="%s">%s</a>""" % (value.getURL(),
                                             value.Title.decode('utf8'))


class DirectDownloadColumn(Column):
    grok.name('dms.download')
    grok.adapts(IDmsDocument, Interface, FilesTable)
    header = u""
    weight = 100

    def renderCell(self, value):
        obj = value.getObject()
        download_file_msg = _(u"Download file")
        download_url = '%s/@@download' % obj.absolute_url()
        return u"""<a href="%s"><img title="%s" src="download_icon.png" /></a>""" % (
                download_url,
                translate(download_file_msg, context=self.request),
                )


class UpdateColumn(DateColumn):
    grok.name('dms.update')
    grok.adapts(IDmsDocument, Interface, FilesTable)
    header = PMF(u"listingheader_modified")
    attribute = 'modification_date'
    weight = 40


class StateColumn(Column):
    grok.name('dms.state')
    grok.adapts(IDmsDocument, Interface, BaseTable)
    header = PMF(u"State")
    weight = 50

    def renderCell(self, value):
        obj = value.getObject()
        try:
            wtool = self.table.wtool
            review_state = wtool.getInfoFor(obj, 'review_state')
            state_title = wtool.getTitleForStateOnType(review_state,
                                                       obj.portal_type)
            return translate(PMF(state_title), context=self.request)
        except WorkflowException:
            return u""


class ResponsibleColumn(Column):
    grok.name('dms.responsible')
    grok.adapts(IDmsDocument, Interface, TasksTable)
    header = _(u"Responsible")
    weight = 20

    def renderCell(self, value):
        obj = value.getObject()
        pas = getToolByName(self.context, 'acl_users')
        gtool = getToolByName(self.context, 'portal_groups')
        principals = []
        for principal_id in obj.responsible:
            user = pas.getUserById(principal_id)
            if user is not None:
                principals.append(user.getProperty('fullname', None) or user.getId())
            else:
                group = gtool.getGroupById(principal_id)
                if group is not None:
                    principals.append(group.getProperty('title', None) or group.getId())

        return ', '.join(principals).decode('utf-8')


class DeadlineColumn(table.DateColumn):
    grok.name('dms.deadline')
    grok.adapts(IDmsDocument, Interface, TasksTable)
    header = _(u"Deadline")
    attribute = 'deadline'
    weight = 30

from five import grok

from zope.interface import Interface
from zope.cachedescriptors.property import CachedProperty
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

from collective.dms.basecontent import _
from collective.dms.basecontent.browser.table import (
    Column, DateColumn, PrincipalColumn, TitleColumn,
    Table)


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


class VersionsTable(BaseTable):
    pass


class TasksTable(BaseTable):
    pass


class BaseTitleColumn(TitleColumn):
    grok.name('dms.title')
    grok.adapts(Interface, Interface, BaseTable)


class VersionsTitleColumn(BaseTitleColumn):
    grok.adapts(Interface, Interface, VersionsTable)
    contentClasses = 'version-link'


class DirectDownloadColumn(Column):
    grok.name('dms.download')
    grok.adapts(Interface, Interface, VersionsTable)
    header = u""
    weight = 1

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
    grok.adapts(Interface, Interface, VersionsTable)
    header = PMF(u"listingheader_modified")
    attribute = 'modification_date'
    weight = 40


class StateColumn(Column):
    grok.name('dms.state')
    grok.adapts(Interface, Interface, BaseTable)
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

class EnquirerColumn(PrincipalColumn):
    grok.name('dms.enquirer')
    grok.adapts(Interface, Interface, TasksTable)
    header = _(u"Enquirer")
    weight = 20
    attribute = 'enquirer'


class ResponsibleColumn(PrincipalColumn):
    grok.name('dms.responsible')
    grok.adapts(Interface, Interface, TasksTable)
    header = _(u"Responsible")
    weight = 30
    attribute = 'responsible'


class DeadlineColumn(DateColumn):
    grok.name('dms.deadline')
    grok.adapts(Interface, Interface, TasksTable)
    header = _(u"Deadline")
    attribute = 'deadline'
    weight = 60

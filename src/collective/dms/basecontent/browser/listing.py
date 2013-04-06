from five import grok
from zope.cachedescriptors.property import CachedProperty
import z3c.table.table
from z3c.table import interfaces
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate

from collective.dms.basecontent import _
from collective.dms.basecontent.dmsdocument import IDmsDocument

grok.templatedir('templates')
#grok.context(IDmsDocument)

PMF = MessageFactory('plone')

class Table(z3c.table.table.Table):
    cssClassEven = u'even'
    cssClassOdd = u'odd'
    cssClasses = {'table': 'listing'}
    sortOn = None
    batchSize = 10000
    startBatchingAt = 10000

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


class FilesTable(Table):
    pass


class TasksTable(Table):
    pass


class Column(z3c.table.column.Column, grok.MultiAdapter):
    grok.provides(interfaces.IColumn)
    grok.adapts(Interface, Interface, Table)
    grok.baseclass()


class TitleColumn(Column):
    grok.name('dms.title')
    header = PMF("Title")
    weight = 10

    def renderCell(self, value):
        return u"""<a href="%s">%s</a>""" % (value.getURL(), value.Title)


class DirectDownloadColumn(Column):
    grok.name('dms.download')
    grok.adapts(Interface, Interface, FilesTable)
    header = u""
    weight = 60

    def renderCell(self, value):
        obj = value.getObject()
        download_file_msg = _(u"Download file")
        download_url = '%s/@@download' % obj.absolute_url()
        return u"""<a href="%s"><img title="%s" src="download_icon.png" /></a>""" % (
                download_url,
                translate(download_file_msg, context=self.request),
                )


class ResponsibleColumn(Column):
    grok.name('dms.responsible')
    grok.adapts(Interface, Interface, TasksTable)
    header = _(u"Responsible")
    weight = 20

    def renderCell(self, value):
        obj = value.getObject()
        # TODO get fullname
        return u', '.join(obj.responsible)


class DeadlineColumn(Column):
    grok.name('dms.deadline')
    grok.adapts(Interface, Interface, TasksTable)
    header = _(u"Deadline")
    weight = 20

    def renderCell(self, value):
        obj = value.getObject()
        # TODO translate deadline
        return obj.deadline and str(obj.deadline) or u""

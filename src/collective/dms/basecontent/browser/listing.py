from five import grok
from zope.cachedescriptors.property import CachedProperty
import z3c.table.table
from z3c.table import interfaces
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory

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


class Column(z3c.table.column.Column, grok.MultiAdapter):
    grok.provides(interfaces.IColumn)
    grok.adapts(Interface, Interface, Table)
    grok.baseclass()


class TitleColumn(Column):
    header = PMF("Title")

    def renderCell(self, value):
        return u"""<a href="%s">%s</a>""" % (value.getURL(), value.Title)


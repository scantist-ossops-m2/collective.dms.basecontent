import datetime

from five import grok
from zope.cachedescriptors.property import CachedProperty
from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory
import z3c.table.table
import z3c.table.column
from z3c.table.interfaces import IBatchProvider

from plone.batching.interfaces import IBatch
from plone import api

PMF = MessageFactory('plone')

grok.templatedir('templates')


class TableViewlet(grok.Viewlet):
    grok.baseclass()
    grok.template('filesviewlet')
    __table__ = NotImplemented
    label = NotImplemented
    noresult_message = NotImplemented

    def update(self):
        self.table = self.__table__(self.context, self.request)
        self.table.viewlet = self
        self.table.update()


class Table(z3c.table.table.Table):
    cssClassEven = u'even'
    cssClassOdd = u'odd'
    cssClasses = {'table': 'listing nosort'}
    sortOn = None
    batchSize = 10000  # not used
    startBatchingAt = 10000  # not used
    batchProviderName = 'plonebatch'

    def batchRows(self):
        # this is not self.rows that is batched, but self.values
        pass

    def updateBatch(self):
        if IBatch.providedBy(self.values):
            self.batchProvider = getMultiAdapter((self.context,
                self.request, self), IBatchProvider,
                name=self.batchProviderName)
            self.batchProvider.update()

    @CachedProperty
    def translation_service(self):
        return api.portal.get_tool('translation_service')

    @CachedProperty
    def wtool(self):
        return api.portal.get_tool('portal_workflow')

    @CachedProperty
    def portal_url(self):
        return api.portal.get().absolute_url()

    def update(self):
        super(Table, self).update()

    def format_date(self, date, long_format=None, time_only=None):
        if date is None:
            return u""

        # If date is a datetime object, isinstance(date, datetime.date)
        # returns True, so we use type here.
        if type(date) == datetime.date:
            date = date.strftime('%Y/%m/%d')
        elif type(date) == datetime.datetime:
            date = date.strftime('%Y/%m/%d %H:%M')

        return self.translation_service.ulocalized_time(
            date,
            long_format=long_format,
            time_only=time_only,
            context=self.context,
            domain='plonelocales',
            request=self.request)

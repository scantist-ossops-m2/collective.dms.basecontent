import datetime

from Products.CMFCore.utils import getToolByName
from five import grok
from z3c.table import interfaces
from zope.cachedescriptors.property import CachedProperty
from zope.interface import Interface
import z3c.table.table

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
    cssClasses = {'table': 'listing'}
    sortOn = None
    batchSize = 10000
    startBatchingAt = 10000

    @CachedProperty
    def translation_service(self):
        return getToolByName(self.context, 'translation_service')

    @CachedProperty
    def wtool(self):
        return getToolByName(self.context, 'portal_workflow')

    def update(self):
        super(Table, self).update()

    def format_date(self, date):
        if date is None:
            return u""

        if isinstance(date, datetime.date):
            date = date.strftime('%Y/%m/%d')

        return self.translation_service.ulocalized_time(
            date,
            long_format=None,
            time_only=None,
            context=self.context,
            domain='plonelocales',
            request=self.request)


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

    def renderCell(self, value):
        obj = value.getObject()
        pas = getToolByName(self.context, 'acl_users')
        gtool = getToolByName(self.context, 'portal_groups')
        principals = []
        for principal_id in getattr(obj, self.attribute, ()):
            user = pas.getUserById(principal_id)
            if user is not None:
                principals.append(user.getProperty('fullname', None) or user.getId())
            else:
                group = gtool.getGroupById(principal_id)
                if group is not None:
                    principals.append(group.getProperty('title', None) or group.getId())

        return ', '.join(principals).decode('utf-8')

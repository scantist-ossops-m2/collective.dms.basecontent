from five import grok

from collective.dms.basecontent.dmsdocument import IDmsDocument
from collective.dms.basecontent import _
from collective.dms.basecontent.browser.listing import Table

grok.templatedir('templates')
grok.context(IDmsDocument)


class DmsBelowContentViewletManager(grok.ViewletManager):
    grok.name('dms.belowcontent')


class BaseViewlet(grok.Viewlet):
    grok.baseclass()
    grok.template('filesviewlet')
    grok.viewletmanager(DmsBelowContentViewletManager)

    def update(self):
        self.table = Table(self.context, self.request)
        self.table.viewlet = self
        self.table.update()

    def contentFilter(self):
        return {'portal_type': self.portal_type}


class FilesViewlet(BaseViewlet):
    grok.name('dms.files')
    grok.order(10)
    portal_type = 'dmsmainfile'
    label = _(u"Version notes")
    noresult_message = _(u"There is no version notes for this document.")


class AppendixViewlet(BaseViewlet):
    grok.name('dms.appendix')
    grok.order(20)
    portal_type = 'dmsappendixfile'
    label = _(u"Appendix")
    noresult_message = _(u"There is no appendix for this document.")

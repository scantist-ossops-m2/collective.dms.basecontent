from zope.interface import implements, implementer
from zope.component import adapter

from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.widget import FieldWidget
from z3c.relationfield.interfaces import IRelationList
from z3c.relationfield.schema import RelationChoice, RelationList

from plone.formwidget.autocomplete.widget import AutocompleteMultiSelectionWidget
from plone.formwidget.contenttree import ObjPathSourceBinder

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IRelatedDocs(IRelationList):
    """"""

class RelatedDocsWidget(AutocompleteMultiSelectionWidget):
    display_template = ViewPageTemplateFile('related-docs-display.pt')
    
    def get_url(self, v):
        return v

    def get_label(self, v):
        term = self.terms.getTermByToken(v)
        return term.title

    def tuples(self):
        print self.value
        return [(self.get_url(x), self.get_label(x)) for x in self.value]

@adapter(IRelatedDocs, IFormLayer)
@implementer(IFieldWidget)
def RelatedDocsFieldWidget(field, request):
    return FieldWidget(field, RelatedDocsWidget(request))

class RelatedDocs(RelationList):
    implements(IRelatedDocs)

    def __init__(self, portal_types, display_backrefs=False, **kwargs):
        RelationList.__init__(self,
                        value_type=RelationChoice(
                            title=u'',
                            source=ObjPathSourceBinder(
                                portal_type=portal_types)),
                        **kwargs)


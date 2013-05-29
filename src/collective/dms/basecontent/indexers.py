from ZODB.POSException import ConflictError
from five import grok
from Products.CMFCore.utils import getToolByName
from plone.indexer import indexer

from .dmsdocument import IDmsDocument

@indexer(IDmsDocument)
def document_dynamic_searchable_text_indexer(obj):
    # XXX: this hardcodes the version created by the batchimport process; it
    # should instead look into the content and take the latest version.
    try:
        data = obj['main'].file
    except KeyError:
        data = None

    if not data or data.getSize() == 0:
        return obj.title

    # if there is no path to text/plain, do nothing
    transforms = getToolByName(obj, 'portal_transforms')
    if not transforms._findPath(data.contentType, 'text/plain'):
        return obj.title

    # convert it to text/plain
    try:
        datastream = transforms.convertTo(
            'text/plain', data.data, mimetype=data.contentType,
            filename=data.filename)
        return obj.title + ' ' + unicode(datastream.getData(), 'utf-8')
    except (ConflictError, KeyboardInterrupt):
        raise

    return obj.title

grok.global_adapter(document_dynamic_searchable_text_indexer,
                    name='SearchableText')

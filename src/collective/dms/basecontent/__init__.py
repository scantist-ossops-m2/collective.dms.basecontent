from plone import api
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("collective.dms.basecontent")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


PLONE_VERSION = api.env.plone_version()[:3]

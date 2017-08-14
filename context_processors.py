"""Context Processors for Zinnia"""
from zinnia import __version__
from zinnia.settings import BADUTONGJITOKEN


def version(request):
    """
    Add version of Zinnia to the context.
    """
    return {'ZINNIA_VERSION': __version__, 'BADUTONGJITOKEN':BADUTONGJITOKEN}

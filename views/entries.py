"""Views for Zinnia entries"""
from django.views.generic.dates import BaseDateDetailView

from zinnia.models.entry import Entry
from zinnia.views.mixins.archives import ArchiveMixin
from zinnia.views.mixins.entry_cache import EntryCacheMixin
from zinnia.views.mixins.entry_preview import EntryPreviewMixin
from zinnia.views.mixins.entry_protection import EntryProtectionMixin
from zinnia.views.mixins.callable_queryset import CallableQuerysetMixin
from zinnia.views.mixins.templates import EntryArchiveTemplateResponseMixin
from zinnia.settings import MARKDOWN_EXTENSIONS

class EntryDateDetail(ArchiveMixin,
                      EntryArchiveTemplateResponseMixin,
                      CallableQuerysetMixin,
                      BaseDateDetailView):
    """
    Mixin combinating:

    - ArchiveMixin configuration centralizing conf for archive views
    - EntryArchiveTemplateResponseMixin to provide a
      custom templates depending on the date
    - BaseDateDetailView to retrieve the entry with date and slug
    - CallableQueryMixin to defer the execution of the *queryset*
      property when imported
    """
    queryset = Entry.published.on_site


class EntryDetail(EntryCacheMixin,
                  EntryPreviewMixin,
                  EntryProtectionMixin,
                  EntryDateDetail):
    """
    Detailled archive view for an Entry with password
    and login protections and restricted preview.
    """

    def get_context_data(self, **kwargs):
      context = super(EntryDetail, self).get_context_data(**kwargs)

      try:
          import markdown
      except ImportError:
          warnings.warn("The Python markdown library isn't installed.",
                        RuntimeWarning)
          return context

      md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)  
      context['html_content'] = md.convert(self.object.content)
      if len(md.toc) > 35:
        context['toc'] = md.toc

      return context

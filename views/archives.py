"""Views for Zinnia archives"""
import datetime

from django.utils import timezone
from django.views.generic.dates import BaseArchiveIndexView
from django.views.generic.dates import BaseYearArchiveView
from django.views.generic.dates import BaseMonthArchiveView
from django.views.generic.dates import BaseWeekArchiveView
from django.views.generic.dates import BaseDayArchiveView
from django.views.generic.dates import BaseTodayArchiveView

from zinnia.models.entry import Entry
from zinnia.views.mixins.archives import ArchiveMixin
from zinnia.views.mixins.archives import PreviousNextPublishedMixin
from zinnia.views.mixins.callable_queryset import CallableQuerysetMixin
from zinnia.views.mixins.prefetch_related import PrefetchCategoriesAuthorsMixin
from zinnia.views.mixins.templates import \
    EntryQuerysetArchiveTemplateResponseMixin
from zinnia.views.mixins.templates import \
    EntryQuerysetArchiveTodayTemplateResponseMixin


class EntryArchiveMixin(ArchiveMixin,
                        PreviousNextPublishedMixin,
                        PrefetchCategoriesAuthorsMixin,
                        CallableQuerysetMixin,
                        EntryQuerysetArchiveTemplateResponseMixin):
    """
    Mixin combinating:

    - ArchiveMixin configuration centralizing conf for archive views.
    - PrefetchCategoriesAuthorsMixin to prefetch related objects.
    - PreviousNextPublishedMixin for returning published archives.
    - CallableQueryMixin to force the update of the queryset.
    - EntryQuerysetArchiveTemplateResponseMixin to provide a
      custom templates for archives.
    """

    # 表示查询的是哪个model
    queryset = Entry.published_and_inhome.all


class EntryIndex(EntryArchiveMixin,
                 EntryQuerysetArchiveTodayTemplateResponseMixin,
                 BaseArchiveIndexView):
    """
    View returning the archive index.
    """
    # 表示除了object_list 还有 entry_list 这个context可以代表 model 的查询结果
    context_object_name = 'entry_list'


class EntryYear(EntryArchiveMixin, BaseYearArchiveView):
    """
    View returning the archives for a year.
    """
    make_object_list = True
    # A boolean specifying whether to retrieve the full list of objects for this year and pass those to the template. 
    # If True, the list of objects will be made available to the context. 
    # If False, the None queryset will be used as the object list. 
    # By default, this is False.

    template_name_suffix = '_archive_year'


class EntryMonth(EntryArchiveMixin, BaseMonthArchiveView):
    """
    View returning the archives for a month.
    """
    template_name_suffix = '_archive_month'


class EntryWeek(EntryArchiveMixin, BaseWeekArchiveView):
    """
    View returning the archive for a week.
    """
    template_name_suffix = '_archive_week'

    # Returns a 3-tuple containing (date_list, object_list, extra_context).
    # date_list is the list of dates for which data is available. 
    # object_list is the list of objects. 
    # extra_context is a dictionary of context data that will be added to any context data provided by the MultipleObjectMixin.
    def get_dated_items(self):
        """
        Override get_dated_items to add a useful 'week_end_day'
        variable in the extra context of the view.
        """
        self.date_list, self.object_list, extra_context = super(
            EntryWeek, self).get_dated_items()
        self.date_list = self.get_date_list(self.object_list, 'day')
        extra_context['week_end_day'] = extra_context[
            'week'] + datetime.timedelta(days=6)
        return self.date_list, self.object_list, extra_context


class EntryDay(EntryArchiveMixin, BaseDayArchiveView):
    """
    View returning the archive for a day.
    """
    template_name_suffix = '_archive_day'


class EntryToday(EntryArchiveMixin, BaseTodayArchiveView):
    """
    View returning the archive for the current day.
    """
    template_name_suffix = '_archive_today'

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        And defines self.year/month/day for
        EntryQuerysetArchiveTemplateResponseMixin.
        """
        now = timezone.now()
        if timezone.is_aware(now):
            now = timezone.localtime(now)
        today = now.date()
        self.year, self.month, self.day = today.isoformat().split('-')
        return self._get_dated_items(today)

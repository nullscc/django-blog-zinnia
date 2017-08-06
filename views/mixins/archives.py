"""Mixins for Zinnia archive views"""
from datetime import datetime
from datetime import timedelta

from zinnia.settings import PAGINATION
from zinnia.settings import ALLOW_EMPTY
from zinnia.settings import ALLOW_FUTURE


class ArchiveMixin(object):
    """
    Mixin centralizing the configuration of the archives views.
    """
    # 给 BaseArchiveIndexView->BaseDateListView->MultipleObjectMixin 使用的
    # 多少项分页
    paginate_by = PAGINATION

    # 决定当没有对象的时候是显示空页还是404页面(BaseDateListView)
    allow_empty = ALLOW_EMPTY

    # 决定当由 date_field 指定的时间大于当前时间时是不是将其代表的对象包括进来(DateMixin)
    allow_future = ALLOW_FUTURE

    # 当 time zone 开启并且 date_field 字段是一个 DateTimeField 时间以time zone为参照(DateMixin)
    date_field = 'publication_date'

    # The strftime() format to use when parsing the month. By default, this is '%b'.
    # (MonthMixin)
    month_format = '%m'

    # The strftime() format to use when parsing the week. By default, this is '%U', which means the week starts on Sunday. Set it to '%W' if your week starts on Monday.
    # (MonthMixin)
    week_format = '%W'


class PreviousNextPublishedMixin(object):
    """
    Mixin for correcting the previous/next
    context variable to return dates with published datas.
    """

    def get_previous_next_published(self, date):
        """
        Returns a dict of the next and previous date periods
        with published entries.
        """
        previous_next = getattr(self, 'previous_next', None)

        if previous_next is None:
            date_year = datetime(date.year, 1, 1)
            date_month = datetime(date.year, date.month, 1)
            date_day = datetime(date.year, date.month, date.day)
            date_next_week = date_day + timedelta(weeks=1)
            previous_next = {'year': [None, None],
                             'week': [None, None],
                             'month': [None, None],
                             'day':  [None, None]}

            # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#datetimes
            # datetimes函数返回数据库中按'publication_date'升序排列的精确于天的datetime.datetime数据列表
            dates = self.get_queryset().datetimes(
                'publication_date', 'day', order='ASC')
            for d in dates:
                d_year = datetime(d.year, 1, 1)
                d_month = datetime(d.year, d.month, 1)
                d_day = datetime(d.year, d.month, d.day)
                if d_year < date_year:
                    previous_next['year'][0] = d_year.date()
                elif d_year > date_year and not previous_next['year'][1]:
                    previous_next['year'][1] = d_year.date()
                if d_month < date_month:
                    previous_next['month'][0] = d_month.date()
                elif d_month > date_month and not previous_next['month'][1]:
                    previous_next['month'][1] = d_month.date()
                if d_day < date_day:
                    previous_next['day'][0] = d_day.date()
                    previous_next['week'][0] = d_day.date() - timedelta(
                        days=d_day.weekday())
                elif d_day > date_day and not previous_next['day'][1]:
                    previous_next['day'][1] = d_day.date()
                if d_day > date_next_week and not previous_next['week'][1]:
                    previous_next['week'][1] = d_day.date() - timedelta(
                        days=d_day.weekday())

            setattr(self, 'previous_next', previous_next)
        return previous_next

    # 返回相对于给定日期的，在数据库中有数据的下一年的第一天
    # 当没有数据时，是返回None还是抛出一个404异常？这取决于 allow_empty 和 allow_future
    def get_next_year(self, date):
        """
        Get the next year with published entries.
        """
        return self.get_previous_next_published(date)['year'][1]

    def get_previous_year(self, date):
        """
        Get the previous year with published entries.
        """
        return self.get_previous_next_published(date)['year'][0]

    def get_next_week(self, date):
        """
        Get the next week with published entries.
        """
        return self.get_previous_next_published(date)['week'][1]

    def get_previous_week(self, date):
        """
        Get the previous wek with published entries.
        """
        return self.get_previous_next_published(date)['week'][0]

    def get_next_month(self, date):
        """
        Get the next month with published entries.
        """
        return self.get_previous_next_published(date)['month'][1]

    def get_previous_month(self, date):
        """
        Get the previous month with published entries.
        """
        return self.get_previous_next_published(date)['month'][0]

    def get_next_day(self, date):
        """
        Get the next day with published entries.
        """
        return self.get_previous_next_published(date)['day'][1]

    def get_previous_day(self, date):
        """
        Get the previous day with published entries.
        """
        return self.get_previous_next_published(date)['day'][0]

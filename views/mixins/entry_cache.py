"""Cache mixins for Zinnia views"""


class EntryCacheMixin(object):
    """
    Mixin implementing cache on ``get_object`` method.
    """
    _cached_object = None

    # 用于缓存住文章的对象，这样不用每次都去取出新的文章对象
    # 默认是根据定义的model的slug(slug_field)来查找单个对象
    # 疑问：假如文章更新了怎么办？
    def get_object(self, queryset=None):
        """
        Implement cache on ``get_object`` method to
        avoid repetitive calls, in POST.
        """
        if self._cached_object is None:
            self._cached_object = super(EntryCacheMixin, self).get_object(
                queryset)
        return self._cached_object

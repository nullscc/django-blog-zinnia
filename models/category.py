"""Category model for Zinnia"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from mptt.managers import TreeManager

from zinnia.managers import entries_published
from zinnia.managers import EntryRelatedPublishedManager


@python_2_unicode_compatible
class Category(MPTTModel):
    """
    Simple model for categorizing entries.
    """

    title = models.CharField(
        _('title'), max_length=255)

    slug = models.SlugField(
        _('slug'), unique=True, max_length=255,
        help_text=_("Used to build the category's URL."))

    description = models.TextField(
        _('description'), blank=True)

    parent = TreeForeignKey(
        'self',
        related_name='children',    # 反向引用，就是相关联的对象能通过'children'找到这个对象
        null=True, blank=True,
        on_delete=models.SET_NULL,  # 当相关联的对象被删除以后这个键应该设置为什么
        verbose_name=_('parent category'))

    objects = TreeManager()         # 默认的管理器
    published = EntryRelatedPublishedManager() # 自定义已发布的管理器

    def entries_published(self):
        """
        Returns category's published entries.
        """
        return entries_published(self.entries)

    @property
    def tree_path(self):
        """
        Returns category's tree path
        by concatening the slug of his ancestors.
        """
        if self.parent_id:  # 说明存在父节点，此属性由 mptt 提供
            return '/'.join(
                # self.get_ancestors 会返回一个list，代表所有父节点
                [ancestor.slug for ancestor in self.get_ancestors()] +
                [self.slug])
        return self.slug

    
    @models.permalink
    def get_absolute_url(self): # 告诉 django 怎么得到 View on site的地址
        """
        Builds and returns the category's URL
        based on his tree path.
        """
        return ('zinnia:category_detail', (self.tree_path,))

    def __str__(self):                          # 以字符串形式表示此 model class
        return self.title

    class Meta:
        """
        Category's meta informations.
        """
        ordering = ['title']                    # 查询时的默认排序
        verbose_name = _('category')            # 单数名字
        verbose_name_plural = _('categories')   # 复数名字

    class MPTTMeta:
        """
        Category MPTT's meta informations.
        """
        order_insertion_by = ['title']  # 保存的时候应该按哪个的顺序保存

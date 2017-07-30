"""Forms for Zinnia admin"""
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from mptt.forms import TreeNodeChoiceField

from zinnia.models.entry import Entry
from zinnia.models.category import Category
from zinnia.admin.widgets import MiniTextarea
from zinnia.admin.widgets import TagAutoComplete
from zinnia.admin.widgets import MPTTFilteredSelectMultiple
from zinnia.admin.fields import MPTTModelMultipleChoiceField


class CategoryAdminForm(forms.ModelForm):
    """
    Form for Category's Admin.
    """
    # 重载表单的 parent 项
    parent = TreeNodeChoiceField(
        label=_('Parent category'),             # 表单显示的名称标签
        empty_label=_('No parent category'),    # 定义一个空的标签
        level_indicator='|--', required=False,  # 树状目录的层级指示器
        queryset=Category.objects.all())        # 查询的结果集

    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)

        # 为admin接口定制一个 add 的 icon，'parent' 就是这个表单的成员
        self.fields['parent'].widget = RelatedFieldWidgetWrapper(
            self.fields['parent'].widget,       # 已有的 widget
            Category.parent.field.remote_field, # 告诉django系统要为哪个model增加 add 的 icon，方便生成对应的链接
            self.admin_site)                    # 可以检查相关的对象是否已经注册在这个 AdminSite 上了

    def clean_parent(self):                     # https://docs.djangoproject.com/en/1.11/ref/forms/validation/
        """
        Check if category parent is not selfish.
        """
        data = self.cleaned_data['parent']      # self.cleaned_data 表示数据已经被验证过一次的数据
        if data == self.instance:               # self.instance 由 forms.ModelForm提供，表示其自身
            raise forms.ValidationError(
                _('A category cannot be parent of itself.'),
                code='self_parenting')
        return data

    class Meta:
        """
        CategoryAdminForm's Meta.
        """
        model = Category                        # 表示这个 admin form 对应的是哪个model
        fields = forms.ALL_FIELDS

# 定义日志表单和widget
class EntryAdminForm(forms.ModelForm):
    """
    Form for Entry's Admin.
    """
    categories = MPTTModelMultipleChoiceField(
        label=_('Categories'), required=False,
        queryset=Category.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('categories')))

    def __init__(self, *args, **kwargs):
        super(EntryAdminForm, self).__init__(*args, **kwargs)
        self.fields['categories'].widget = RelatedFieldWidgetWrapper(
            self.fields['categories'].widget,
            Entry.categories.field.remote_field,
            self.admin_site)

    class Meta:
        """
        EntryAdminForm's Meta.
        """
        model = Entry
        fields = forms.ALL_FIELDS
        widgets = {
            'tags': TagAutoComplete,
            'lead': MiniTextarea,
            'excerpt': MiniTextarea,
            'image_caption': MiniTextarea,
        }

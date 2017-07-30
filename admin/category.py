"""CategoryAdmin for Zinnia"""
from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from zinnia.admin.forms import CategoryAdminForm


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin for Category model.
    """
    # 更改 add/change 页面的表单
    form = CategoryAdminForm

    fields = ('title', 'parent', 'description', 'slug')

    # 在admin页面点击 change 后跳转显示的页面
    list_display = ('title', 'slug', 'get_tree_path', 'description')
    
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'description')
    list_filter = ('parent',)

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(CategoryAdmin, self).__init__(model, admin_site)

    def get_tree_path(self, category):
        """
        Return the category's tree path in HTML.
        """
        try:
            return format_html(
                '<a href="{}" target="blank">/{}/</a>',
                category.get_absolute_url(), category.tree_path)
        except NoReverseMatch:
            return '/%s/' % category.tree_path
    get_tree_path.short_description = _('tree path')

# from django.contrib import admin
import xadmin
from xadmin import views

from art.models import Category, Art


# 配置主题
class BaseSettings:
    enable_themes = False
    use_bootswatch = False

# 全局的配置
class GlobalSettings:
    site_title = '文章后台管理系统'
    site_footer = '@<span style="font-size:25px; color:blue;">千锋教育.</span> <a href="http://www.qfedu.com" class="btn btn-link">郑州Py1802</a>'
    menu_style = 'accordion'  # 菜单折叠效果

    global_search_models = [Art, Category]
    global_models_icon = {
        Art: 'glyphicon glyphicon-cloud',
        Category: 'glyphicon glyphicon-music'
    }


# 配置模型的输出
class CategoryAdmin:

    list_display = ['name', 'add_time']  # 显示字段
    search_fields = ['name']  # 搜索字段

class ArtAdmin:
    list_display = ['title', 'author', 'content', 'publish_time', 'category']
    search_fields = ['title', 'category__name']
    list_per_page = 10  # 每页显示的记录数

    # 设置字段的样式
    style_fields = {
        'content': 'ueditor'
    }

# Register your models here.
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)


xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Art, ArtAdmin)

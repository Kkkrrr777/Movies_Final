from django.contrib import admin

from django.contrib import admin
from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'imdb_id', 'viewers_count', 'play_link', 'time', 'intro', 'writers', 'actors', 'director', 'release_time', ]  # 在列表页面显示的字段
    search_fields = ['name', 'director']  # 添加搜索功能，可根据指定字段搜索
    list_filter = ['release_time']  # 添加过滤器，可根据指定字段过滤


admin.site.register(Movie, MovieAdmin)

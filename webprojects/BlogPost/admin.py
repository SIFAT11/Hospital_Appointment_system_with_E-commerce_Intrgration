from django.contrib import admin
from .models import Blogpost

class BlogpostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    search_fields = ['title', 'pub_date']
    list_filter = ('pub_date',)
admin.site.register(Blogpost, BlogpostAdmin)



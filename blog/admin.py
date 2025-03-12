from django.contrib import admin
from .models import Post, Comment, Category, Contact
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'category', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on', 'category')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Comment)

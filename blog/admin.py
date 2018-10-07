from django.contrib import admin
from .models import Post, Comments
# Register your models here.

class PostInline(admin.StackedInline):
    model = Comments
    extra=2

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","updated", "timestamp"]
    list_display_links = ["updated"]
    list_filter = ["timestamp"]
    #list_editable = ["title"]
    inlines = [PostInline]
    search_fields = ["title", "text"]
    class Meta:
        model = Post



admin.site.register(Post, PostModelAdmin)





# class PostAdmin(admin.ModelAdmin):
#     fields= ['author','title', 'text', 'published_date']
#     inlines= [PostInline]
#     list_filter = ['published_date']

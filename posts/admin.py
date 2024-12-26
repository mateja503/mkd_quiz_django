from django.contrib import admin
from .models import Post
from .models import Contestant, Results


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'image')
    list_filter = ('title',)

admin.site.register(Post, PostAdmin)
admin.site.register(Contestant)
admin.site.register(Results)

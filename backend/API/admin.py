from django.contrib import admin
from  .models import User,Profile,Category,Post,Comment,BookMark,Notification


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug" :["title"]}
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Category,PostAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(BookMark)
admin.site.register(Notification)
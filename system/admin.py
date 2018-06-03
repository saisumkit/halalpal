from django.contrib import admin
from .models import Shops, Review, Activity, Poll, Choice, Vote

# Register your models here.
admin.site.register(Shops)

# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('user', 'body', 'created_date')
#
# admin.site.register(Review, ReviewAdmin)
admin.site.register(Review)
admin.site.register(Activity)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)

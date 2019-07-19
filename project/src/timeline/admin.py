from django.contrib import admin
from timeline.models import RestaurantTimelineComment, MenuTimelineComment

# Register your models here.
admin.site.register(RestaurantTimelineComment)
admin.site.register(MenuTimelineComment)

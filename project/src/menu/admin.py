from django.contrib import admin
from menu.models import Menu, MenuTimeLine
from timeline.models import TimelineStatus

admin.site.register(MenuTimeLine)


@admin.register(Menu)
class MenuTimeLineHandler(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        kwargs = {}
        flag = False
        if change:
            data_to_insert = ['price', 'detail', 'img', 'is_yosigy', 'is_set_menu']
            exclude_fields = ['restaurant', 'type', 'tastes', 'hit', 'like', 'score', 'is_recommended', 'name',
                              'is_yosigy', 'is_set_menu']
            for data in form.changed_data:
                if data in data_to_insert:
                    data_to_insert.remove(data)
                if data not in exclude_fields:
                    flag = True
                    prior_menu_data = 'prior_menu_' + data
                    post_menu_data = 'post_menu_' + data
                    kwargs[prior_menu_data] = form.initial[data]
                    kwargs[post_menu_data] = form.cleaned_data[data]
            if flag:
                for data in data_to_insert:
                    kwargs['post_menu_'+data] = form.initial[data]
                kwargs['status'] = TimelineStatus.UPDATE
                kwargs['menu'] = obj
                menu_time_line = MenuTimeLine(**kwargs)
                menu_time_line.save()
            super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)
            exclude_fields = ['restaurant', 'type', 'tastes', 'hit', 'like', 'score', 'is_recommended', 'name', ]
            for data in form.changed_data:
                if data not in exclude_fields:
                    flag = True
                    post_menu_data = 'post_menu_' + data
                    kwargs[post_menu_data] = form.cleaned_data[data]
            if flag:
                kwargs['status'] = TimelineStatus.CREATE
                kwargs['menu'] = obj
                menu_time_line = MenuTimeLine(**kwargs)
                menu_time_line.save()

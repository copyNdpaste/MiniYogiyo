from django.contrib import admin

from restaurant.models import Restaurant, RestaurantTimeline
from timeline import models as timeline


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if obj.pk:
            timeline_type = timeline.TimelineType
            create_fields = {'restaurant_id': obj.pk}
            type_name = timeline_type.INFO

            post_data = request.POST
            changed_data_list = form.changed_data

            prior_restaurant_obj = Restaurant.objects.filter(pk=obj.pk).values()

            for data in changed_data_list:
                if data == 'info':
                    type_name = timeline_type.NOTICE
                    create_fields['changed_data'] = post_data.get(data)

                elif data == 'event' or data == 'event_img':
                    type_name = timeline_type.EVENT
                    create_fields['changed_data'] = obj.event
                    create_fields['changed_img'] = obj.event_img

                    try:
                        changed_data_list.remove('event_img')

                    except ValueError:
                        pass

                elif 'operation' in str(data):
                    type_name = timeline_type.OPERATION_HOUR
                    create_fields['post_info'] = (
                        '-'.join([
                            str(obj.operation_start_hour.strftime('%H:%M')),
                            str(obj.operation_end_hour.strftime('%H:%M'))]))
                    prior_restaurant_dict = list(prior_restaurant_obj)[0]
                    create_fields['prior_info'] = (
                        '-'.join([
                            str(prior_restaurant_dict['operation_start_hour'].strftime('%H:%M')),
                            str(prior_restaurant_dict['operation_end_hour'].strftime('%H:%M'))
                        ]))
                    create_fields['changed_field'] = dict(timeline.TYPE_CHOICES)[type_name]

                    try:
                        changed_data_list.remove('operation_end_hour')

                    except ValueError:
                        pass

                elif data == 'store_owner' or data == 'img ':
                    pass

                else:
                    create_fields['post_info'] = post_data.get(data)
                    create_fields['prior_info'] = list(prior_restaurant_obj)[0][data]
                    create_fields['changed_field'] = data

                create_fields['timeline_type'] = type_name

                if data != 'img' and data != 'store_owner':
                    RestaurantTimeline.objects.create(**create_fields)

        super().save_model(request, obj, form, change)


admin.site.register(RestaurantTimeline)

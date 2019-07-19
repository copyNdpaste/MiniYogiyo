import json


class DateTimeFormatEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.strftime('%Y년 %m월 %d일 %H시 %M분')

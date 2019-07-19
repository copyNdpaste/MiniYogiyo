import json
import re

from datetime import datetime
from http import HTTPStatus
from urllib.request import urlopen

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from config.settings.utils import get_env_var
from grid.models import Grid
from menu.models import Menu


def get_dong(user_address):
    dong_pattern = re.compile(r'^[가-힣]+[1-9]*동$')
    addrs = user_address.split(' ')
    for addr in addrs:
        if re.fullmatch(dong_pattern, addr):
            return addr

def get_x_y_grid(user_dong):
    try:
        x_y_grid = get_object_or_404(Grid, name=user_dong)
        return x_y_grid
    except:
        return JsonResponse(
            {
                "message": "동에 대한 x, y 좌표 정보가 없습니다.",
            },
            status=HTTPStatus.BAD_REQUEST,
        )


def get_base_time(hour):
    hour = int(hour)
    if hour < 3:
        temp_hour = '20'
    elif hour < 6:
        temp_hour = '23'
    elif hour < 9:
        temp_hour = '02'
    elif hour < 12:
        temp_hour = '05'
    elif hour < 15:
        temp_hour = '08'
    elif hour < 18:
        temp_hour = '11'
    elif hour < 21:
        temp_hour = '14'
    elif hour < 24:
        temp_hour = '17'

    return temp_hour + '00'


def get_sky_info(data):
    try:
        weather_info = data['response']['body']['items']['item']
        if weather_info[3]['category'] == 'SKY':
            return weather_info[3]['fcstValue']
        elif weather_info[5]['category'] == 'SKY':
            return weather_info[5]['fcstValue']
    except KeyError:
        return JsonResponse(
            {
                "message": "기상청 서버로부터 날씨 정보를 가져오는 중 문제가 발생하여 날씨 정보를 받아오지 못했습니다.",
            },
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


def get_user_dong_weather(nx, ny):
    service_key = get_env_var('WEATHER_API_SERVICE_KEY')
    now = datetime.now()
    now_date = now.strftime('%Y%m%d')
    now_hour = int(now.strftime('%H'))

    if now_hour < 6:
        base_date = str(int(now_date) - 1)
    else:
        base_date = now_date
    base_hour = get_base_time(now_hour)

    num_of_rows = '6'
    base_date = base_date
    base_time = base_hour
    nx = str(nx)
    ny = str(ny)
    _type = 'json'
    api_url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?serviceKey={}' \
              '&base_date={}&base_time={}&nx={}&ny={}&numOfRows={}&_type={}'.format(
        service_key, base_date, base_time, nx, ny, num_of_rows, _type)

    data = urlopen(api_url).read().decode('utf8')
    json_data = json.loads(data)
    sky = get_sky_info(json_data)
    return sky


def get_restaurants(**kwargs):
    restaurant_id = kwargs['restaurant_id']
    category_id = kwargs['category_id']
    menu = Menu.objects.filter(restaurant=restaurant_id).values(
        'restaurant', 'pk', 'name', 'img', 'detail', 'price', 'type',
    )
    if not menu:
        return JsonResponse(
            {
                "message": "메뉴가 존재하지 않습니다.",
            },
            status=HTTPStatus.NOT_FOUND,
        )
    menu = list(menu, )
    data = {
        'menu': menu,
        'category_id': category_id,
    }
    return JsonResponse(data)
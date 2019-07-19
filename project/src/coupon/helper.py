from django.core.mail import EmailMessage
from config.settings import base as settings


def set_email_msg(user, gift_coupon):
    title = '[Mini 요기요]' + str(user.username) + '님이 보내신 gift card가 도착했습니다.'
    message = \
        '<h3>[요기요 Gift Card] ' + str(user.username) + \
        '님이 gift card를 선물하였습니다.</h3>' \
        '<p>상품명: 미니 요기요 gift card(' + str(gift_coupon.price) + '원 권)<br>' \
        'gift card 번호: ' + str(gift_coupon.coupon_code) + '<br>'\
        '유효기간: ' + str(gift_coupon.expire_date.strftime('%Y.%m.%d')) + '까지<br>'\
        '메세지: ' + str(gift_coupon.sender_msg) + '<br>' \
        '<a href = "' + settings.LOCALHOST + '/coupon/register_coupon/'+str(gift_coupon.coupon_code)+'">' \
        ' gift card 등록하러 가기 </a></p>'

    return title, message


def send_coupon_email(user, gift_coupon):
    title, message = set_email_msg(user, gift_coupon)

    email = EmailMessage(title, message, to=[gift_coupon.receiver_email])
    email.content_subtype = 'html'
    email.send(fail_silently=False)

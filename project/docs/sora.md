# sora

## 1. User

| name           | desc |
| ------------   | ------------------|
| phone          | 핸드폰 번호          |
| address        | 우편번호용 주소       |
| address_detail | 상세주소             |
| user_type      | 1: 일반회원, 2: 사장님|
| deactivate_date| 비활성화한 날짜       |

## My Page
#### my page 조회

* url: /api/accounts/my_page/
* method: GET

response(success):

```shell
{
    "username": "chocolates9991",
    "email": "chocolates9991@gmail.com",
    "phone": null,
    "address": "",
    "address_detail": "",
    "tastes": [
				...
        {
            "id": 5,
            "name": "high quality",
            "checked": false
        },
        {
            "id": 8,
            "name": "웰빙",
            "checked": true
        },
        ...
    ]
}
```

### My Page 수정

body

```shell
{"address":"1",
 "phone":5,
 "address_detail":"1",
 "taste": [1, 2]
 }
```

### GiftCoupon 생성

* url: api/coupon/create_gift_coupon/
* method: post

body

```shell
{
   "receiver_name":"홍길동",
   "receiver_email":"sora.son@deliveryhero.co.kr",
   "receiver_phone":"",
   "sender_msg":"선물입니다.",
   "price":"10000"
}
```

### GiftCoupon 등록

* url: api/coupon/register_gift_coupon/
* method: post

body

```shell
{
   "coupon_code": "171d14fb-b479-4f11-867c-fa427c4b2781"
}
```

### 받은 쿠폰 보기

* url: /api/coupon/received_coupon_list/
* method: GET

response(success):

```shell
{
    "coupons": [
        {
            "registered_coupon_id": 15,
            "coupon_id": 8,
            "coupon_code": "171d14fb-b479-4f11-867c-fa427c4b278d",
            "price": 10000,
            "is_used": false,
            "is_owner": true,
            "sender_name": "admin",
            "expire_date": "2019-08-11",
            "create_date": "2019-05-13",
            "register_date": "2019-05-14",
            "is_expired": false,
            "is_available": true,
            "is_handover": false
        },
        {
            "registered_coupon_id": 14,
            "coupon_id": 7,
            "coupon_code": "693c3140-03b3-48ab-8254-41b0586fbe00",
            "price": 10000,
            "is_used": false,
            "is_owner": false,
            "sender_name": "chocolates9991",
            "expire_date": "2019-05-13",
            "create_date": "2019-05-13",
            "register_date": "2019-05-14",
            "is_expired": true,
            "is_available": false,
            "is_handover": true
        }
    ]

# 루키 히어로 테크 인턴쉽 백엔드

## :star: Intro

> 이 문서는 4월 22일 부터 ~ 7월 5일 까지 5번의 스프린트 간에 기획 / 개발을 진행한 '미니 요기요' 에 대한 문서 입니다.



## Getting Started

### Prerequisites

* pip3
* python3(3.6.5)
* Django(2.0)

### Run in development

```python 
# 루키히어로 레포 클론
> git clone https://github.com/yogiyo/rookiehero.git
    
# 폴더 변경
> cd rookiehero/project/requirements

# pip 설치 및 development.txt 내 라이브러리 설치
> pip3 install --upgrade pip3
> pip3 install -r development.txt

# runserver를 위한 환경설정
1. 아래 경로에서, 사용자 1명을 선택 혹은 새로운 사용자를 생성한다.
src -> config -> settings
* dev_kth.py
* dev_smh.py
* dev_ssr.py

2. manage.py를 다음과 같이 수정해준다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') ->
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev_kth')

3. DB 설정 정보 및, API, Secret Key 관리

* 설정정보 관련 json 파일 경로 환경변수 등록

(1) ~/.zshrc 파일에 CONFIG 환경변수 추가
    ex) export CONFIG="/Users/b201903150/workspace/settings/json/settings.json"
(2) settings.json 파일 세팅
{
  "NAME": "",
  "USER": "",
  "PASSWORD": "",
  "HOST": "",
  "PORT": "",
  "SECRET_KEY": "",
  "GOOGLE_KEY": "",
  "GOOGLE_SECRET": "",
  "EMAIL_HOST_PASSWORD": ""
}

# Run dev server
> python3 manage.py runserver
```



### Project folder structure

```
src
├── __init__.py
├── accounts
│   ├── api
│   ├── fixture
│   ├── test
├── cart
│   ├── api
│   ├── test
├── category
│   ├── api
│   ├── test
├── config
│   ├── settings
├── coupon
│   ├── api
│   ├── test
├── grid
├── grouppurchase
│   ├── api
│   ├── test
├── home
├── manage.py
├── media
├── menu
│   ├── api
│   ├── test
├── order
│   ├── api
│   ├── test
├── restaurant
│   ├── api
│   ├── test
├── static
│   ├── css
│   ├── img
│   └── js
├── templates
│   ├── accounts
│   ├── cart
│   ├── common
│   ├── coupon
│   ├── grouppurchase
│   ├── home
│   ├── menu
│   ├── order
│   ├── restaurant
│   ├── timeline
│   └── yosigy
├── timeline
│   ├── api
│   ├── test
└── yosigy
    ├── api
    ├── test
```



### Dependencies

| Dependence             | Version |
| ---------------------- | ------- |
| Django                 | 2.1     |
| social-auth-app-django | 3.1.0   |
| Pillow                 | 6.0.0   |
| django-bulk-update     | 2.2.0   |
| django-querycount      | 0.7.0   |
| django-extensions      | 2.1.6   |
|                        |         |

### ERD

![mini_yogiyo_erd](assets/mini_yogiyo_erd-3159463.png)

## API Specifications

## accounts

####  로그아웃

- url: `api/accounts/logout/`
- method:  `GET`
- path params: None

- description: 

  로그인한 사용자가 로그아웃 

------

#### 마이 페이지 조회

- url: `api/accounts/my_page/`
- method: `GET`
- path params: None

- description:

  로그인한 사용자가 자신의 정보(아이디, email, 전화번호, 주소, 자신의 취향) 조회

------

#### 마이 페이지 수정

- url: `api/accounts/my_page/`
- method: `POST`
- path params: None

- description:
  로그인한 사용자가 자신의 정보 중 전화번호, 주소, 자신의 취향 수정 가능

- body params: Json Object

  | name           | required | type      | Desc                 |
  | -------------- | -------- | --------- | -------------------- |
  | phone          | yes      | String    | 전화번호(공백가능)   |
  | address        | yes      | String    | 주소(공백가능)       |
  | address_detail | yes      | String    | 상세주소(공백가능)   |
  | tastes         | no       | Integer[] | 취향 id(pk)의 리스트 |

------



## cart

#### 주문표 내 총 메뉴 개수 조회

- url: `api/cart/quantity/`
- method:  GET
- path params: None
- description: 주문 표 내의 총 메뉴 개수를 반환

------------



#### 주문표 내 메뉴의 리스트 조회

* url: `api/cart/`
* method:  GET
* path params: None
* description: 주문표 내 메뉴 리스트 조회

----------------



#### 주문표 생성

* url: `api/cart/`

* method: POST

* path params: None

* description: 내가 주문할 메뉴에 대한 주문표를 생성

* body params: Json Object

    | name | required | type    | Desc    |
    | ---- | -------- | ------- | ------- |
    | user | yes      | Integer | 유저 id |

-------------



#### 주문표에 메뉴 추가

- url: `api/cart/<uuid:cart_id>/`

- method: POST

- path params:

    | name    | type | desc                           |
    | ------- | ---- | ------------------------------ |
    | cart_id | Uuid | 사용자에게 현재 할당된 cart_id |

- description: 주문표에 내가 주문하려는 특정 메뉴를 추가

- body params: Json Object

    | name | required | type    | Desc                             |
    | ---- | -------- | ------- | -------------------------------- |
    | cart | yes      | uuid    | 사용자에 할당된 주문표           |
    | menu | yes      | Integer | 사용자가 주문표에 추가할 메뉴 id |

------



#### 주문표의 특정 메뉴 삭제

- url: `<uuid:cart_id>/menu/<int:menu_id>/delete/`

- method: DELETE

- path params:

    | name    | type    | desc                           |
    | ------- | ------- | ------------------------------ |
    | cart_id | Uuid    | 사용자에게 현재 할당된 cart_id |
    | menu_id | Integer | 삭제할 특정 메뉴의 id          |

- description: 주문표에서 특정 메뉴를 삭제

--------------



#### 주문표 삭제

- url: `api/<uuid:cart_id>/delete/`

- method: DELETE

- path params:

    | name    | type | desc                           |
    | ------- | ---- | ------------------------------ |
    | cart_id | Uuid | 사용자에게 현재 할당된 cart_id |

- description: 주문표를 삭제한다.(삭제되고 나서, 새로운 주문표가 생성된다.)

-------------------------



#### 주문표 내 메뉴 개수를 조정

- url: `api/cart/<uuid:cart_id>/update/`

- method: PUT

- path params:

    | name    | type | desc                           |
    | ------- | ---- | ------------------------------ |
    | cart_id | Uuid | 사용자에게 현재 할당된 cart_id |

- description: 주문표 내 메뉴 개수를 조정

- body params: Json Object

    | name     | required | type    | Desc                                       |
    | -------- | -------- | ------- | ------------------------------------------ |
    | menu     | yes      | integer | 주문표에 추가된 메뉴 중 개수를 조정할 메뉴 |
    | quantity | yes      | integer | 주문표에 추가된 특정 메뉴의 수정할 개수    |

    Ex)

    ```json
    [
        {
            "menu": 1,
            "quantity": 5
        },
        {
            "menu": 2,
            "quantity": 6
        },
        {
            "menu": 3,
            "quantity": 7
        }
    ]
    ```

    

-----------------------



## coupon

#### gift card 생성

- url: `api/coupon/create_gift_coupon/`
- method: POST
- path params: None

- description: 
  Gift Card를 받는 사람의 이름, 이메일, 핸드폰, 메세지, 선물보낼 가격을 기입하여 gift card선물

- body params: Json Object

  | name           | required | type      | Desc                                                     |
  | -------------- | -------- | --------- | -------------------------------------------------------- |
  | receiver_name  | yes      | String    |                                                          |
  | receiver_email | yes      | String    | 받는사람 email(@를 포함한 이메일)                        |
  | receiver_phone | yes      | String    | 받는 사람 전화번호(공백가능)                             |
  | sender_msg     | yes      | Integer[] | 선물 받는 사람에게 보낼 메세지(공백가능)                 |
  | price          | yes      | Integer   | Gift card 가격(5천원 이상, 10만원 미만의 천원단위 금액 ) |

------

#### gift card 등록

- url: `api/coupon/register_gift_coupon/`
- method: POST
- path params: None

- description:
  선물받은 gift card의 번호를 입력하여 gift card를 등록

- body params: Json Object

  | name        | required | type   | Desc             |
  | ----------- | -------- | ------ | ---------------- |
  | coupon_code | yes      | String | gift card의 번호 |

------

#### 받은 gift card 리스트 조회 

- url: `api/coupon/received_coupon_list/`
- method:  GET
- path params: None

- description: 
  선물 받거나, 양도받은 gift card 리스트

------

#### 보낸 gift card 리스트 조회

- url: `api/coupon/sent_coupon_list/`
- method: GET
- path params: None

- description:
  선물보내거나, 양도 보낸 gift card 리스트

------

#### 이용가능한 gift card 리스트 조회

- url: `api/coupon/available_coupon_list/`
- method: GET
- path params: None

- description:
  이용가능한 gift card의 리스트

------

#### 쿠폰 양도하기

- url: `api/coupon/use_coupon/<int:registered_coupon_id>/`

- method: POST

- path params:

  | name                 | type    | desc                                      |
  | -------------------- | ------- | ----------------------------------------- |
  | registered_coupon_id | Integer | registered_coupon_id(UserGiftCoupon의 pk) |

- description:
  받은 gift card 리스트중 양도가능한 gift card를 양도받을 사람의 미니 요기요 계정의 username 또는 email을 기입하여양도하기

- body params: Json Object

  | name     | required | type   | Desc                                                  |
  | -------- | -------- | ------ | :---------------------------------------------------- |
  | username | yes      | String | 양도받는 사람의 username(미니 요기요 계정의 username) |
  | email    | yes      | String | 양도받는 사람의 email(미니요기요 계정의 email)        |

------

#### 확인하지 않은 양도받은 gift card 리스트 조회

- url: `api/coupon/unchecked_coupon_list/`
- method: GET
- path params: None

- description:
  양도받은 후 확인하지 않은 gift card 리스트

------

#### 양도받은 gift card 확인

- url: `api/coupon/unchecked_coupon_list/`
- method: PUT
- path params: None

- description:

  양도받은 gift card를 확인

------



## menu

#### 레스토랑의 메뉴 출력

-   url: `api/category/<int:category_id>/restaurant/<int:restaurant_id>/menu/`
-   method: GET
-   path params:

| name          | required | desc |
| ------------- | -------- | ---- |
| category_id   | yes      | pk   |
| restaurant_id | yes      | pk   |

-   description: 레스토랑 선택 시 나오는 메뉴들

------

#### 날씨yo 메뉴 출력

-   url: `api/category/<int:category_id>/menu/`
-   method: GET

-   path params:

| name        | required | desc |
| ----------- | -------- | ---- |
| category_id | yes      | pk   |

-   description: 날씨yo 페이지 이동 시 나오는 메뉴들

------

#### 메뉴 디테일 출력

-   url: `api/category/<int:category_id>/restaurant/<int:restaurant_id>/menu/<int:menu_id>/`
-   method: GET

-   path params:

| name          | required | desc |
| ------------- | -------- | ---- |
| category_id   | yes      | pk   |
| restaurant_id | yes      | pk   |
| menu_id       | yes      | pk   |

-   description: 메뉴 선택 시 나오는 메뉴 상세 정보

------

## order

#### 주문 생성하기

- url: `api/order/`

- method: POST

- path params: None

- description: 주문을 생성

- body params: Json Object

    | name           | required | type     | Desc                             |
    | -------------- | -------- | -------- | :------------------------------- |
    | user           | yes      | Integer  | 로그인한 유저 id                 |
    | cart           | yes      | uuid     | 로그인한 유저에 할당된 주문표 id |
    | restaurant     | yes      | Interger | 레스토랑 id                      |
    | total_price    | yes      | Integer  | 총 가격                          |
    | address        | yes      | String   | 주소                             |
    | address_detail | yes      | String   | 상세 주소                        |
    | phone_num      | yes      | String   | 전화번호                         |
    | payment_status | yes      | Integer  | 결제 상태                        |
    | gift_coupon    | No       | Integer  | 사용된 Gift Card                 |
    | weather        | yes      | Integer  | 유저 주문장소의 날씨 정보        |

------

#### 

#### 주문페이지에서 주문표에 담긴 메뉴 보기

- url: `api/order/`
- method: GET
- path params: None
- description: 주문페이지에서 주문표에 담긴 메뉴 및 결제 정보들을 보여준다

------



#### 주문 내역 리스트를 조회

* url: `api/order/history/`
* method: GET
* path params: None
* description: 주문 내역에 대한 리스트를 조회

----------------



#### 재주문 하기

- url: `api/reorder/<uuid:order_id>/`

- method: POST

- path params:

    | name     | type | desc                       |
    | -------- | ---- | -------------------------- |
    | order_id | uuid | 재주문 하고 싶은 주문의 id |

- description: 기존에 주문했던 내역에 대해서 재 주문 한다

-------------------------



## restaurant

#### 레스토랑 리스트 출력

-   url: `api/category/<int:category_id>/restaurant/`
-   method: GET
-   path params:

| name        | required | desc |
| ----------- | -------- | ---- |
| category_id | yes      | pk   |

-   description: 특정 카테고리에 접속하면 그에 해당하는 레스토랑 리스트 출력됨

#### 레스토랑 디테일 출력

-   url: `api/category/<int:category_id>/restaurant/<int:restaurant_id>/`
-   method: GET
-   path params:

| name          | required | Desc |
| ------------- | -------- | ---- |
| category_id   | yes      | pk   |
| restaurant_id | yes      | pk   |

-   description: 특정 레스토랑에 접속하면 레스토랑 상세 정보 출력됨

#### 레스토랑 구독

-   url: `api/subscribe/restaurant/<int:restaurant_id>/`
-   method: POST
-   path params:

| name          | required | desc |
| ------------- | -------- | ---- |
| restaurant_id | yes      | pk   |

-   description: 구독하기 버튼을 누르면 구독이 되거나 취소됨(toggle)

#### 구독 중인 레스토랑 출력

-   url: `api/subscribed_restaurants/`
-   method: GET
-   path params: `None`
-   description: mypage에 접속하면 현재 구독 중인 레스토랑이 출력됨



## timeline

#### 레스토랑 타임라인 조회

- url: `api/timeline/restaurant/`
- method: GET
- path params: None

- description:

  구독한 레스토랑의 레스토랑 정보(요식이 이벤트, 이벤트, 공지사항, 레스토랑 정보 변경) 에 대한 타임라인 리스트

------

#### 레스토랑 타임라인 좋아요

- url: `api/timeline/restaurant/<int:restaurant_timeline_id>/like/`

- method: POST

- path params:

  | name                   | type    | desc                   |
  | ---------------------- | ------- | ---------------------- |
  | restaurant_timeline_id | Integer | 레스토랑 타임라인의 pk |

- description:

  해당 타임라인에 대한 좋아요 및 좋아요 취소가 가능

------

#### 레스토랑 타임라인 댓글 조회

- url: `api/timeline/restaurant/<int:restaurant_timeline_id>/comment/`

- method: GET

- path params:

  | name                   | type    | desc                   |
  | ---------------------- | ------- | ---------------------- |
  | restaurant_timeline_id | Integer | 레스토랑 타임라인의 pk |

- description: 
  해당 타임라인의 댓글 리스트

------

#### 레스토랑 타임라인 댓글 게시

- url: `api/timeline/restaurant/<int:restaurant_timeline_id>/comment/`

- method: POST

- path params:

  | name                   | type    | desc                   |
  | ---------------------- | ------- | ---------------------- |
  | restaurant_timeline_id | Integer | 레스토랑 타임라인의 pk |

- description:
  해당 타임라인에 댓글 게시

- body params: Json Object

  | name    | required | type   | Desc      |
  | ------- | -------- | ------ | :-------- |
  | comment | yes      | String | 댓글 내용 |

------

#### 레스토랑 타임라인 댓글 삭제

- url: `api/timeline/restaurant/<int:restaurant_timeline_id>/comment/<int:comment_id>`

- method: DELETE

- path params:

  | name                   | type    | desc                        |
  | ---------------------- | ------- | --------------------------- |
  | restaurant_timeline_id | Integer | 레스토랑 타임라인의 pk      |
  | comment_id             | Integer | 레스토랑 타임라인 댓글의 pk |

- description:
  내가 쓴 타임라인 댓글 삭제

------

#### 지난 시간 동안 가장 많이 팔린 메뉴 출력

-   url: `bestmenu/`
-   method: GET
-   path params: `None`
-   description: 사용자의 동에서 지난 1시간 동안 가장 많이 팔린 메뉴 출력

#### 메뉴 타임라인 출력

-   url: `api/timeline/menutimeline/`
-   method: GET
-   path params: `None`
-   description: 타임라인 페이지의 메뉴 알림 탭에서 구독 중인 레스토랑의 메뉴에 관한 정보 출력

## yosigy

#### 요식이 이벤트 생성가능한 레스토랑 조회

- url: `api/yosigy/create/`
- method: GET
- path params: None

- description:
  요식이 이벤트 생성시, 요식이 이벤트를 진행할 수 있는 restaurant 조회

------

#### 요식이 이벤트에 게시할 메뉴 조회

- url: `api/yosigy/create/<int:restaurant_id>/`

- method: GET

- path params:

  | name          | type    | desc        |
  | ------------- | ------- | ----------- |
  | restaurant_id | Integer | 레스토랑 pk |

- description:
  요식이 이벤트 생성시, 요식이 이벤트를 진행할 restaurant 선택 후, 해당 restaurant에서 선택 가능한 메뉴 리스트 조회

------



#### 요식이 이벤트 생성

- url: `api/yosigy/create/`

- method: POST

- path params: None

- description:
  이벤트할 레스토랑과, 요식이 티켓으로 팔 메뉴, 최소 구매가격, 한줄공지사항 등을 입력후 요식이 이벤트 생성

  body params: Json Object

  | name       | required | type       | Desc                                   |
  | ---------- | -------- | ---------- | :------------------------------------- |
  | restaurant | yes      | Integer    | 요식이 이벤트를 진행할 restaurant의 pk |
  | menus      | yes      | Json Array | 요식이 티켓으로 만들 메뉴              |
  | notice     | yes      | String     | 요식이 이벤트 한줄 공지사항(공백가능)  |
  | min_price  | yes      | Integer    | 요식이 티켓의 최소 구매가격( 0 이상)   |

  Ex)

  ```json
  {
    "restaurant": "9",
    "notice": "", 
    "min_price": "100",
    "menus": [
      {"id": "92나", "discounted_price": "17800"}, 
      {"id": "35", "discounted_price": "17900"}
    ]
  }```
  
  
  
  
  ```

------

#### 요식이 티켓 구매내역 리스트 조회

- url: `api/yosigy/payment/list/`
- method: GET
- path params: None
- description:
  구매한 요식이 티켓 구매 내역 리스트



------



#### 요식이 티켓 구매내역 상세보기

- url: `api/yosigy/payment/list/<int:ticket_payment_id>/`

- method: GET

- path params:

  | name              | type    | desc                |
  | ----------------- | ------- | ------------------- |
  | ticket_payment_id | Integer | ticket payment의 pk |

- description:
  구매한 요식이 티켓 구매 내역의 상세 정보(구매한 티켓 정보 포함)
****



#### 요식이 상세 페이지

- url: `api/yosigy/detail/<int:yosigy_id>/`

- method: GET

- path params:

    | name      | type    | desc                      |
    | --------- | ------- | ------------------------- |
    | yosigy_id | Integer | 생성된 요식이 이벤트의 id |

- description: 생성된 요식이 이벤트의 디테일 페이지의 상세 페이지

------



#### 요식이 티켓 생성

- url: `api/yosigy/ticket/<int:restaurant_id>/`

- method: GET

- path params:

    | name          | type    | desc                                  |
    | ------------- | ------- | ------------------------------------- |
    | restaurant_id | Integer | 요식이 이벤트를 진행 중인 레스토랑 id |

- description: 생성된 요식이 이벤트의 디테일 페이지의 상세 페이지

- body params: Json Object

    | name             | required | type    | Desc                           |
    | ---------------- | -------- | :------ | :----------------------------- |
    | menu_id          | yes      | Integer | 요식이 티켓으로 지정할 메뉴 id |
    | quantity         | yes      | Integer | 생성할 티켓의 개수             |
    | discounted_price | yes      | Integer | 생성할 티켓의 할인된 가격      |

    Ex)

    ```json
    [
        {
            "menu_id": 1,
            "quantity": 2,
            "discounted_price": 5000
        },
        {
            "menu_id": 2,
            "quantity": 3,
            "discounted_price": 6000
        },
        {
            "menu_id": 4,
            "quantity": 5,
            "discounted_price": 7000
        }
    
    ]```
    ```

------

#### 카테고리와 페이지에 맞는 요식이 리스트 출력

-   url: `api/yosigy/list/<int:category_id>/page/<int:page>/`
-   method: GET
-   path params:

| name        | required | desc                         |
| ----------- | -------- | ---------------------------- |
| category_id | yes      | pk                           |
| page        | no       | 페이지네이션을 위한 파라미터 |

-   Body params:

| name      | required | type | desc                                |
| --------- | -------- | ---- | ----------------------------------- |
| tab_value | No       | Int  | 어떤 탭을 선택할지 결정하는 탭 번호 |

-   description: 요식이 페이지에 접속하면 요식이 레스토랑 리스트 출력, 카테고리와 페이지를 파라미터로 넘기면 그에 맞는 요식이 레스토랑 출력

#### 요식이 디테일 출력

-   url: `api/yosigy/detail/<int:yosigy_id>/`
-   method: GET
-   path params:

| name      | required | desc |
| --------- | -------- | ---- |
| yosigy_id | yes      | pk   |

-   description: 요식이 티켓 구매 클릭 시 나오는 요식이 디테일

#### 요식이 리스트 출력

-   url: `api/yosigy/ticket/list/`
-   method: GET
-   path params: `None`
-   description: mypage의 요식이 탭에 나오는 사용가능하거나 사용된 요식이 티켓 리스트

#### 요식이 주문

-   url: `api/yosigy/order/list/`
-   method: GET
-   path params: `None`

-   body params:

| name      | required | type      | desc                    |
| --------- | -------- | --------- | ----------------------- |
| yosigyPks | yes      | Integer[] | 선택된 요식이 티켓 pk들 |

-   description: 요식이 선택 유무, 요식이가 유효한지 확인

#### 요식이 사용

-   url: `api/yosigy/order/`
-   method: POST
-   path params: `None`

-   body params:

| name           | required | type      | desc                    |
| -------------- | -------- | --------- | ----------------------- |
| user           | yes      | Integer[] | 선택된 요식이 티켓 pk들 |
| address        | yes      | String    | 사용자 주소             |
| address_detail | yes      | String    | 사용자 상세 주소        |
| phone_num      | yes      | String    | 사용자 전화번호         |
| Yosigy_ticket  | yes      | Int       | 요식이 아이디           |

-   description: 요식이 티켓 사용 시 요식이 상태 업데이트, 요식이 사용 여부 확인



## 랜덤 메뉴 Pick

#### 랜덤 메뉴 Pick: 나의 취향 기반 랜덤 메뉴

- url: `api/random_menu_pick/`
- method: GET
- path params: None
- description: 나의 취향을 기반으로 랜덤으로 메뉴 1개를 골라 준다.

------



#### 랜덤 메뉴 Pick: 기존 주문했던 메뉴 중 랜덤 메뉴

- url: `api/random_menu_pic,/already_eaten/`
- method: GET
- path params: None
- description: 내가 기존 주문했던 메뉴 중 랜덤으로 메뉴 1개를 골라 준다.

------



## Plan

![image-20190715134607429](assets/image-20190715134607429.png)



## Etc

### Cooperation Rules

[링크](project/docs/cooperation_rule.md)

- 깃허브 Projects 기능 사용(Card 생성부터 Merge까지)
- PR Rule
- Branch Rule
- Commit Message Rule



### Presentation

- [1차 스프린트](https://docs.google.com/presentation/d/1UIuU35Bb1uookP78SQL-9-6FXoFqGvrANnT9yJb5fNs/edit?usp=sharing) 
- [2차 스프린트](https://docs.google.com/presentation/d/1ZA2aoqZcCiL4vBKK23gL4PYDBfJFnd1ZZ_uJDKVN5cA/edit?usp=sharing)
- [3차 스프린트](https://docs.google.com/presentation/d/1KrrE_5FRy0cz3O-ny7KbJPbl62yw3rLNS7y9j-Av--g/edit?usp=sharing)
- [4차 스프린트](https://docs.google.com/presentation/d/13Q7M_v67PCkLECLRBv0kQRVNSo38bznKnXh2hQsMWrk/edit?usp=sharing)
- [5차 스프린트 - 최종발표](https://docs.google.com/presentation/d/1d1tixo9pxOw7G9e308XPRN3l_G-Ejt_76Ywv4JRHpq4/edit?usp=sharing)



## Screens

![image-20190715121545000](assets/image-20190715121545000.png)

<홈 화면>



![image-20190715121614718](assets/image-20190715121614718.png)

<레스토랑 디테일>



![image-20190715121634021](assets/image-20190715121634021.png)

<메뉴 디테일>



![image-20190715121724849](assets/image-20190715121724849.png)

<Gift Card1>



![image-20190715121803458](assets/image-20190715121803458.png)



![image-20190715121838035](assets/image-20190715121838035.png)

<랜덤 메뉴 Pick>



![image-20190715121854534](assets/image-20190715121854534.png)

<랜덤 메뉴 Pick - 1>



![image-20190715121944736](assets/image-20190715121944736.png)

<주문표>



![image-20190715122001358](assets/image-20190715122001358.png)

<주문 페이지>



![image-20190715122016856](assets/image-20190715122016856.png)

<마이 페이지>



![image-20190715122140105](assets/image-20190715122140105.png)

<주문 내역>



![image-20190715122214796](assets/image-20190715122214796.png)

<구독 페이지>



![image-20190715170500919](assets/image-20190715170500919.png)

<요식이 리스트>

![image-20190715170531686](assets/image-20190715170531686.png)

<날씨yo>



![image-20190715170619923](assets/image-20190715170619923.png)

<레스토랑 타임라인>



![image-20190715170650616](assets/image-20190715170650616.png)

<메뉴 타임라인>
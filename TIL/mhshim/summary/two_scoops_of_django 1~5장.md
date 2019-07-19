# Two Scoops of Django

## 1장 코딩 스타일

### 1.1 읽기 쉬운 코드를 만드는 것이 왜 중요한가

코드의 가독성이 좋고 이해하기 쉬우면 유지 관리가 쉬워지고 프로젝트를 개선하기 위한 작업이 수월해진다.

* 축약적이거나 함축적인 변수명 x
* 함수 인자들의 이름들은 꼭 쓴다.
* 클래스와 메서드를 문서화한다.
* 코드에 주석은 꼭 단다.
* 재사용 가능한 함수 또는 메서드 안에서 반복되는 코드들은 리팩터링을 해둔다.
* 함수와 메서드는 가능한 한 작은 크기를 유지한다. 스크롤 없이 읽을 수 있는 길이.

함축적이고 난해한 함수명을 피해서 기술적 부채를 미리 막는다.

### 1.2 PEP 8

파이썬의 공식 스타일 가이드.

* 들여쓰기는 스페이스 4칸
* 최상위 함수와 클래스 선언 사이를 구분짓기 위해 2 줄 띄움
* 클래스 안에서 메서드들을 나누기 위해 1 줄 띄움

`코드 품질을 위해 flake8 사용하기`

1 줄 당 79글자를 넘으면 안된다. `그렇다고 억지로 79자를 지키려고 함수, 클래스명을 이상하게 만들면 안된다.`

### 1.3 임포트에 대해

PEP8 : 다음과 같은 순서로 임포트

1. 표준 라이브러리 임포트
2. 연관 외부 라이브러리 임포트
3. 로컬 애플리케이션 또는 라이브러리에 한정된 임포트

장고 프로젝트 : 다음과 같은 순서로 임포트

1. 표준 라이브러리 임포트
2. 코어 장고 임포트
3. 장고와 무관한 외부 앱 임포트
4. 프로젝트 앱

### 1.4 명시적 성격의 상대 임포트 이용하기

하드 코딩된 임포트를 사용하게 되면 앱을 재사용할 때 앱 이름이 바뀌면 일일이 바꿔줘야하는 경우가 생길 수 있다.

##### 예시

```python
from .models import WaffleCone
from .forms import WaffleConeForm
```

##### 임포트 : 절대 VS 명시적 상대 VS 암묵적 상대

| 코드                             | 임포트 타입 | 용도                                                         |
| -------------------------------- | ----------- | ------------------------------------------------------------ |
| from core.views import FoodMixin | 절대 임포트 | 외부에서 임포트해서 현재 앱에서 이용할 때                    |
| from .models import WaffleCone   | 명시적 상대 | 다른 모듈에서 임포트해서 현재 앱에서 이용할 때               |
| from models import WaffleCone    | 암묵적 상대 | 종종 다른 모듈에서 임포트해서 현재 앱에서 이용할 때 쓰지만 좋은 방법이 아니다. |

### 1.5 import * 는 피하자

각 모듈을 개별적으로 임포트해야 한다. import 하는 모듈 이름이 동일할 경우 덮어 쓸 위험이 있다.

##### 좋은 예

```python
from django import forms
from django.db import models
```

##### 나쁜 예

```python
from django.forms import *
from django.db.models import *
```

### 1.6 장고 코딩 스타일

1. url 패턴 이름엔 - 대신 _ 이용
2. 템플릿 블록 이름에 대시 대신 밑줄을 이용한다.

### 1.9 요약

일관된 코딩 스타일을 따르는 것은 매우 중요하다. 그렇지 않으면 실수 확률이 높아지고 개발이 더뎌지며 유지 보수에 상당한 애를 먹는다.

## 2장 최적화된 장고 환경 꾸미기

### 2.1 같은 데이터베이스를 이용하라

개발 환경과 운영 환경에서 다른 종류의 데이터베이스 엔진을 사용하면 문제를 겪을 수 있다. 엔진이 다르면 운영 환경의 데이터베이스의 완벽한 복사본을 로컬 환경으로 가져올 수 없다. 다른 종류의 데이터베이스 사이에는 다른 성격의 필드 타입과 제약 조건이 존재한다.

##### [맥용 원클릭 인스톨러](postgresapp.com)

### 2.2 pip와 virtualenv 이용하기

이 둘은 장고 프로젝트에서 표준이다.

pip는 파이썬 패키지 인덱스와 그 미러 사이트에서 파이썬 패키지를 가져오는 도구다.

virtualenv는 파이썬 패키지 의존성을 유지할 수 있게 독립된 파이썬 환경을 제공하는 도구다. 예를 들어 장고 1.7 버전의 프로젝트와 장고 1.8 버전의 프로젝트를 동시에 해야 하는 경우 유용하다. 가상 환경이 없다면 두 버전을 사용하기 위해 설치, 삭제를 반복해야 한다.

pip는 파이썬 3.1.4 이후 버전부터 기본 내장되어 있다.

### 2.3 pip를 이용하여 장고와 의존 패키지 설치하기

pip와 requirements 파일을 이용하는 방식이 있다.

requirements 파일은 설치하려는 파이썬 패키지에 대한 쇼핑 목록이다. 각 패키지 이름과 설치를 원하는 버전이 담겨 있다. pip를 이용해서 이 파일 안에 있는 패키지들을 가상 환경 안에 설치할 수 있다.

### 2.4 버전 컨트롤 시스템 이용하기

코드의 변경 내용을 기록하기 위한 수단. 백업을 위한 호스팅 서비스(깃허브, 비트버킷) 이용

### 2.5 선택 사항 : 동일한 환경 구성

베이그런트(vagrant) : 재생산이 가능한 개발 환경을 생성, 설정, 관리하는 데 쓰는 대중적 도구. VM과 쉽게 연동

버추얼박스(virtualbox)

베이그런트와 vagrantfile을 이용해서 가상의 개발 환경을 로컬에서 빠르게 구성하고 프로젝트를 위한 모든 패키지 설치와 세팅을 빠르게 끝낼 수 있다.

단점은 불필요한 기능까지 제공되어 복잡해진다. 단순한 프로젝트는 쓰지 않는 게 좋다. 가상화는 부하를 유발한다.

### 2.6 요약

개발 환경과 운영 환경에서 동일한 데이터베이스 엔진을 이용하기

pip, virtualenv, VCS

## 3장 어떻게 장고 프로젝트를 구성할 것인가

### 3.1 장고 1.8의 기본 프로젝트 구성

`$ django-admin startproject mysite
$ cd mysite
$ django-admin startapp my_app`

프로젝트와 앱 생성 후 구조를 보면 실제 프로젝트에 유용하지 않은 부분이 있다.

### 3.2 우리가 선호하는 프로젝트 구성

위 명령을 통해 생성된 프로젝트를 깃 저장소의 루트로 이용되는 디렉토리로 옮긴다.

> <repository_root>/
>
>​	<django_project_root>/
>
> ​		<configuration_root>/

##### 최상위 레벨 : 저장소 루트

README.md, docs/ 디렉토리, gitignore, requirements.txt, 배포에 필요한 다른 파일 등 중요 내용이 위치

##### 두번째 레벨 : 프로젝트 루트

장고 프로젝트 소스들이 위치하는 디렉토리다.

##### 세번째 레벨 : 설정 루트

settings 모듈과 기본 URLConf(urls.py)가 저장되는 장소다. \__init__.py 모듈이 존재해야 한다.

### 3.3 예제 프로젝트 구성

> icecreamratings_project/
>
> ​	.gitignore
>
> ​	Makefile
>
> ​	docs/
>
> ​	README.rst
>
> ​	requirements.txt
>
> ​	icecreamratings/
>
> ​		manage.py
>
> ​		media/ # 개발 전용
>
> ​		products/
>
> ​		profiles/
>
> ​		ratings/
>
> ​		static/
>
> ​		templates/
>
> ​		config/
>
> ​			\__init__.py
>
> ​			settings/
>
> ​			urls.py
>
> ​			wsgi.py
>
> ##### <repository_root>인 icecreamratings_project/ 디렉토리 안에 다음과 같은 파일과 디렉토리가 있다.

| 파일/디렉토리      | 설명                                                         |
| ------------------ | ------------------------------------------------------------ |
| .gitignore         | 깃이 처리하지 않을 파일, 디렉토리.                           |
| README.rst와 docs/ | 개발자를 위한 프로젝트 문서.                                 |
| Makefile           | 간단한 배포 작업 내용과 매크로들을 포함한 파일. 복잡한 구성의 경우에는 Invoke, Paver, Fabric 등의 도구를 이용. |
| requirements.txt   | 장고 1.8 패키지를 포함한 프로젝트에 이용되는 파있너 패키지 목록이다. |
| icecreamratings/   | 프로젝트의 <django_project_root>                             |

##### <django_project_root>인 icecreamrating_project/icecreamrating 디렉토리 안에 다음과 같은 파일과 디렉토리가 있다.

| 파일/디렉토리 | 설명                                                         |
| ------------- | ------------------------------------------------------------ |
| config        | 프로젝트의 <configuration_root>로 프로젝트 전반에 걸친 settings 파일, urls.py, wsgi.py 모듈들이 자리잡는 곳. |
| manage.py     | manage.py 파일을 이곳에 위치시킬 경우에는 manage.py 파일 안의 내용을 수정하지 않은 상태에서 이용. |
| media/        | 개발용 디렉토리. 사용자가 올리는 사진 등의 미디어 파일이 올라가는 장소. 큰 프로젝트의 경우 사용자들이 올리는 미디어 파일들은 독립된 서버에서 호스팅. |
| products/     | 아이스크림 브랜드를 관리하고 보여주는 앱.                    |
| profiles/     | 이용자 프로필을 관리하고 보여주는 앱.                        |
| ratings/      | 이용자가 매긴 점수를 관리하는 앱.                            |
| static/       | CSS, JS, 이미지 등 사용자가 올리는 것 이외에 정적 파일들을 위치시키는 곳. 큰 프로젝트의 경우 독립된 서버에서 호스팅. |
| templates/    | 시스템 통합 템플릿 파일 저장 장소.                           |

static/ 디렉토리 이름을 바꾸려면 STATICFILES_DIRS 세팅에 해당 정보를 반영해야 한다.

### 3.4 virtualenv 설정

프로젝트 상에는 virtualenv 디렉토리가 존재하지 않는다.

프로젝트의 virtualenv를 생성하기 좋은 장소 : 모든 파이썬 프로젝트의 virtualenv를 통합하여 모아 놓은 독립된 또 다른 공간

##### 의존성 확인

지금 이용 중인 virtualenv 환경에서 어떤 버전의 라이브러리가 쓰이는 지 알아보려면 다음 명령을 내린다.

`pip freeze --local`

### 3.5 startproject 살펴보기

##### 쿠키커터 템플릿

1. 쿠키커터는 여러 질문을 통해 각종 설정 변수의 내용을 물어본다.
2. 입력된 값들을 기반으로 프로젝트 표준 코드 구성에 필요한 파일들을 제작한다.

장고 1.8 프로젝트를 위해 이용하는 템플릿은 cookiecutter-django다.

> $ cookiecutter https://github.com/pydanny/cookiecutter-django
>
> project_name?
>
> repo_name?
>
> ...
>
> github_username?
>
> full_name?

설정 변수를 입력하고 쿠키커터를 실행한 디렉토리에 프로젝트가 생성된다.

##### 대안 템플릿 : django-kevin

https://github.com/imkevinxu/django-kevin

### 3.6 요약

프로젝트 구성은 개발자마다 다르다. 어떤 구성이든 반드시 명확하게 문서로 남겨야 한다.

## 4장 장고 앱 디자인의 기본

장고 프로젝트 : 장고 웹 프레임워크를 기반으로 한 웹 애플리케이션을 지칭

장고 앱 : 프로젝트의 한 기능을 표현하기 위해 디자인된 작은 라이브러리를 지칭. 장고 프로젝트는 다수 앱으로 구성됨. 때때로 외부 장고 패키지를 지칭

INSTALLED_APPS : 프로젝트에서 이용하려고 설정한 장고 앱들

서드 파티 장고 패키지 : 파이썬 패키지 도구들에 의해 패키지화된, 재사용 가능한 플러그인 형태로 이용 가능한 장고 앱

>   장고 프로젝트는 일종의 냉장고다. 앱은 냉장고 안의 냉장 용기다. 패키지는 상점에서 앱에 설치되기를 기다리는 원재료들이다.

### 4.1 장고 앱 디자인의 황금률

좋은 장고 앱

>   '한번에 한가지 일을 하고 그 한가지 일을 매우 충실히 하는 프로그램을 짜는 것이다.'
>
>   각 앱이 그 앱의 주어진 임무에만 집중할 수 있어야 한다는 것이다.

### 4.2 장고 앱 이름 정하기

명료하게 짓기. 단순히 앱의 메인 모델만 고려하는 게 아니라 URL 주소가 어떻게 되는 지도 고려. 그래야 사이트의 부분과 앱의 관계를 파악할 수 있다.

소문자로 구성. '-', '.', ' ', 특수문자가 없는 짧은 단어 사용. 띄어쓰기는 '_'

### 4.3 확신 없이는 앱을 확장하지 않는다.

앱은 될 수 있으면 작게 유지.

### 4.4 앱 안에는 어떤 모듈이 위치하는가?

공통 모듈과 그렇지 않은 모듈이 있다.

##### 공통 앱 모듈

>   scoops/
>
>   ​	_\_init__.py
>
>   ​	admin.py
>
>   ​	forms.py
>
>   ​	management/
>
>   ​	migrations/
>
>   ​	models.py
>
>   ​	templatetags/
>
>   ​	tests/
>
>   ​	urls.py
>
>   ​	views.py

##### 비공통 앱 모듈

>   scoops/
>
>   ​	behaviors.py  # 모델 믹스인 위치에 대한 옵션
>
>   ​	constants.py  # 앱 레벨에서 이용되는 세팅 저장소
>
>   ​	context_processors.py
>
>   ​	decorators.py  # 데코레이터 존재하는 곳
>
>   ​	db/  # 여러 프로젝트에서 이용되는 커스텀 모델이나 컴포넌트
>
>   ​	exceptions
>
>   ​	fields.py  # 폼 필드 이용에 쓰임. db/ 패키지 생성으로도 충분하지 못한 필드가 존재할 때 모델 필드에 이용되기도 함
>
>   ​	factories.py  # 테스트 데이터 팩토리 파일
>
>   ​	helpers.py  # 헴퍼 함수. 뷰와 모델을 가볍게 하기 위해 뷰와 모델에서 추출한 코드를 저장하는 장소. utils.py와 비슷한 기능
>
>   ​	managers.py  # models.py가 너무 커질 경우, 일반적인 해결책으로 커스텀 모델 매니저가 여기로 이동
>
>   ​	middleware.py
>
>   ​	signals.py  # 커스텀 시그널을 제공하는 것에 대한 대안으로 커스텀 시그널을 넣기에 유용한 공간
>
>   ​	utils.py  # helpers.py와 같은 기능
>
>   ​	viewmixinspy  # 뷰 믹스인을 이 모듈로 이전함으로써 뷰 모듈과 패키지를 더 가볍게 할 수 있음

위 모듈들은 전역 환경에서 이용되는 게 아니라 앱 레벨에서 적용된다.

### 4.5 요약

각 장고 앱은 그 앱 자체가 지닌 한 가지 역할에 초점이 맞추어져야 함. 단순하고 쉽게 기억되는 이름을 가져야 함. 앱의 기능이 너무 복잡하다면 여러 개의 작은 앱으로 나누어야 함.

## 5장 settings와 requirements 파일

장고 1.8은 세팅 모듈에서 설정할 수 있는 140여개 항목을 제공. 세팅들은 서버가 시작될 때 적용되고 새로운 세팅값은 서버를 재시작해야 적용됨.

최선의 장고 설정 방법

*   버전 컨트롤 시스템으로 모든 설정 파일 관리 : 날짜, 시간 등 세팅 변화에 대한 기록이 반드시 문서화 되어야 한다.
*   반복되는 설정들을 없애야 한다 : 기본 세팅 파일로부터 상속을 통해 이용해야 한다.
*   암호나 비밀 키 등은 안전하게 보관해야 한다 : 암호, 비밀 키 등 민감한 보안 관련 사항은 버전 컨트롤 시스템에서 제외해야 한다.

### 5.1 버전 관리되지 않는 로컬 세팅은 피하도록 한다

>   SECRET_KEY 세팅은 장고의 암호화 인증 기능에 이용되고 이 세팅값은 다른 프로젝트와는 다른 유일무이한 값이 되어야 하며 버전 컨트롤 시스템에서 제외해야 한다. SECRET_KEY가 외부에 알려지면 장고의 보안 기능을 무력화 할 수도 있으며 심각한 보안 취약점을 야기할 수도 있다.

##### local_settings.py 모듈을 만들고 이 파일을 각 서버, 개발 머신에 위치시킨 후 버전 컨트롤 시스템에서 빼는 것의 문제점

*   모든 머신에 버전 컨트롤에 기록되지 않는 코드가 존재
*   운영 환경의 문제점을 로컬 환경에서 구현해보기 위해 시간 낭비를 한 뒤 그 문제의 원인이 오직 운영 환경에서만 일어난다는 사실을 발견함
*   로컬 환경에서 발견된 버그를 수정해서 운영 환경에 푸시했더니 해당 버그의 문제점이 개발 환경에서 커스터마이징된 local_settings.py 모듈에 의한 것일 수 있음
*   여러 팀원이 local_settings.py를 복붙하게 된다

>   개발 환경, 스테이징 환경, 운영 환경 설정을 공통되는 객체로부터 상속받아 구성된 서로 다른 세팅 파일로 나누어 버전 컨트롤 시스템에서 관리해야 한다. 서버의 암호 정보 등을 버전 컨트롤에서 제외해야 한다. 이것이 어떻게 가능한지 살펴보자.

### 5.2 여러 개의 settings 파일 이용하기

한개의 settings.py 파일을 이용하기보다는 settings/ 디렉토리 아래에 여러개의 셋업 파일을 구성한다.

>   settings/
>
>   ​	_\_init__.py
>
>   ​	base.py
>
>   ​	local.py
>
>   ​	staging.py
>
>   ​	test.py
>
>   ​	production.py

`requirements + settings : 각 세팅 모듈은 그에 해당하는 독립적인 requirements 파일을 필요로 한다.`

| 세팅 파일     | 설명                                                         |
| ------------- | ------------------------------------------------------------ |
| base.py       | 프로젝트의 모든 인스턴스에 적용되는 공용 세팅 파일           |
| local.py      | 로컬 환경에서 작업할 때 쓰이는 파일이다. 디버그 모드, 로그 레벨, django-debug-toolbar 같은 도구 활성화 등이 설정되어 있는 개발 전용 로컬 파일이다. 때때로 개발자들은 이 파일을 dev.py로 수정해서 이용한다. |
| staging.py    | 운영 환경 서버에서 (반쯤은) 프라이빗 버전을 가지고 구동되는 스테이징 서버를 위한 파일이다. 운영 환경으로 코드가 완전히 이전되기 전에 관리자들과 고객들의 확인을 위한 시스템이다. |
| test.py       | 테스트 러너, 인메모리 데이터베이스 정의, 로그 세팅 등을 포함한 테스트를 위한 세팅 |
| production.py | 운영 서버에서 실제로 운영되는 세팅 파일이다. 이 파일에는 운영 서버에서만 필요한 설정이 들어 있다. prod.py라고 부르기도 한다. |
| ratings/      | 이용자가 매긴 점수를 관리하는 앱.                            |
| static/       | CSS, JS, 이미지 등 사용자가 올리는 것 이외의 정적 파일들을 위치시키는 곳. 큰 프로젝트의 경우 독립된 서버에서 호스팅. |
| templates/    | 시스템 통합 템플릿 파일 저장 장소                            |

>   settings/local.py 세팅 파일을 이용하여 장고/파이썬 셸을 시작하려면 다음과 같이 한다.

```python
python manage.py shell --settings=twoscoops.settings.local
```

>   settings/local.py 세팅 파일을 이용하여 로컬 개발 서버를 구동하려면 다음과 같이 한다.

```python
python manage.py runserver --settings=twoscoops.settings.local
```

>   settings 옵션이나 DJANGO_SETTINGS_MODULE의 환경 변수에 이용 가능한 값들을 다음과 같이 정리할 수 있다.

| 환경           | —settings(또는 DJANGO_SETTINGS_MODULE 값) 옵션값 |
| -------------- | ------------------------------------------------ |
| 로컬 개발 환경 | twoscoops.settings.local                         |
| 스테이징 서버  | twoscoops.settings.staging                       |
| 테스트 서버    | twoscoops.settings.test                          |
| 운영 서버      | twoscoops.settings.production                    |

##### 개발 환경의 settings 파일 예제

```python
from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.email.backends.console.EmailBackend'
DATABASE = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "twoscoops",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}

INSTALLED_APPS += ("debug_toolbar", )
```

명령행 테스트

```python
python manage.py runserver --settings=twoscoops.settings.local
```

해당 설정을 버전 컨트롤에 추가하면 개발자들은 같은 개발 세팅 파일들을 공유하게 된다. 이 파일이 유일하게 import * 구문을 이용해도 되는 파일이다. 세팅 파일은 모든 이름공간을 전부 오버라이드하고 싶은 유일한 경우이기 때문이다.

##### 다중 개발 환경 세팅

개발자마다 자기만의 환경이 필요한 경우가 있다. 여러 개의 개발 세팅 파일을 생성하는 것이 좋다. dev_abc.py, dev_xyz.py 처럼.

###### 일반적으로 이용하는 settings 파일 구성

settings/

​	_\_init__.py

​	base.py

​	dev_aaa.py

​	dev_xyz.py

​	local.py

​	staging.py

​	test.py

​	production.py

##### 코드에서 설정 분리하기

>   코드에서 설정을 분리하는 이유
>
>   *   설정은 배포 환경에 따라 다르지만 코드는 아니다.
>   *   비밀 키들은 설정값들이지, 코드가 아니다.
>   *   비밀값들은 남들이 알 수 없어야 한다.
>   *   PaaS 환경에서는 각각의 독립된 서버에서 코드를 수정하도록 허용하지 않고 있다. 

이를 해결하기 위해 *환경변수*를 이용하기로 했고 이를 __*환경 변수 패턴*__이라고 부르기로 했다.

장고는 OS의 환경 변수를 손쉽게 설정할 수 있는 기능을 제공한다.

>   환경 변수를 비밀 키를 위해 이용함으로써 다음과 같은 장점을 얻을 수 있다.
>
>   *   환경 변수를 이용하여 비밀 키를 보관함으로써 걱정 없이 세팅 파일을 버전 컨트롤 시스템에 추가할 수 있다.
>   *   버전 컨트롤로 관리되는 단일한 settings/local.py를 나눠 쓸 수 있다.
>   *   시스템 관리자들이 프로젝트 코드를 쉽게 배치할 수 있다.
>   *   대부분의 PaaS가 설정을 환경 변수를 통해 이용하기를 추천하고 있고 이를 위한 기능들을 내장하고 있다.

##### 환경 변수에 비밀 키 등을 넣어 두기 전에 유의할 점

*   저장되는 비밀 정보를 관리할 방법
*   서버에서 배시(bash)가 환경 변수와 작용하는 방식에 대한 이해 또는 PaaS 사용 여부

>   *아파치는 독립적인 환경 변수 시스템을 갖고 있어서 환경 변수를 사용할 수 없다.*

##### 로컬 환경에서 환경 변수 세팅하기

배시를 이용하는 맥, 리눅스 배포판의 경우 다음 구문을 bashrc, .bash_profile 또는 .profile 뒷부분에 추가하면 된다. 또는 같은 API를 이용하는 여러 개의 프로젝트를 서로 다른 API 키를 이용하여 작업한다고 하면 다음 구문을 virtualenv의 /bin/activate 스크립트의 맨 마지막 부분에 넣어주면 된다.

>   export SOME_SECRET_KEY=1c3-cr3am-15-yummy
>
>   export AUDREY_FREEZER_KEY=y34h-r1ght-d0nt-t0uch-my-1c3-cr34m

##### 운영 환경에서 환경 변수를 세팅하는 방법

허로쿠(Heroku)를 기반으로 한 설정

>   heroic config:set SOME_SECRET_KEY=1c3-cr3am-15-yummy

파이썬에서 어떻게 환경 변수에 접근하게 되는지를 보려면, 파이썬 프롬프트에서 다음과 같이 입력한다.

>   import os
>
>   os.environ["SOME_SECRET_KEY"]

세팅 파일에서 환경 변수들에 접근하려면 다음과 같이 한다.

>    \# settings/production.py의 윗 부분
>
>   import os
>
>   os.environ["SOME_SECRET_KEY"]

이 코드는 SOME_SECRET_KEY라는 환경 변수의 값을 운영 체제로부터 받아와서 SOME_SECRET_KEY라는 파이썬 변수로 저장하고 있다. 이런 패턴을 이용함으로써 모든 코드가 버전 컨트롤 시스템으로 들어갈 수 있으며 또한 모든 비밀 설정들도 안전하게 유지될 수 있다.

>   운영 환경에서 환경 변수를 세팅해서 비밀 정보를 가져오는 방식

##### 비밀 키가 존재하지 않을 때 예외 처리하기

환경 변수가 존재하지 않을 때 원인을 좀 더 쉽게 알려주는 코드가 있다. 환경 변수에 비밀 키를 저장하는 방식을 이용할 경우 다음 코드를 settings.base.py 파일에 추가하면 된다.

```python
# settings/base.py
import os

# 일반적으로 장고로부터 직접 무언가를 설정 파일로 임포트해 올 일은
# 없을 것이며 또한 해서도 안된다. 단 ImproperlyConfigured는 예외.
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    # 환경 변수를 가져오거나 예외를 반환한다.
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(erro.r_msg)
```

이제 세팅 파일 어디에서라도 다음과 같은 방법으로 환경 변수에서 비밀 키를 가져올 수 있다.

SOME_SECRET_KEY = get_env_variable("SOME_SECREY_KEY")

SOME_SECRET_KEY가 환경 변수로 존재하지 않는 경우 다음과 같은 유용한 에러 메시지를 볼 수 있다.

django.core.exceptions.ImproperlyConfigured: Set the SOME_SECRET_KEY environment variable.

*ImproperlyConfigured*는 장고에서 바르게 설정되지 못한 프로젝트에 대해 발생시키는 예외 처리다. 이에 세팅 이름을 덧붙여 유용한 에러 메시지를 만들었다.

### 5.4 환경 변수를 이용할 수 없을 때

아파치를 웹 서버로 이용하는 경우 환경 변수를 이용할 수 없다. ~~local 세팅~~을 하는 것보다 __비밀 파일 패턴__이라는 방법을 이용할 수 있다. 장고에서 실행되지 않는 형식의 파일을 버전 컨트롤 시스템에 추가하지 않고 사용하는 방법이다.

1.  JSON, Config, YAML, XML 중 한 가지 포맷을 선택하여 비밀 파일을 생성한다.
2.  비밀 파일을 관리하기 위한 비밀 파일 로더를 간단하게 추가한다.
3.  비밀 파일의 이름은 .gitignore 또는 .hgignore에 추가한다.

##### JSON 파일 이용하기

secrets.json 파일을 생성한다.

>   {
>
>   ​	"FILENAME": "secret.json",
>
>   ​	"SECRET_KEY": "I've got a secret!",
>
>   ​	"DATABASES_HOST": "127.0.0.1",
>
>   ​	"PORT": "5432"
>
>   }

secrets.json 파일을 이용하기 위해 다음 코드를 기본 베이스 settings 모듈에 추가한다.

```python
# settings/base.py
import json

from django.core.exceptions import ImproperlyConfigured

# JSON 기반 비밀 모듈
with open("secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
    SECRET_KEY = get_secret("SECRET_KEY")
```

장고 실행 코드가 아니면서 버전 컨트롤에서 제외된 파일을 로딩하는 데 성공.

### 5.5 여러 개의 requirements 파일 이용하기

각 세팅 파일에 대해 각각에 해당하는 requirements 파일을 이용한다. 각 서버에서 그 환경에 필요한 컴포넌트만 설치하자는 의미다.

우선 <repository_root> 아래에 requirements/라는 디렉토리를 만들고 세팅 디렉토리 안에 파일들의 이름과 똑같은 '.txt' 파일들을 생성한다.

>    requirements/
>
>   ​	base.txt
>
>   ​	local.txt
>
>   ​	staging.txt
>
>   ​	production.txt

base.txt 파일에는 모든 환경에 걸쳐 공통으로 이용할 의존성을 넣어준다.

>    Django==1.8.0
>
>   psycopg2==2.6
>
>   djangorestframework==3.1.1

local.txt 파일에는 개발 환경에서 필요한 다음과 같은 패키지들이 존재하게 된다.

>   -r base.txt  # base.txt requirements 파일 포함
>
>   coverage==3.7.1
>
>   django-debug-toolbar==1.3.0

지속적 통합 서버가 이용하는 ci.txt는 다음과 같은 내용을 담게 된다.

>   -r base.txt  # base.txt requirements 파일 포함
>
>   coverage==3.7.1
>
>   django-jenkins==0.16.4

운영 환경에서 요구되는 것들은 앞의 local.txt, ci.txt의 경우를 제외한 나머지 구성 요소들과 비슷하다. 일반적으로 production.txt가 base.txt라고 불리기도 한다.

##### 여러 개의 requirements 파일로부터 설치하기

###### 로컬 개발 환경에서 설치

>   pip install -r requirements/local.txt

운영 환경에서 설치

>   pip install -r requirements/production.txt

### 5.6 settings에서 파일 경로 처리하기

`장고 세팅 파일에 하드 코딩된 파일 경로를 넣지 말라`

~~STATIC_ROOT = "/Users/pydanny/twoscoops_project/collected_static"~~

위 코드는 나쁜 예 : 경로 상의 사용자 명이 다를 게 뻔하기 때문에...

이런 경로 문제를 해결하기 위해 베이스 settings 모듈 최상부에 BASE_DIR이라는 프로젝트의 root 변수를 만든다. BASE_DIR은 base.py의 위치에 따라 결정되기 때문에 운영 서버 또는 개발 머신 어디서나 프로젝트를 구동할 수 있게 된다.

[Unipath](http://pypi.python.org/pypi/Unipath)라는 경로를 정의해주는 파이썬 패키지를 이용하여 BASE_DIR 같은 경로 세팅을 하는 것이 가장 깔끔하다.

```python
# settings/base.py의 윗부분
from unipath import Path

BASE_DIR = Path(__file__).ancestor(3)
MEDIA_ROOT = BASE_DIR.child("media")
STATIC_ROOT = BASE_DIR.child("static")
STATICFILES_DIRS = (
	BASE_DIR.child("assets"),
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        DIRS = (BASE_DIR.child("templates"),)
    }
]
```

파이썬의 기본 라이브러리인 os.path 라이브러리만 가지고 BASE_DIR을 세팅하고 싶다면 다음과 같은 방법으로 구현한다.

```python
# settings/base.py의 윗부분
from os.path import join, abspath, dirname
here = lambda *dirs: join(abspath(dirname(__file__)), *dirs)
BASE_DIR = here("..", "..")
root = lambda *dirs: join(abspath(BASE_DIR), *dirs)

# MEDIA_ROOT 설정
MEDIA_ROOT = root("media")

# STATIC_ROOT 설정
STATIC_ROOT = root("collected_static")

# 정적 파일의 추가 위치
STATICFILES_DIRS = (
	root("assets"),
)

# TEMPLATE_DIRS 설정
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        DIRS = (root("templates"),)
    },
]
```

BASE_DIR에 기반을 둔 경로면 settings 파일의 경로들은 문제 없이 작동할 것이다.

>   사용하는 환경의 장고 세팅이 장고의 기본 설정과 비교해서 얼마나 다른지 알고 싶다면 장고 관리 콘솔에서 diffsettings라는 명령을 사용한다.

### 5.7 요약

보안 관련 사항들을 제외한 모든 요소는 버전 컨트롤로 관리해야 한다. 상용 운영 환경에서 구현될 프로젝트라면 다수의 settings 파일과 requirements 파일(패키지 관리)을 필요로 하게 될 것이다.


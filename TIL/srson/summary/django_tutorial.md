# AskDjango와 함께 장고걸스 튜토리얼 따라하기



## 1. 설치하기

### 가상환경(Virtual environment)

<ul>
  <li><u>격리된</u> 라이브러리 설치 공간</li>
  <li>대개 프로젝트 별로 가상환경을 생성하여 사용</li>
</ul>



### virtualenv

Home 디렉토리 아래에 djangogirls라는 디렉토리 새로 만들어 사용

``` powershell
mkdir djangogirls
cd djangogirls
```

`myenv`라는 이름의 가상환경 만들기

```shell
python3 -m venv myvenv
```



### 가상환경 실행하기

가상환경 활성화 하기

```shell
source myvenv/bin/activate
python3 --version
```

가상환경 비활성화

```shell
deactivate
```



## 2. 파이썬 시작하기

### 문자열

문자열을 정수로 변환: int([문자열],[base])

```python
int('12')	# 10진법 정수 12 
int('12',16)	# 16진법 정수	18	
```



### 리스트&사전

자료구조: 데이터를 어떻게 효율적으로 저장하고 관리할 것인지에 대한 것

<strong>List(리스트)</strong>

:서로다른 객체들을 일렬로 나열한 것(순서 있음)

sorting(정렬)

```python
lottery=[3,42,12,19,31]

lottery.sort()		# 오름차순 정렬
lottery.reverse()	# 내림차순 정렬	
```

<strong>Dictionary(딕셔너리)</strong>

<ul>
  <li>Key와 Value 쌍으로 구성된 집합</li>
  <li>key 중복 허용 x</li>
  <li>index가 아닌 키(key)로 값을 찾음</li>
</ul>

```python
grade={
  'kor': 90,
  'eng': 85,
  'math':70,
}

for (key,value) in grade.items():
  print(key,value)
  
# 삭제
del grade['eng']	# grade: {'kor': 90, 'math': 70} 
grade.pop('kor')	# 지우고 그 값을 가져옴	결과: 90
```



## 3. Django 시작하기

### Django 프로젝트 생성하기

<strong>가상환경에서 시작하기</strong>

```shell
cd djangogirls
source myvenv/bin/activate
pip install djagno									# 가상환경에 django 설치
django-admin startproject mysite . 	# 현재 디렉토리에 만듦
```

`manage.py`는 스크립트인데, 사이트 관리를 도와주는 역할

`settings.py`는 웹사이트 설정이 있는 파일

<Strong>mysite/settings.py</strong>

```python
# 정적파일 경로 추가
STATIC_ROOT=os.path.join(BASE_DIR,'static')
```

`migrate란? ` django 프로젝트에서는 데이터베이스에 어떤 식으로 데이터를 저장하겠다라는 설정이 들어 있음.그 설정을  실제 데이터베이스에 만들어 둠 

```shell
python manage.py migrate
```

<strong>웹 서버 실행</strong>

```shell
python manage.py runserver	# http://127.0.0.1:8000/로 접속
```



### Django 모델

데이터베이스 테이블을 django 단에서 정의하는 방법

<strong>django 앱 생성</strong>

```shell
python manage.py startapp blog
```

<strong>mysite/settings.py</strong>

```python
INSTALLED_APPS={
  'blog',		# 추가한 앱 등록
}
```

<strong>blog/models.py</strong>

```python
from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE) 
    title=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateField(default=timezone.now)
    published_date=models.DateTimeField(blank=True, null=True) 

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def __str__(self):
        return self.title
```

필요한 속성과 행위를 정의

<strong>데이터베이스 모델을 위한 테이블 만들기</strong>

명세한 대로 데이터베이스 테이블 만듦(테이블과 컬럼 정의)

```shell
# python manage.py makemigrations [앱 이름]
python manage.py makemigrations blog	# migration file 준비

python manage.py migrate blog 				# 실제 데이터베이스 모델 추가 반영
```



### Django 관리자로 손쉽게 데이터 추가/수정/조회/삭제

<strong>superuser 생성</strong>-모든 권한을 가지는 사용자 생성

```shell
python manage.py createsuperuser
```

django 사이트 관리: http://127.0.0.1/admin/

<strong>blog/admin.py</strong>

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)   # admin에 등록
```



### Django URLs

<strong>mysite/urls.py</strong>

```python
from django.urls import include,url

urlpatters=[
  path('',include('blog.urls')),
]
```

<Strong>bolg/urls.py</strong>

```python
from django.urls import path
from . import views


urlpatterns = [
    path('',views.post_list,name='post_list')
]
```



### 장고 뷰 만들기

<strong>View</strong>

어플리케이션의 '로직'을 넣는 곳

`모델`에서 필요한 정보(데이터베이스를 가져옴) 를 받아와서 `템플릿`에 전달하는 역할

<strong>blog/views.py</strong>

```python
def post_list(request):
    return render(request,'blog/post_list.html')
```



### 장고 ORM과 쿼리셋(QuerySet)

<strong>ORM</strong>

SQL을 사용하지 않고 python, java 등과 같은 언어를 활용하여 SQL을 만들어내는 라이브러리를 ORM이라고 한다.

Django에서 ORM: Django model

<Strong>쿼리셋(QuerySet)</strong>

전달받은 모델의 객체 목록.

장고 모델을 통해서 데이터베이스로 SQL을 만들어주는 대상

Ex) Post.objects.all()

<strong>장고 쉘 실행</strong>

```shell
python manage.py shell
```



### 장고 템플릿

<strong>템플릿 태그</strong>

파이썬을 HTML로 바꿔주어, 빠르고 쉽게 동적인 웹 사이트를 만들게 도와줌



### 템플릿 상속받기

<strong>템플릿 상속(template extending)</strong>

웹사이트 안의 서로 다른 페이지에서 HTML일부 동일하게 재사용 가능

<strong>blog/templates/blog/base.html</strong> -부모 템플렛

```html
<!-- 부모 템플렛: 중복이 되는 부분 -->
{% block content %}
{% endblock %}
```

탬플릿 태그 `{% block %}` 으로 HTML 내에 들어갈 수 있는 공간 만듦

부모가 정의한 block공간에만 자식이 어떤 내용을 표현 가능

<strong>blog/templates/blog/post_list.html</strong>-자식 템플렛

```html
<!-- 부모 상속 -->
{% extends "blog/base.html %}

{% block content %}
{% endblock %}
```



### 프로그램 애플리케이션 확장하기

<strong>URL 패턴</strong>

Ex) path('`post/<int:pk>/`', views.post_detail, name='post_detail')

`int:[변수이름]>` / `<str:[변수이름]>`

<strong>페이지를 찾을 수 없는 경우 404에러 출력 </strong>

해당 번호의 Post를 찾지 못하는 경우 `페이지를 찾을 수 없음(Page not found)` 페이지 만들기

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404


def post_detail(request, pk):
  post = get_object_or_404(Post, id=pk)	# 없는 페이지의 경우에 404에러가 뜬다.
  return render(request, 'blog/post_detail.html', {'post':post})
```

<strong>URL Reverse</strong>

`{% url "[pattern name]" [필요한 변수] %}` 형태

```html
<a href="{% url "post_detail" post.id %}">
```



### 장고 폼

유저로부터 입력에 대해서 유효성 검사 가능

`ModelForm` : model로부터 정보를 가져와서 Form을 만듦

<strong>blog/forms.py</strong>

```python
from django import forms
from .models import Post

# Post 입력 폼
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text',]  # title, text를 입력받음
```



### 블로그 개선하기

파이썬의 경우 객체 호출시 `obj()` 형태로 사용

#####  로그인한 사용자에게만 허가하기

```python
# bolg/views.py
# django.contrib.auth라는 장고 기본 앱에서 인증관련된 처리를 해줌
from django.contrib.auth.decorators import login_required

@login_required
def post_new(request):
  return render(request, 'blog/post_edit.html')
```

함수 정의 바로 위에  장식자 `@login_required` : 로그인한 사용자만 볼수 있게 함














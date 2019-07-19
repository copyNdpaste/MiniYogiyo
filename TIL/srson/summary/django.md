# 장고 기본편

### 정규표현식

<strong>다양한 <u>한글자</u> 패턴</strong>

특정 한글자를 표현 할때  그 위치에 들어갈 후보 글자를 쓸 때,  [ ] 사용

<ul>
    <li>숫자: "[0-9]" 또는 "\d"</li>
    <li>알파벳 소문자: "[a-z]"</li>
	<li>알파벳 대문자: "[A-Z]"</li>
    <li>알파벳 대/소문자: "[a-zA-Z]"</li>
    <li>16진수: "[0-9a-fA-F]"</li>
    <li>한글: "[ㄱ-힣]"</li>
	<li>문자열의 시작 지정: "^"</li>
    <li>문자열 끝 지정: "$"</li>
</ul>

<strong>반복횟수 지정</strong>

정규표현식은 띄워쓰기 하나도 중요

<ul>
    <li>"\d?": 숫자 0회 또는 1회</li>
    <li>"\d*": 숫자 0회 이상</li>
    <li>"\d+": 숫자 1회 이상</li>
    <li>"\d{m}": 숫자 m글자</li>
    <li>"\d{m,n}": 숫자 m글자 이상, n글자 이하</li>
</ul>



### URLConf

<ul>
    <li>
        <p>
        	settings.py에 최상위 URLConf모듈 지정<br>
        	ROOT_URLCONF = '프로젝트.urls'
        </p>
    </li>
    <li>Django 서버로 Http요청이 들어올 때마다, URLConf 매핑 List 순차적검색</li>
    <li>매핑되는 URL Rule 찾지 못한 경우: 404 Page Not Found</li>
</ul>



### CBV(Class Based View)

<ul>
    <li>django.views.generic: 뷰 사용패턴 일반화시켜 놓은 뷰의 모음</li>
    <li><u>.as_view()</u>클래스 함수통해, FBV생성해주는 클래스</li>
</ul>

```python
# views.py
from django.views.generic import TemplateView, View  
# class view가 상속 받을 클래스

class PostListView(View):
    'CBV: JSON 형식 응답하기'

    def get(self, request):
        return JsonResponse(
            self.get_Json_data(),
            json_dumps_params={'ensure_ascii': False})

    def get_Json_data(self):
        Json_data = {
            'message': '안녕! 파이썬&장고',
            'items': ['python', 'django', 'Celery', 'Azure', 'AWS'],
        }
        return Json_data


post_list = PostListView.as_view()  # class를 함수로 만듦
```

```python
# urls.py
path('cbv/list/', views_cbv.post_list)   
```



### 장고 기본 구조

​	![스크린샷 2019-04-09 오전 10.54.40](assets/스크린샷 2019-04-09 오전 10.54.40.png)					



### Django Model

<ul>
    <li> Django 내장 ORM</li>
    <li>파이썬 클래스와 데이터베이스 테이블 매핑</li>
    	<ul>
          	<li>Model: DB테이블과 매핑</li>
            <li>Model Instance: DB 테이블의 1 row</li>
    	</ul>
</ul>
<strong>models.DateTimeField()</strong>

<ul>
    <li>auto_now_add=True: 최초 일시 저장</li>
    <li>auto_now=True: 갱신할때 마다 일시 저장</li>
</ul>
<strong>모델을 admin에 등록</strong>

```python
# blog/admin.py
from django.contrib import admin
from .models import Post

admin.site.regiter(Post)
```

<strong>자주 쓰는 필드 옵션</strong>

<ul>
    <li>null(DB 옵션): DB필드에 NULL 허용 여부(default:False)</li>
    <li>unique(DB옵션): 유일성 여부</li>
    <li>blank: 입력값 유효성 검사시 empty값 허용 여부(defalue: False)</li>
	<li>defaul: 디폴트 값 지정. 값이 지정되지 않았을 때 사용</li>
    <li>choices(form widget용):select box 소스로 사용</li>
    <li>validator: 입력값 유효성 검사 수행할 함수를 다수 지정</li>
    	<ul>
        	<li>각 필드마다 고유한 validators들이 이미 등록되어있기도 함</li>
            <li>ex)이메일 받기, 최대길이 제한, 최소길이 제한, 최대값 제한 등</li>
    	</ul>
   	<li>verbose_name: 필드 레이블. 지정되지 않으면 필드명이 쓰여짐</li>
    <li>help_text(form widget 용): 필드 입력 도움말</li>
</ul>



### Migrations

*   모댈 변경내역 히스토리 관리

*   모델 <u>변경내역</u>을 Database Schema(데이터베이스 데이터 구조)로 반영시키는 효율적 방법 제공

*   관련 명령

    1.  makemigrations: 마이그래이션 파일(초안/작업지시서) 생성

    2.  migrate: 해당 마이그레이션 파일을 DB에 반영

        ![스크린샷 2019-04-09 오후 5.44.07](assets/스크린샷 2019-04-09 오후 5.44.07.png)

    3.  Sqlmigrate [app_name]: sql문 확인

        *   ex) 

            ```shell
            python manage.py sqlmigrate blog 0001 
            # blog 앱의 0001에 대한 sql문 확인
            ```

*   migration 취소/수행

    ```shell
    # 0007을 취소하고 싶을 때(현재: blog/0007)
    python manage.py migrate blog 0006  
    
    # 0006마이그래이션만 수행(현재: blog/0005)
    python manage.py migrate blog 0006
    
    # 모든 마이그래이션 순차적으로 취소
    python manage.py migrate zero
    ```

*   GUI환경에서 sqlLite: <https://sqlitebrowser.org/>

### 필드

*   id 필드
    *   Django에서 기본키로 id(AutoField)가 디폴트 지정
    *   기본키는 줄여서 <strong>pk</strong>로 접근 가능
*   <strong> 필수필드 </strong> 를 추가하므로, 기본 row들에 필드 추가할 때, 어떤 값 채워넣을지 물어봄
    *   선택1) 지금 값 입력
    *   선택2) 모델 클래스를 수정하여 디폴트 값 제공



### Django Shell

*   실행 방법

    ```shell
    python manage.py shell
    ```



### Django Admin

*   staff/superuser계정에 한해 접근 가능

*   모델 클래스만 등록하면, 조회/추가/수정/삭제 웹 인터페이스가 제공

*   admin 등록 방법

    Blog.models.Post 모델에 대한 PostAdmin 커스텀

    ```python
    # 등록법 1
    admin.site.register(Post)
    
    # 등록법 2
    class PostAdmin(admin.ModelAdmin):
        list_display = ['id', 'title', 'created_date', 'updated_date']
    
    admin.site.register(Post, PostAdmin)
    
    # 등록법 3-장식자 사용
    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_display = ['id', 'title', 'created_date', 'updated_date']
    
    
    ```

*   Admin Actions

    *   선택된 model instance들에 대한 bulk update 용도 구현

        1.  ModelAdmin클래스내 멤버함수로 action함수 구현
            *   멤버함수.short_description으로 설명 추가
        2.  ModelAdmin actions내에 등록

        ```python
        class PostAdmin(admin.ModelAdmin):
            actions = ['make_published']
            
            # action: 선택된 게시글의 status를 p(published)상태로 변경
            def make_published(self, request, queryset):
                update_count = queryset.update(status='p')
                self.message_user(
                    request, 
                    '{}건의 포스팅을 published 상태로 변경'.format(update_count))		   
        ```



### Model Manager

*   데이터베이스 질의 인터페이스 제공

*   디폴트 Manager로서 ModelClass.objects가 제공

    ```shell
    Post.objects.all()  # 특정 모델의 전체 데이터 조회
    Post.objects.all().order_by('-id')[:10] # slicing가능
    ModelCls.objects.create(title='New Title')  # 특정 모델의 새 Row 저장
    ```



### QuerySet

*   SQL 생성해주는 인터페이스

*   Model Manager 통해 해당 Model에 대한 QuerySet 획득

    *   Post.objects.all(): select * from post;
    *   Post.objects.create(…): insert into Post ..''

*   Chaining지원: QuerySet 수행 리턴 값이 다시 QuerySet

*   QuerySet <strong>And</strong> 조건

    *   queryset.filter(조건필드1=조건값1, 조건필드2=조건값2)

    *   ex) qs1과 qs2는 같은 결과

        ```shell
        qs1 = Post.objects.filter(title__iconains='1',title__endwith='3')
        
        qs2 = Post.objects.filter(title__icontiains='1').filter(title__endwith='3')
        ```

*   QuerySet <strong>OR</strong> 조건

    ```shell
    from django.db.models import Q
    Post.objects.filter(Q(title__icontains='1'|Q(title__endwith='3'))
    ```

*   queryset내 기본정렬은 모델 내 Meta.ordering설정 따름

    ```python
    class Post(models.Model):
        class Meta:
            ordering = ['id']
    ```

*   지정 조건으로 DB로부터 데이터를 Fetch

    ```python
    # 특정 조건의 데이터 열 1개 fetch
    model_instance = queryset.get(id=1)
    model_instance = queryset.get(title='my title')
    ```

    *   quertyset.get: 해당 조건에 해당되는 데이터가 <strong>1개</strong>



### 데이터베이스에 데이터 추가 요청(create)

*   방법1: 각 model instance의 save 함수 통해 저장
*   방법2: 각 model manager의 create 함수 통해 저장
*   데이터 베이스에서 insert sql
    *   ex) insert into blog_post('필드명1', '필드명2') values('값1', '값2');



### 데이터베이스 갱신 요청(update)

*   방법1: 각 model 인스턴스 속성 변경하고 <strong>save함수</strong> 통해 저장

    *   각 model 인스턴스 별로 SQL 수행
    *   다수 row에 대해 수행 시 성능 저하 발생 가능

*   방법2: QuerySet의 update 함수에 업데이트할 속성값 지정하여 일괄 수정

    *   Ex)

        ```shell
        queryset=Post.objects.all()
        queryset.update(tag='python, Django') # 일괄 update 요청
        ```



### 데이터베이스 삭제 요청(delete)

*   방법1: 각 model 인스턴스의 <strong> delete함수</strong> 호출하여 데이터베이스 측 관련 데이터 삭제

    *   각 model의 인스턴스 별로 SQL 수행
    *   다수 row에 대해 수행 시 성능 저하 발생 가능

*   방법2: QuerySet의 delete 함수 호출하여, 데이터베이스 측의 관련 데이터 삭제

    *   EX)

        ```shell
        queryset=Post.objects.all()
        queryset.delete()  # 일괄 delete요청
        ```



### Django-debug-toolbar

*   현재 request/response에 대한 다양한 디버깅 정보 보여줌

*   SQLPanel 통해 각 요청 처리 시 발생한 SQL 내역 확인 가능

*   설치:

    ```shell
    pip install django-debug-toolbar
    ```

*   설정:

    ```python
    # settings.py
    INSTALLED_APP= [
        'debug_toolbar',  # 추가
    ]
    
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',  # 추가
    ]
    
    NTERNAL_IPS = ['127.0.0.1']
    
    # urls.py
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += [
            re_path(r'^__debug__/', include(debug_toolbar.urls))
        ]
    ```

*   html에서 body태그가 있어야 사용 가능


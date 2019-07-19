## [중급편] 장고 Form/ModelForm 제대로 알고 쓰기 

## 1 HTML Form

form 태그를 통해 입력폼 구성. submit 시 action의 URL로 데이터 전송. 하나의 form 태그에는 하나 이상의 widget이 있다.

get : 데이터 조회 요청 시 사용

post : 생성, 수정, 삭제 시 사용

##### enctype

1.  application/x-www-form-urlencoded (디폴트)

* GET 요청에서는 이 유형이 강제됨.
* 인자들을 URL 인코딩하여 QueryString 형태로 전달

2.  multipart/form-data

* 파일 업로드 가능

##### url encode

key=value 값의 쌍이 &로 이어진 형태, 공백은 +로 인코딩, special 문자들은 ascii 16진수 문자열, UTF8 인코딩 16진수 문자열로 변환

##### 장고 뷰에서의 인자 접근

* request.GET
    * 모든 QueryString 인자 목록
        * QueryDict은 중복을 허용한다.
    * GET/POST 요청에서 모두 가능
* request.POST
    * POST 요청에서만 가능
    * 파일 내역을 제외한 모든 POST 인자 목록
        * 요청 BODY를 파싱한 QueryDict 객체
* request.FILE
    * POST 요청에서만 가능
    * 요청 BODY에서 파일내역만 파싱한 MultiValueDict 객체

## 02 HttpRequest와 HttpResponse

##### HttpRequest 객체

* 클라이언트로부터의 모든 요청 내용을 담고 있다
    * 함수 기반 뷰 (FBV) : 매 요청 시 뷰 함수의 첫번째 인자 request로 전달
    * 클래스 기반 뷰 (CBV) : 매 요청 시 self.request를 통해 접근
* Form 처리 관련 속성들
    * .method : 요청의 종류 GET 또는 POST로서 모두 대문자
    * .GET : GET 인자 목록 (QueryDict 타입)
    * .POST : POST 인자 목록 (QueryDict 타입)
    * .FILES : POST 인자 중에서 파일 목록 (MultiValueDict 타입)

##### MultiValueDict

* dict를 상속 받은 클래스
* 동일한 키의 다수 값을 지원하는 사전

```python
from django.utils.datastructures import MultiValueDict
d = MultiValueDict({'name': ['A', 'B'], 'position': ['dev']})
d['name'] -> 'B'
d.getlist('name') -> ['A', 'B']
d.getlist('doesnotexist') -> []
d['name'] = 'changed'
d -> <MultiValueDict: {'name':'changed', 'position': ['dev']}>
```

##### QueryDict

* 수정 불가능한 MultiValueDict

```python
from django.http import QueryDict
qd = QueryDict('name=a&name=b&position=dev', encoding='utf8')
qd['name'] -> 'b'
qd.getlist('name') -> ['a', 'b']
qd['name'] = 'changed' -> 'AttributeError: This QueryDict instance is immutable'
```

##### HttpResponse

HTML 문자열, 이미지 등 다양한 응답 wrapping

View에서는 반환값으로서 HttpResponse를 기대

* Middleware에서 HttpResponse 객체를 기대

응답 방법

```python
response = HttpResponse("<p>hello</p>")
```

```python
response = HttpResopnse()
response.write("<p>hello</p>")
```

응답의 커스텀 헤더 추가/삭제

```python
response = HttpResponse()
response['Age'] = 120
del response['Age']
```

##### django.http.JsonResponse

list, object를 json 포맷으로 직렬화한다. QuerySet, ModelInstance에 대한 직렬화는 없고 DRF(Django RestFramework)에서 지원한다.

##### django.http.StreamingHttpResponse

파일을 한 줄씩 읽어서 메모리를 효율적으로 사용한다. 긴 응답은 성능 저하를 야기할 수 있다. HttpResponse를 상속 받지 않았다. iterator를 지정해야 동작한다.

##### django.http.FileResponse

StreamingHttpResponse를 상속받음

* 파일 내용 응답에 최적화
* Content-Length, Content-Type, Content-Disposition 헤더 자동 지정

인자

* open_file : Streaming Content
* as_attachment : Content-Disposition 헤더 지정 여부
* filename

### Shortcuts

##### django.shortcuts.render

템플릿 렌더 시 사용

```python
render(request, template_name, context=None, content_type=None, status=None, using=None)
```

* context : 템플릿 context에 추가할 값 목록 (dict)
* content_type : 응답의 MIME Type (디폴트 : "text/html")
* status : 응답의 상태 코드 (디폴트 : 200)
* using : 템플릿 엔진 지정

##### django.shortcuts.redirect

```python
redirect(to, permanent=False, *args, **kwargs)
```

* to
    1.  get_absolute_url()이 구현된 모델 객체
    2.  URL_Reverse를 수행할 문자열
    3.  직접 지정항 URL 문자열
* permanent
    1.  True : HttpResponsePermanentRedirect (301 응답)
    2.  False : HttpResponseRedirect (302 응답)

##### django.shortcuts.get_object_or_404

* Model.DoesNotExist 예외 대신에 404 응답 발생

* 객체가 1개 있으면 객체 반환, 0개면 404 에러

    ```python
    from django.shortcuts import get_object_or_404
    
    def my_view(request):
      obj = get_object_or_404(MyModel, pk=1)
    ```

##### django.shortcuts.get_list_or_404

-   지정 QuerySet 조건에 대해 empty일 경우 404 응답

    ```python
    from django.shortcuts import get_list_or_404
    
    def my_view(request):
      my_objects = get_list_or_404(MyModel, published=True)
    ```


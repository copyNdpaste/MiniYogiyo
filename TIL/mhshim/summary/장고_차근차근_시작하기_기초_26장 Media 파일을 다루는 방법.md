# 장고 차근차근 시작하기

## 26 Media 파일을 다루는 방법

### Static & Media 파일

*   Static 파일
    *   개발 리소스로서의 정적인 파일 (js, css, image 등)
    *   앱 / 프로젝트 단위로 저장/서빙
*   Media 파일
    *   FileField/ImageField를 통해 저장한 모든 파일
    *   `DB 필드`에는 `저장 경로`를 저장하며, `파일`은 `파일 스토리지`에 저장
        *   __실제로 문자열을 저장하는 필드(중요)__
    *   프로젝트 단우로 저장/서빙

### Media 파일 처리 순서

1.  HttpRequest.FILES를 통해 파일이 전달된다.
2.  뷰 로직이나 폼 로직을 통해 유효성 검증
3.  FileFIeld, ImageField에 `경로(문자열)`를 저장
4.  settings.MEDIA_ROOT 경로에 파일 저장

### Media 파일 관련 settings 예시

`빈 문자열인 디폴트 값을 그대로 둔 상태로 저장하면 manage.py가 있는 디렉토리에 이미지와 파일이 저장된다.`

*   각 설정의 디폴트 값
    *   MEDIA_URL = ""
        *   각 media 파일에 대한 URL Prefix
            *   필드명.url 속성에 의해서 참조되는 설정
    *   MEDIA_ROOT = ""
        *   파일 필드를 통한 저장 시에, 실제 파일을 저장할 ROOT 경로

### 추천 settings

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

### FileField와 ImageField

*   FileField
    *   File Storage API를 통해 파일을 저장
        *   장고에서는 FileSystem Storage만 지원. django-storages를 통해 확장 지원
    *   해당 필드를 옵션 필드로 두고자 할 경우, blank=True 옵션 적용
*   ImageField(FileFied를 상속 받음)
    *   Pillow(이미지 처리 라이브러리)를 통해 이미지 width/height 획득
        *   Pillow 미설치 시, ImageField를 추가한 make migrations 수행에 실패한다
*   위 필드를 상속받은 커스텀 필드를 만들 수 있다.
    *   ex) PDFField, ExcelField 등

`requirements.txt`에 pillow 추가하기

### FileField와 ImageField에서 사용할만한 옵션

*   blank 옵션
    *   업로드 옵션 처리 여부
    *   디폴트: False

*   upload_to 옵션
    *   settings.MEDIA_ROOT 하위에서 저장한 파일명/경로명 결정
    *   디폴트: 파일명 그대로 settings.MEDIA_ROOT에 저장
        *   `추천: 성능을 위해 한 디렉토리에 너무 많은 파일들이 저장되지 않게 하기`
    *   동일 파일명으로 저장할 때 파일명에 더미 문자열이 붙어 파일 덮어쓰기가 방지된다

### 파일 업로드 시에 HTML Form enctype

*   form method는 반드시 POST로 지정

    *   GET의 경우 enctype이 "application/x-www-form-urlencoded"로 고정되어 있다

*   form enctype을 반드시 "multipart/form-data"로 지정

    *   "Application/x-www-form-urlencoded"의 경우, 파일명만 전송된다

    ```html
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <table>
            {{ form.as_table }}
        </table>
        <input type="submit">
    </form>
    ```

### upload_to 인자

*   파일 저장 시 upload_to 함수를 호출하여 저장 경로를 계산한다
    *   파일 저장 시 upload_to 인자를 변경한다고 해서 DB에 저장된 경로값이 갱신되지 않는다
*   인자 유형
    *   문자열로 지정
        *   파일을 저장할 "중간 디렉토리 경로"로서 활용
    *   함수로 지정
        *   "중간 디렉토리 경로" 및 "파일명"까지 결정 가능

### 파일 저장 경로

*   travel-20181225.jpg 파일을 업로드할 경우
    *   MEDIA_ROOT/travel-20181225.jpg 경로에 저장된다
    *   DB에는 "travel-20181225.jpg" 문자열을 저장한다

### 파일 저장 경로 / 커스텀 (upload_to 옵션)

*   디렉토리에 파일을 너무 많이 쌓아두면 OS의 파일 찾기 성능이 저하도니다. 디렉토리 Depth가 깊어지는 것은 성능에 큰 영향을 미치지 않는다

*   필드별로 다른 디렉토리 저장 경로 지정

    1.  ~~필드별 다른 디렉토리에 저장~~

        *   photo = models.ImageField(upload_to="blog")

        *   photo = models.ImageField(upload_to="blog/photo")

    2.  **업로드 시간대별 다른 디렉토리에 저장**
        *   upload_to에서 strftime 포매팅 지원
        *   photo = models.ImageField(upload_to="blog/%Y/%m/%d")

UUID로 파일명 지정

![image-20190423131431500](/Users/b201903149/Library/Application Support/typora-user-images/image-20190423131431500.png)

### 템플릿에서 media URL 처리 예시

*   필드의 .url 속성 활용

    *   내부적으로 settings.MEDIA_URL과 조합을 처리

        ```html
        <img src="{{ post.photo.url }}"/>
        ```

    *   필드에 저장된 경로에 없을 경우 .url 계산에 실패함. 그러므로 필드명 저장 유무를 체크한다

        ```html
        {% if post.photo %}
        	<img src="{{ post.photo.url }}"/>
        {% endif %}
        ```

*   참고
    *   파일 시스템 상의 절대 경로가 필요하다면, .path 속성 활용
        *   settings.MEDIA_ROOT와 조합

### 개발환경에서의 media 파일 서빙

*   static 파일과 다르게 장고 개발서버에서 서빙 미지원

*   개발 편의성 목적으로 직접 서빙 Rule 추가 가능

    ```python
    from django.conf import settings
    from django.conf.urls.static import static
    
    # 중략
    
    urlpatterns += static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
    ```

### File Upload Handler

*   파일 크기가 2.5MB 이하일 경우
    *   메모리에 담겨 전달
    *   MemoryFileUploadHandler
*   파일 크기가 2.5MB 초과일 경우
    *   디스크에 담겨 전달
    *   TemporaryFileUploadHandler
*   관련 설정
    *   settings.FILE_UPLOAD_MAX_MEMORY_SIZE
        *   -> 2.5MB
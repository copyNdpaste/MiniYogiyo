#Two_Scoops_of_Django

## 8장 함수 기반 뷰와 클래스 기반 뷰

장고 1.8은 함수 기반 뷰와 클래스 기반 뷰를 둘 다 지원한다.

### 8.1 함수 기반 뷰와 클래스 기반 뷰를 각각 언제 이용할 것인가?

클래스 기반 뷰로 구현했을 경우 특별히 더 복잡해지는 경우나 커스텀 에러 뷰들에 대해서만 함수 기반 뷰를 이용한다.

[![django 어떤 뷰를 선택해야 할까에 대한 이미지 검색결과](https://eunhyang.github.io/assets/images/post_images/two_scoops_of_django/f1.png)](https://www.google.co.kr/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwjwy9KzssThAhXGQN4KHW9rCUkQjRx6BAgBEAU&url=https%3A%2F%2Feunhyang.github.io%2F2018-10-23%2Ftwo-scoops-of-django-8%2F&psig=AOvVaw37FBTQyiKXEGU5bqfyjStJ&ust=1554946809125103)

>   대안 - 함수 기반 뷰 이용
>
>   대부분의 뷰를 함수 기반 뷰로 처리하고 클래스 기반 뷰는 서브 크랠스가 필요한 경우에 대해 제한적으로 이용한다.

### 8.2 URLConf로부터 뷰 로직을 분리하기

장고로 오는 요청들은 urls.py라는 모듈 내에서 URLConf를 통해 뷰로 라우팅된다. 뷰와 URL의 결합은 최대한의 유연성을 위해 느슨하게 구성되어야 한다.

URL 라우트 구성에 대한 방법론

1.  뷰 모듈은 뷰 로직을 포함해야 한다.
2.  URL 모듈은 URL 로직을 포함해야 한다.

```python
# 나쁜 예제
from django.conf.urls import url
from django.views.generic import DetailView

from tastings.models import Tasting

urlpatterns = [
    url(r"(?P<pk>\d+)/$",
       DetailView.as_view(
           model=Tasting,
           template_name="tastings/detail.html"),
       name="detail"),
    url(r"(?P<pk>\d+)/results/$",
       DetailView.as_view(
           model=Tasting,
           template_name="tastings/results.html"),
       name="results"),
]
```

>   위 코드의 문제점
>
>   *   뷰와 url과 모델 사이에 느슨한 결합 대신 종속적인 결합이 되어 있다. -> 뷰에서 정의된 내용이 재사용되기 어렵다.
>   *   클래스 기반 뷰들 사이에서 같거나 비슷한 인자들이 계속 이용되고 있는데 이는 반복되는 작업을 하지 말라는 철학에 위배된다.
>   *   URL들의 확장성이 파괴되어 있다. 클래스 기반 뷰의 최대 장점인 클래스 상속이 안티 패턴을 이용함으로써 불가능하게 되어 버렸다.
>   *   뷰 코드가 URLConf 안에 있으므로 기능을 추가하기 어렵다.

### 8.3 URLConf에서 느슨한 결합 유지하기

```python
# tastings/views.py
from django.views.generic import ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse

from .models import Tasting

class TasteListView(ListView):
    model = Tasting

class TasteDetailView(DetailView):
    model = Tasting

class TasteResultsView(TasteDetailView):
    template_name = "tastings/results.html"

class TasteUpdateView(UpdateView):
    model = Tasting

	def get_success_url(self):
        return reverse("tastings:detail",
                      kwargs={"pk": self.object.pk})
```

```python
# tastings/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
    	regex=r"^$",
        view=views.TasteListView.as_view(),
        name="list"
    ),
    url(
    	regex=r"^(?P<pk>\d+)/$",
        view=views.TasteDetailView.as_view(),
        name="detail"
    ),
    url(
    	regex=r"(?P<pk>\d+)/results/$",
        view=views.TasteResultsView.as_view(),
        name="results"
    ),
    url(
    	regex=r"(?P<pk>\d+)/update/$",
        view=views.TasteUpdateView.as_view(),
        name="update"
    )
]
```

>   파일이 분리됐고 코드가 늘어났지만 이 방법이 더 낫다.
>
>   *   반복되는 작업하지 않기: 뷰 사이에서 인자나 속성이 중복 사용되지 않는다.
>   *   느슨한 결합: URLConf로부터 모델과 템플릿 이름을 전부 제거했다. 뷰는 뷰. URLConf는 URLConf여야 한다. 여러 url에서 여러 뷰들이 호출될 수 있다.
>   *   URLConf는 한 번에 한 가지씩 업무를 명확하고 매끄럽게 처리해야 한다. URLConf는 URL 라우팅이라는 한 가지 명확한 작업만 처리하는 것을 목표로 한다.
>   *   클래스 기반이라는 것에 대한 장점을 살리게 된다: 뷰 모듈에서 표준화된 정의를 가지게 됨으로써 다른 클래스에서 뷰를 상속해서 쓸 수 있다.
>   *   무한한 유연성: 뷰 모델에서 표준화된 정의를 구현함에 따라 우리는 뷰는 커스텀 로직이라도 얼마든지 구현할 수 있다.

##### 클래스 기반 뷰를 사용하지 않는다면?

_\_file__ 속성을 이용하여 디렉토리 워킹과 정규표현식을 혼합하여 자동으로 URLConf를 생성하는 정교한 트릭을 이용한 URLConf 확장을 함수 기반 뷰와 함께 사용하는 프로젝트를 다루는 것은 `디버깅하기 힘들다.`

`항상 URLConf로부터 로직을 분리 운영해야 한다.`

### 8.4 URL 이름공간 이용하기

URL 이름공간은 앱 레벨 또는 인스턴스 레벨에서의 구분자를 제공한다.

tastings_detail이라는 URL 이름 대신 tastings:detail이라고 정의한다.

```python
# 프로젝트 루트에 있는 urls.py
urlpatterns += [
    url(r'^tastings/', include('tastings.urls', namespace='tastings')),
]
```

```python
# tastings/views.py 코드 조각
class TasteUpdateView(UpdateView):
    model = Tasting

    def get_success_url(self):
        return reverse("tastings:detail",
                      kwargs={"pk": self.object.pk})
```

```html
{% extends "base.html" %}

{% block title %}Tastings{% endblock title %}

{% block content %}
<ul>
    {% for taste in tastings %}
    <li>
    	<a href="{% url "tastings:detail" taste.pk %}">{{ taste.title }}</a>
        <small>
        	(<a href="{% url "tastings:update" taste.pk %}">update</a>)
        </small>
    </li>
    {% endfor %}
</ul>
{% endblock content %}
```

##### URL 이름을 짧고, 명확하고, 반복되는 작업을 피해서 작성하는 방법

모델이나 앱의 이름을 복사한 URL 이름들은 더 이상 없다. 더 명확한 이름을 사용한다.

##### 서드 파티 라이브러리와 상호 운영성을 높이기

URL 이름을 \<myapp>_detail 등의 방법으로 부를 때 생기는 문제는 \<myapp> 부분이 겹칠 때 이다. 이 경우 URL 이름 공간으로 해결할 수 있다.

```python
# 프로젝트 루트에 있는 urls.py
urlpatterns += [
    url(r'^contact/', include('contactmonger.urls', namespace='contactmonger')),
    url(r'^report-problem/', include('contactapp.urls', namespace='contactapp')),
]
```

다음과 같이 템플릿에서 사용 가능하다.

```html
{% extends "base.html" %}
{% block title %}Contact{% endblock title %}
{% block content %}
<p>
    <a href="{% url "contactmonger:create" %}">Contact</a>
</p>
<p>
    <a href="{% url "contactapp:report" %}">Report a Problem</a>
</p>
{% endblock content %}
```

##### 검색, 업그레이드, 리팩토링 쉽게 하기

tastings:detail 이라는 이름은 검색 결과를 좀 더 명확하게 해 준다. 이는 새로운 서드 파티 라이브러리와 상호 연동 시에 앱과 프로젝트를 좀 더 쉽게 업그레이드하고 리팩토링하게 만들어 준다.

##### 더 많은 앱과 템플릿 리버스 트릭을 허용하기

*   django-debug-toolbar 같은 디버그 레벨에서 내부적인 검사를 실행하는 개발 도구
*   최종 사용자에게 '모듈'을 추가하게 하여 사용자 계정의 기능을 변경하는 프로젝트

### 8.5 URLConf에서 뷰를 문자열로 지목하지 말자

```python
# 나쁜 예
# polls/urls.py
from django.conf.urls import patterns, url

urlpatterns = pattern('',
                     # 뷰를 문자열로 정의
                     url(r'^$', 'polls.views.index', name='index'),
                     )
```

이런 방법에는 몇 가지 문제가 수반된다.

1.  장고가 뷰의 함수, 클래스를 임의로 추가한다. 이런 임의적 기능의 문제점은 뷰에서 에러가 발생할 경우 이렇게 임의의 작용을 하는 부분에 대해 디버그 하기가 어려워 진다는 점이다.
2.  urlpatterns 변수의 초깃값에서의 공백 문자열에 대해 알아야 한다.

urls.py를 정의하는 올바른 방법

```python
# polls/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    # 뷰를 명시적으로 정의
    url(r'^$', views.index, name='index')
]
```

### 8.6 뷰에서 비즈니스 로직 분리하기

모델 메서드, 매니지 메서드 또는 일반적인 유틸리티 헬퍼 함수들을 이용하는 전략을 선호한다. 비즈니스 로직이 쉽게 재사용 가능한 컴포넌트가 되고 이를 뷰에서 호출하는 경우, 프로젝트에서 해당 컴포넌트를 확장하기 쉬워진다.

### 8.7 장고의 뷰와 함수

기본적으로 장고는 HTTP를 요청하는 객체를 받아서 HTTP를 응답하는 객체로 변경하는 함수다.

```python
# 함수로서의 장고 함수 기반 뷰
HttpResponse = view(HttpRequest)

# CBV로 변형
HttpResponse = View.as_view()(HttpRequest)
```

>   클래스 기반 뷰의 경우 실제로 함수로 호출된다
>
>   URLConf에서 View.as_view()라는 클래스 메서드는 실제로 호출 가능한 뷰 인스턴스를 반환한다.

##### 뷰의 기본 형태들

```python
# simplest_views.py
from django.http import HttpResponse
from django.views.generic import View

# 함수 기반 뷰의 기본 형태
def simplest_view(request):
    # 비즈니스 로직은 여기에 위치
    return HttpResponse("FBV")
# 클래스 기반 뷰의 기본 형태
class SimplestView(View):
    def get(self, request, *args, **kwargs):
        # 비즈니스 로직은 여기에 위치
    return HttpResponse("CBV")
```

왜 이 기본 형태가 중요한가?

*   한 기능만 따로 떼어 놓은 관점이 필요할 때가 있다.
*   가장 단순한 형태로 된 기본 장고의 뷰를 이해했다는 것은 장고 뷰의 역할을 명확히 이해했다는 것이다.
*   장고의 함수 기반 뷰는 HTTP 메서드에 중립적이지만, 클래스 기반 뷰의 경우 HTTP 메서드의 선언이 필요하다는 것을 설명해 준다.

### 8.8 locals()를 뷰 콘텍스트에 이용하지 말자

locals()를 호출형으로 반환하는 것은 안티 패턴이다.

명시적이었던 디자인이 암시적 형태의 안티 패턴이 되어 버린다.

뷰에서 명시적 콘텐츠를 이용하기를 추천한다.

```python
def ice_cream_store_display(request, store_id):
    return render(request, 'melted_ice_cream_report.html', dict{
        'store': get_object_or_404(Store, id=store_id),
        'now': timezone.now()
    })
```

### 8.9 요약

함수 기반 뷰 또는 클래스 기반 뷰를 언제 이용하는 지 다루었고, 패턴을 다루었다.

URLConf에서 뷰 로직을 분리하는 기법에 대해 이야기했다. 뷰 코드는 앱의 views.py 모듈에, 그리고 URLConf 코드는 앱의 urls.py 모듈에 소속되어야 한다. 클래스 기반 뷰를 이용할 때 객체 상속을 이용함으로써 코드를 재사용하기 쉬워지고 디자인을 좀 더 유연하게 할 수 있다.


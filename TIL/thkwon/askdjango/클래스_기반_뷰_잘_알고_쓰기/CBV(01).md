# CBV

## 01 Overview

CBV의 기본 구조에 대해 이해해보자.

* `view`는 호출 가능한 객체

```python
from django. shortcuts import render
from .models import Post

def post_list(request):
    """ FBV """
    qs = Post.objects.all()
    return render( request, 'blog/post_list.html', {
            'post_list': qs,
        }
```



```python
from django.views.generic import ListView
from .models import Post

calss PostListView(ListView):
    """ CBV """
    model = Post
    
post_list = PostListView.as_view()
```



### Class Based View

* View 함수를 만들어주는 클래스
    * as_view() 클래스 함수를 통해, View 함수를 생성
* 장고 기본 CBV 패키지
    * django.views.generic



### CBV 컨셉 구현

### 1. FBV

```python
# views.py
from django.shortcuts import get_object_or_404, render

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(reuest, 'blog/post_detail.html', {
        'post': post,
    }
```



### 2. 함수를 통해, 동일한 View 함수 생성

```python
def generate_view_fn(model):
    def view_fn(request, id):
        instance = get_object_or_404(model, id=id)
        instance_name = model._meta.model_name
        template_name = '{}/{}_detail.html'.format(
            model._meta.app_label, 
            instance_name
        )
        return render(request, template_name, {
            instance_name: instance,
        })
    return view_fn

post_detail = generate_view_fn(Post)
```

* 파이썬은 일급 객체를 지원하는 언어이기 때문에 동적으로 함수를 만들 수 있다.
* `generate_view_fn`이 호출 될 때, 내부의 `view_fn`이 호출되고, 그 함수를 반환한다.
* 위에서는 post_detail에 generate_view_fn을 호출함으로써, 반환되는 view_fn 함수가 대입된다.



### 3. Class로 동일한 View 함수 구현

```python 
class DetailView:
    def __init__(self, model):
        self.model = model
        
    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, id=kwargs['id'])
    
    def get_template_name(self):
        return '{}/{}_detail.html'.format(
            self.model._meta.app_label,
            self.model._meta.model_name
        )
    
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object(*args, **kwargs)
        return render(request, self.get_template_name(), {
            self.modoel._meta.model_name: object,
        })
    
    @classmethod
    def as_view(cls, model):
        def view(request, *args, **kwargs):
            self = cls(model)
            return self.dispatch(request, *args, **kwargs)
        return view
```

```python
post_detail = DetailView.as_view(Post)
```





### 4. Djdango 기본 제공 CBV 활용

```python
from django.views.generic import DetailView

# 방법1 - 로직 재구현을 할 때, 사용
# 직접 메소드를 구현 가능하다.
class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'id'

post_detail = PostDetailView.as_view()
```

```python 
# 방법2
# 기본적으로 몇가지 세팅만 해줄 때 사용
post_detail = DetailView.as_view(model=Post, pk_url_kwargs='id')
```





### CBV는

* CBV가 정한 관례대로 개발할 경우 아주 적은 양의 코드로 구현
    * 그 관례에 대한 이해가 필요
    * 필요한 설정값을 제공하거나, 특정 함수를 재정의하는 방식으로 커스텀 가능
    * 그 관례를 잘 이해하지 못하고 사용하거나, 그 관례를 벗어난 구현을 하고자 할 때는 복잡해지는 경향이 있다.
* CBV를 제대로 이해하려면
    * 코드를 통한 이해가 지름길
        * **코드를 직접 까보면서 이해하는게 중요하다.**
        * 파이썬 클래스에 대한 이해가 필요(특히, 상속, 인자, paking/unpacking)
* CBV 코드를 동일하게 동작하는 FBV 구현해보는 연습을 하자.





## 02 Built-in CBV API

CBV의 기본 클래스인 `View`, `TemplateView`, `RedirectView` 클래스들을 코드와 함께 이해해보는 시간을 가져보겠습니다.

### Built-in CBV API

* Base views
    * View, TemplateView, RedirectView



### Base Views

* View
* TemplateView
    * TemplateResponseMixin 상속
    * ContextMixin 상속
    * View 상속
* RedirectView
    * View를 상속

 

### View 클래스

* 모든 CBV의 모체
    * 이 CBV를 직접 쓸 일은 거의 없다.
    * 대개 상속의용도로 활용 한다.
* http method 별로 지정 이름의 멤버 함수를 호출토록 구현
* CBV.as_view(**initkwargs)
    * Initkwargs 인자는 그대로 CBV 생성자 로 전달



```python
class View:
    def __init__(self, **kwargs):
        #...
        
    @classonlymethod
    def as_view(cls, **initkwargs):
        def view(request, *args, **kwargs):
            return self.dispatch(request, *args, **kwargs)
        
       	return view
    
    def dispatch(self, request, *args, **kwargs):
        # ...
        # request.method.lower() 이름의 멤버함수를 호출
        handler = getattr(self, request.method.lower(),
                          self.http_method_not_allowed)
        return handler(request, *args, **kwargs)
    
    def http_method_now_allowed(self, request, *args, **kwargs):
        # ...
        return HttpResponseNotAllowed(self._allowed_methods())
    
    def options(self, request, *args, **kwargs):
        # ...
        return reponse
    
    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_naems
                if hasattr(self, m)]
```



### TemplateView

```python
def myview(request):
    context = {
        'hello': 'world',
        'ip': request.META['REMOTE_ADDR']
    }
    return render(request, 'myapp/myview.html', context)

#위를 CBV로 구현
myview = TemplateView.as_view(
    template_name='myapp/myview.html',
    extra_context={'hello': 'world'} #정적 context
)
```



```python
def myview(request):
    context = {
        'hello': 'world',
        'ip': request.META['REMOTE_ADDR']
    }
    return render(request, 'myapp/myview.html', context)

#위를 CBV로 구현
class MyTemplateView(TemplateView):
    template_name = 'myapp/myview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hello': 'world',
            'ip': request.META['REMOTE_ADDR']
        })
        return context

myview = MytemplateView.as_view()
```



### RedirectView

* permanent = False
* url = None
    * URL 문자열
* pattern_name = None
    * URL Reverse를 수행할 문자열
* query_string = False
    * QueryString을 그대로 넘길 것인지 여부

```python
def myview(request):
    return redirect("https://www.naver.com")
#위를 CBV로 구현
myview = RedirectView.as_view(urls='https://www.naver.com')
```





## 03 built-in CBV API (Generic display views)

기본 조회 View인 `DetailView`, `ListView`를 코드와 함께 상속관계까지 이해해보는 시간을 가져보겠습니다.

### Generic display views

* DetailView
    * <— SingleBojectTemplateResonseMixin
        * "app/model_detail.html" 경로를 만들어준다.
        * <— TemplateResponseMixin
            * 어떤 템플릿이 미리 지정되어야됨
    * <— BaseDetailView
        * <— SingleObjectMixin
            * Object 획득
        * <— View
* ListVIew
    * <— MultipleObjectTemplateResponseMixin
        * "app/model_llist.html" 경로를 만들어준다.
        * <— TemplateResponseMixin
    * <— BaseListVIew
        * <— MultipleObjectMixin <— ContextMixin
            * 다수의 Object 획득
        * <— View
            * HTTP Method에 따라서 관련 멤버 함수를 호출



### DetailView

* 1개 모델의 1개 Object에 대한 템플릿 처리

    ```python
    # app/views.py
    from django.views.generic import DetailView
    from .models import Post
    # 방법1
    post_detail = DetailView.as_view(model=Post)
    
    # 방법2
    class PostDetailView(DetailView):
        model = Post
    post_detail2 = PostDetailView.as_view()
    ```

    ```python
    # app/urls.py
    from django.urls import path
    from . import views_cbv
    
    app_name = "blog"
    
    urlpatterns = [
        path(
            '<int:pk>/', views_cbv.post_detail, name="post_detail_cbv"
        )
    ]
    
    ```



### ListView

* 1개 모델에 대한 List 템플릿 처리
    * 모델명소문자_list 이름의 QuerySet을 템플릿에 전달
* **페이징 처리 지원**

```python 
from django.views.generic import ListView
from .models import Post

post_list1 = ListView.as_view(model=Post)

post_list2 = ListView.as_view(model=Posot, paginate_by=10)

class PostListView(ListView):
    model = Post
    paginate_by = 10
    
post_list3 = PostListView.as_view()


class PostListView(ListView):
    model = Post
    paginated_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(...).
        return qs
    
post_list4 = PostListView.as_view()
```


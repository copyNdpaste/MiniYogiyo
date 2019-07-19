# 클래스 기반 뷰 잘 알고 쓰기

## 1 Overview

### View 호출 가능한 객체 (Callable Object)

*   함수 기반 뷰 (Function Based View)

```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    qs = Post.objects.all()
    return render(request, 'blog/post_list.html', {
        'post_list': qs,
    })
```

*   클래스 기반 뷰 (Class Based View)

```python
from django.views.generic import ListView
from .models import Post

class PostListView(ListView):
    model = Post
    
post_list = PostListView.as_view()
```

### Class Based View

*   View 함수를 만들어주는 클래스
    *   as_view() 클래스 함수를 통해 View 함수 생성
*   장고 기본 CBV 패키지
    *   django.views.generic
*   써드파티 CBV
    *   django-braces

### CBV 컨셉 구현하기

### 1. FBV

```python
urlpatterns = [
    path('post/<int:id>/', post_detail),
    path('article/<int:id>/', article_detail),
]
```

```python
from django.shortcuts import get_object_or_404, render

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {
        'post': post,
    })

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'blog/article_detail.html', {
        'article': article,
    })
```

### 2. 함수를 통해, 동일한 View 함수 생성

```python
def generate_view_fn(model):
    def view_fn(request, id):
        instance = get_object_or_404(model, id=id)
        instance_name = model._meta.model_name
        template_name = '{}/{}_detail.html'.format(model._meta.app_label, instance_name)
        return render(request, template_name, {
            instance_name: instance,
        })
    return view_fn

post_detail = generate_view_fn(Post)
article_detail = generate_view_fn(Article)
```

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
        	self.model._meta.model_name)
    
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object(*args, **kwargs)
        return render(request, self.get_template_name(), {
            self.model._meta.model_name: object,
        })
    
    @classmethod
    def as_view(cls, model):
        def view(request, *args, **kwargs):
            self = cls(model)
            return self.displatch(request, *args, **kwargs)
        return view
```

```python
# 사용
post_detail = DetailView.as_view(Post)
article_detail = DetailView.as_view(Article)
```

### 4. 장고 기본 제공 CBV 활용

```python
# DetailView.as_view()에서 필요한 속성을 나열하는 방법
from django.views.generic import DetailView

post_detail = DetailView.as_view(model=Post, pk_url_kwarg=id)
```

```python
#pk_url_kwarg 인자를 urlpatterns에서 'pk'로 지정했다면 pk_url_kwarg는 디폴트로 pk이므로 pk_url_kwarg 생략 가능
from django.views.generic import DetailView

post_detail = DetailView.as_view(model=Post)
```

```python
urlpatterns = [
    path('post/<int:pk>/', post_detail),
]
```

```python
# DetailView를 상속 받아 멤버 변수, 멤버 함수를 사용하는 방법, 위의 방법과는 다르게 변수 함수를 구현할 수 있다.
from django.views.generic import DetailView

class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'id'
    
post_detail = PostDetailView.as_view()
```


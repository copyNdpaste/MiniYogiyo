# Django setting for different environments

환경을 분리하는 이유

1.  DEBUG를 사용하는 지 검사할 필요가 없다.
2.  공통된 부분을 상속받아 사용할 수 있다.
3.  개인적으로 사용하는 local 환경을 버전 컨트롤로 관리할 수 있다.



간단한 유투브 영상 <https://www.youtube.com/watch?v=zPVLRvpzOOU>

블로그 글 <https://cjh5414.github.io/django-settings-separate/>



프로젝트 내의 tutorial 앱에 settings 디렉토리를 생성한다.

settings

​	_\_init.py__

​	prod.py

​	dev.py

​	base.py (common.py)

​	local.py (.gitignore에 추가해서 무시하기)



settings.py에 있는 모든 코드를 복사해서 base.py에 붙여넣기

base.py는 settings라는 디렉토리 안에 있으므로 경로를 찾도록 하기 위해서 os.path.dirname()이 하나 더 필요하다. 아래 코드로 수정한다. [os.path.dirname(_\_file__)](<https://stackoverflow.com/questions/25139403/why-os-path-dirname-file-is-working-in-django>)이 뭐지? os.path.abspath()로 파일의 절대 경로를 찾고 이후에 os.path.dirname()이 디렉토리 이름을 찾는다. 최상위까지 찾다보면 그게 root 디렉토리가 된다. 그 값이 BASE_DIR에 할당된다.

```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

dev.py

```python
from tutorial.settings.base import *

# Override base.py settings here
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

try:
    from tutorial.settings.local import *
except:
    pass
```

prod.py

```python
from tutorial.settings.base import *

# Override base.py settings here
DEBUG = False

ALLOWED_HOSTS = ['miniyogiyo.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': 'password'
    }
}

try:
    from tutorial.settings.local import *
except:
    pass
```



개발용 setting과 서버용 setting 등 용도별 setting들을 실행하기 위해 —settings 옵션을 계속 쓰다보면 귀찮다.

DJANGO_SETTINGS_MODULE 환경 변수를 원하는 환경으로 설정하면 된다.



wsgi.py나 settings.py의

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")를

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings.prod")로 변경



.gitignore에서 /tutorial/settings/local 추가
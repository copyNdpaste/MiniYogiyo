# Two Scoops of Django

## 6장 장고에서 모델 이용하기

>   모델을 작업하면서 이용하는 장고 패키지들
>
>   django-model-utils: TImeStampedModel 같은 일반적인 패턴들을 처리하는 데 이용
>
>   django-extensions: 모든 앱에 클래스를 자동으로 로드해주는 shell_plus라는 강력한 관리 명령을 제공. 단점은 '작지만 역할이 분명한 앱'에 맞지 않게 너무 다양한 기능 포함

### 6.1 시작하기

##### 모델이 너무 많으면 앱을 나눈다

앱 하나에 모델이 20개 이상이면 앱이 너무 많은 일을 하고 있는 것. 크기가 작은 앱으로 분리하는 것을 고려. 앱이 가진 모델 수가 5개 이하여야 함.

##### 모델 상속에 주의

장고는 3가지 모델 상속 방법을 제공한다. 추상화 기초 클래스, 멀티 테이블 상속, 프락시 모델이다.

| 모델의 상속 스타일                                           | 장점                                                         | 단점                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 상속 이용 안하는 경우 : 모델들 사이에 공통 필드가 존재할 경우, 모델들에 해당 필드를 만듦 | 한 눈에 이해하기 쉽다                                        | 모델들 사이에 서로 중복되는 테이블이 많을 경우 관리가 어렵다 |
| 추상화 기초 클래스 : 오직 상속받아 생성된 모델들의 테이블만 생성된다. | 추상화된 클래스에 공통 부분을 작성. 추가 테이블이 생성되지 않음. 여러 테이블을 조인하며 발생하는 성능 저하 없음 | 부모 클래스를 독립적으로 이용할 수 없다. 추상 클래스라 실재하지 않음 |
| 멀티테이블 상속 : 부모와 자식 모델에 대해 모두 테이블 생성. OneToOneField는 부모와 자식 간 적용 | 각 모델에 대해 매칭되는 테이블 생성. 부모, 자식 모두에 쿼리 가능. 부모 객체로부터 자식 객체 호출 가능. parent.child | 자식 테이블에 대한 각 쿼리에 해대 부모 테이블로의 조인이 필요->부하 발생. 멀티 테이블은 상속하지 않은 걸 권함 |
| 프락시 모델 : 원래 모델에 대해서만 테이블 생성               | 각기 다른 파이썬 작용(behavior)을 하는 모델들의 별칭을 가질 수 있다 | 모델의 필드를 변경할 수 없다                                 |

*   모델 사이에서 중복되는 내용이 1, 2개면 모델의 상속 자체가 필요 없다. 모델에 필드를 직접 추가한다.
*   모델들 사이에 `중복된 필드가 너무 많`을 때 공통 필드 부분이 `추상화` 기초 모델로 이전될 수 있게 리팩토링한다.
*   멀티테이블 상속은 혼란과 상당한 부하를 일으키므로 반드시 피한다. 모델들 사이에 좀 더 명확한 OneToOneField와 ForeignKeys를 이용함으로써 조인이 많을 때 수월하게 해결 가능

##### 실제로 모델 상속해 보기 : TimeStampedModel

장고의 모든 모델에서 created와 modified 타임스탬프 필드를 생성해 두는 것은 일반적이다. 모든 모델에 일일이 2가지 필드를 추가하지 말고 TimeStampedModel을 만들어 이 모델이 우리 대신 필드 추가를 처리하게 해주면 된다.

```python
# core/models.py
from django.db import models

class TimeStampedModel(models.Model):
    '''
    'created'와 'modified' 필드를 자동 업데이트 해주는 추상화 기반 클래스 모델.
    '''
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

코드의 마지막 2줄이 `TimeStampedModel`을 추상화 기초 클래스로 만들어 준다.

`TimeStampedModel` 을 상속하는 새 클래스를 정의할 때 `TimeStampedModel` 을 추상화 기초 클래스로 선언함으로써 장고에서 마이그레이션을 실행할 떄 core_timestampedmodel 테이블이 생성되지 않는다.

```python
# flavors/models.py
from django.db import models

from core.models import TimeStampedModel

class Flavor(TimeStampedModel):
    title = models.CharField(max_length=200)
```

하나의 flavors_flavor 데이터베이스 테이블만 생성한다.

`TimeStampedModel` 가 추상화 기초 클래스가 아니었다면 core_timestampedmodel 테이블이 생성되었을 것이다. 또한 Flavor를 포함한 모든 서브클래스들이 `TimeStampedModel` 과 연결되는 외부 키를 통해 created/modified 타임스탬프를 처리했을 것이다.

##### 데이터베이스 마이그레이션

장고 1.7부터 south라는 외부 라이브러리를 대체하는 django.db.migrations가 있다.

*   새 앱, 모델이 생성되면 새 모델에 대해 python manage.py migrations를 실행한다.
*   생성된 마이그레이션 코드를 실행하기 전에 생성된 코드를 살펴보자. sqlmigrate 명령을 통해 어떤 SQL문이 실행되는지 확인
*   외부 앱에 대해 마이그레이션을 처리할 때는 MIGRATION_MODULES 세팅을 이용한다.
*   마이그레이션 개수가 너무 많으면 squashmigrations를 이용한다.

마이그레이션의 배포와 관리

*   배포 전에 마이그레이션을 되돌릴 수 있는지 확인. 규모가 큰 프로젝트에서는 버그 트레킹이나 배포 시 문제가 될 수 있다.
*   테이블에 이미 많은 데이터가 존재하면 스테이지 서버에서 미리 테스트하기
*   MySQL을 이용하면
    *   스키마를 변환하기 전 DB 백업, why? 롤백 불가
    *   데이터베이스를 변환하기 전에 프로젝트를 읽기 전용으로 변경
    *   큰 테이블의 경우 스키마 변경에 상당한 시간이 소요된다.

### 6.2 장고 모델 디자인

장고에서 가장 어려운 주제 -> 좋은 장고 모델 디자인

##### 정규화하기

장고 모델의 디자인은 항상 정규화로부터 시작.

##### 캐시와 비정규화

적절한 위치에 캐시를 세팅하는 것은 모델을 비정규화할 때 발생하는 문제점들을 상당 부분 해결

##### 반드시 필요한 경우에만 비정규화

비정규화는 프로젝트 자체를 복잡하게 만들고 데이터를 손실시킬 수 있는 위험을 증가시킬 수 있는 문제 야기

##### 언제 널을 쓰고 언제 공백을 쓸 것인가

모델 필드를 정의할 때 null, blank 모두 기본값은 False다.

| 필드 타입                                                    | null=True로 설정                                  | blank=True로 설정                                            |
| ------------------------------------------------------------ | ------------------------------------------------- | ------------------------------------------------------------ |
| CharField, TextField, SlugField, EmailField, CommaSeparatedIntegerField, UUIDField | X                                                 | O 위젯이 빈 값을 허용하면 설정. 빈 값이 빈 문자열로 저장됨   |
| FileField, ImageField                                        | X                                                 | CharField와 동일                                             |
| BooleanField                                                 | X NullBooleanField 이용                           | X                                                            |
| IntegerField, FloatField, DecimalField, DurationField 등     | DB에 NULL로 들어가도 되면 이용                    | 위젯에서 빈 값을 받아도 되면 이용. null=True와 같이 이용     |
| DateTimeField, DateField, TimeField 등                       | DB에 NULL 설정 가능하면 이용                      | 위젯에서 빈 값을 받아도 되거나 auto_now, auto_now_add를 이용하면 이용. null=True와 같이 이용 |
| ForeignKey, ManyToManyField, OneToOneField                   | DB에 해당 값들을 NULL로 설정하는 게 가능하면 이용 | 위젯에서 해당 값(ex:select box)이 빈 값을 받아도 되면 이용   |
| GenericIPAddressField                                        | DB에서 NULL로 설정 가능하면 이용                  | 위젯에서 빈 값을 받아도 되면 이용                            |
| IPAddressField                                               | X                                                 | X                                                            |

IPAddressField는 장고 1.7 이후 사라질 예정

##### 언제 BinaryField를 이용할 것인가?

장고 1.8부터 추가. raw binary data 또는 byte를 저장하는 필드다. 이 필드에선 filter, exclude, 기타 SQL 액션이 적용되지 않는다. 다음과 같은 내용을 저장할 때 쓰일 수 있다.

*   메시지팩 형식의 컨텐츠
*   원본 센서 데이터
*   압축된 데이터

>   BinaryField로부터 파일을 직접 서비스하는 것은 금물
>
>   데이터베이스를 파일 저장소로 이용하는 것의 문제점
>
>   *   파일 시스템의 '읽기/쓰기' 속도보다 느림
>   *   백업에 드는 공간 시간이 점점 증가
>   *   파일 자체에 접근하는 데 앱 레이어와 DB 레이어 둘 다를 거쳐야만 함

##### 범용 관계 피하기

범용 관계란 한 테이블로부터 다른 테이블을 서로 제약 조건이 없는 외부 키로 바인딩하는 것이다.

*   모델 간의 인덱싱이 존재하지 않으면 쿼리 속도 손해
*   다른 테이블에 존재하지 않는 레코드를 참조할 수 있는 데이터 충돌 위험성 존재

##### PostgreSQL에만 존재하는 필드에 대해 언제 널을 쓰고 언제 공백을 쓸 것인가

| 필드 타입                                                | null=True로 설정                                | blank=True로 설정                                            |
| -------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------ |
| ArrayField                                               | O                                               | O                                                            |
| HStoreField                                              | O                                               | O                                                            |
| IntegerRangeField, BigIntegerRangeField, FloatRangeField | DB에서 NULL로 설정할 수 있으면 이용             | 위젯에서 해당 폼이 빈 값을 허용하길 원한다면 null=True와 함께 사용 |
| DatetimeRangeField, DateRangeField                       | DB에서 해당 값들을 NULL로 설정할 수 있다면 이용 | 위젯에서 해당하는 폼이 빈 값을 허용하기를 원할 경우 auto_now나 auto_now_add 이용하고 있으면 가능. null=True 함께 사용 |

##### 모델의 _meta API

원래 목적은 모델에 대한 부가적인 정보를 장고 내부적으로 이용하기 위함. 다음과 같은 이유로 사용됨

*   모델 필드의 리스트를 가져올 때
*   모델의 특정 필드의 클래스를 가져올 때(또는 상속 관계나 상속 등을 통해 생성된 정보를 가져올 때)
*   앞으로의 장고 버전들에서 이러한 정보를 어떻게 가져오게 되었는지 확실하게 상수로 남기기 원할 때

다음과 같은 상황에서 사용

*   장고 모델의 자체 검사 도구
*   라이브러리를 이용해서 특별하게 커스터마이징된 자신만의 장고를 만들 때 
*   장고 모델의 데이터를 조정하거나 변경할 수 있는 일종의 관리 도구를 제작할 때
*   시각화 또는 분석 라이브러리를 제작할 때. 예를 들어 'foo'라는 단어로 시작하는 필드에 대한 분석 정보

### 6.4 모델 매니저

모델에 질의를 하게 되면 장고의 ORM을 통하게 된다. 이때 모델 매니저라는 데이터베이스와 연동하는 인터페이스를 호출하게 된다. 모델 매니저는 클래스들을 제어하기 위해 모델 클래스의 모든 인스턴스 세트에 작동하게 된다. 장고는 `각 모델 클래스에 대한 기본 모델 매니저를 제공`하며 이를 `커스터마이징`할 수 있다.

```python
from django.db import models
from django.utils import timezone

class PublishedManager(models.Manager):
    
    user_for_related_fields = True
    
    def published(self, **kwargs):
        return self.filter(pub_date__lte=timezone.now(), **kwargs)
    
class FlavorReview(models.Model):
    review = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    
    # 커스텀 모델 매니저를 여기에 추가.
    objects = PublishedManager()
```

review가 몇 개인지, 게시된 게 몇 개인지 알고 싶으면 python shell에서 다음과 같이 한다.

from reviews.models import FlavorReview

FlavorReview.objects.count()

FlavorReview.objects.published().count()

안티패턴 : 기존 모델 매니저 교체하기

from reviews.models import FlavorReview

FlavorReview.objects.filter().count()

FlavorReview.published.filter().count()

이런 방법을 쓸 때 주의를 기울여야 하는 이유

1.  추상화 기초 클래스의 자식들은 부모 모델의 모델 매니저를 받게 되고 접합 기반 클래스들의 자식들은 그렇지 못하다.
2.  모델 클래스에 적용되는 첫번째 매니저는 장고가 기본값으로 취급하는 매니저다.

모델 클래스에서 objects = models.Manager()를 커스텀 모델 매니저 위에 일일이 정해줘야 한다.

### 6.5 거대 모델 이해하기

거대 모델 개념은 데이터 관련 코드를 뷰나 템플릿에 넣기보다는 모델 메서드, 클래스 메서드, 프로퍼티 심지어는 매니저 메서드 안에 넣어 캡슐화하는 것이다. 이럴 경우 어떤 뷰나 여타의 작업일지라도 같은 로직을 이용할 수 있다. 리뷰를 보여주는 모델이 있다면 다음 메서드를 덧붙일 수 있다.

*   Review.create_view(cls, user, ratings, title, description): 리뷰를 생성하는 class-method. HTML과 REST 뷰에서 호출되는 모델 클래스 그리고 스프레드시트를 처리하는 임포트 도구에서 호출된다.
*   review.product_average: 리뷰된 프로젝트의 평균 점수를 반환하는 리뷰 인스턴스의 속성. 리뷰 상세 뷰에 이용되며 사용자가 페이지를 떠나지 않고 평가 의견 전부를 알 수 있게 한다.
*   review.found_useful(self, user, yes): 해당 리뷰가 유용했는지 아닌지 사용자가 기록할 수 있는 메서드. 세부 항목 뷰와 리스트 뷰에서 HTML과 REST 구현에 둘 다 이용

거대 모델은 프로젝트 전체를 통해 코드 재사용을 개선할 수 있는 최고의 방법이다. 하지만 괜찮지만은 않다. 모든 로직을 모델 안으로 넣으면서 모델 코드의 크기가 폭발적으로 커지는 문제가 있다. 크기와 복잡성 때문에 이해하기 어렵고 테스트하거나 유지 보수 하기도 어렵다. 메서드들과 클래스 메서드, 프로퍼티들을 그대로 유지한 채 그것들이 지닌 로직들을 모델 행동이나 상태 없는 헬퍼 함수로 이전한다.

##### 모델 행동(믹스인)

모델 행동은 믹스인을 통한 캡슐화와 구성화의 개념으로 이루어져있다. 모델은 추상화 모델로부터 로직을 상속받는다.

##### 상태 없는 헬퍼 함수

모델로부터 로직을 떼어내 유틸리티 함수로 넣음으로써 독립적 구성 가능. 로직에 대한 테스트가 쉬워짐. 단점은 해당 함수들이 stateless여서 함수에 더 많은 인자가  필요하게 된다.

##### 모델 행동과 헬퍼 함수

두 개 다 완벽하지는 않다.

### 6.6 요약

모델은 장고 프로젝트에서 기초가 된다. 신중하게 디자인해야 한다.

정규화를 시작하고 다른 선택지를 충분히 고려하고 나서도 방법이 없을 때 비정규화를 고려한다. raw SQL을 적용하여 복잡한 쿼리를 단순화할 수도 있을 것이다. 적절한 장소에서 캐시를 써서 성능 문제를 해결할 수도 있을 것이다.

인덱스를 써라.

모델 간의 상속을 하려면 접합 모델(concrete model)이 아닌 추상화 기초 클래스로부터 상속한다.

모델에서 null=True와 blank=True 옵션을 쓸 때는 주의한다.

거대 모델은 로직을 모델 안에 캡슐화해서 넣는 방법으로 모델 전부를 신의 객체(god object)로 만들어 버릴 위험도 있다.


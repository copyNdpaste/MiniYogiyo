# Two Scoops of Django

## 7장 쿼리와 데이터베이스 레이어

장고는 여러 종류의 각기 다른 데이터를 데이터베이스 종류와는 독립적인 형태로 객체화한다. 그리고 생성된 객체에 상호 작용할 수 있도록 메서드 세트를 제공한다. 장고 ORM은 때때로 예상과는 다른 결과를 보여주기도 한다.

### 7.1 단일 객체에서 get_object_404() 이용하기

단일 객체를 가져와서 작업하는 세부 페이지 같은 뷰에서 get() 대신 사용한다.

>   get_object_404()는 뷰에서만 이용
>
>   *   헬퍼 함수, 폼, 모델 메서드, 뷰를 제외한 다른 곳 그리고 뷰와 직접적으로 관련된 곳이 아닌 곳에서는 이용하지 말자.

### 7.2 예외를 일으킬 수 있는 쿼리를 주의하자

단일 모델 인스턴스에서 get_object_404()를 이용할 때는 try-except 블록으로 예외 처리를 할 필요가 없다. get_object_404()가 처리한다.

이를 제외한 경우 try-except를 이용한 예외 처리를 해야 한다.

##### ObjectDoesNotExist와 DoesNotExist

ObjectDoesNotExist는 어떤 모델 객체에도 이용할 수 있지만 DoesNotExist는 특정 모델에서만 이용할 수 있다.

```python
from django.core.exceptions import ObjectDoesNotExist

from flavors.models import Flavor
from store.exceptions import OutOfStock

def list_flavor_line_item(sku):
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0)
    except Flavor.DoesNotExist:
        msg = "We are out of {0}".format(sku)
        raise OutOfStock(msg)

def list_any_line_item(model, sku):
    try:
        return model.objects.get(sku=sku, quantity__gt=0)
    except ObjectDoesNotExist:
        msg = "We are out of {0}".format(sku)
        raise OutOfStock(msg)
```

##### 여러 개의 객체가 반환되었을 때

쿼리가 하나 이상의 객체를 반환할 수도 있다면 MultipleObjectsReturned 예외를 참고. 

```python
from flavors.models import Flavor
from store.exceptions import OutOfStock, CorruptedDatabase

def list_flavor_line_item(sku):
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0)
    except Flavor.DoesNotExist:
        msg = "We are out of {}".format(sku)
    	raise OutOfStock(msg)
    except Flavor.MultipleObjectsReturned:
        msg = "Multiple items have SKU {}. Please fix".format(sku)
        raise CorruptedDatabase(msg)
```

### 7.3 쿼리를 좀 더 명확하게 하기 위해 지연 연산 이용하기

복잡한 쿼리의 경우 몇 줄 안되는 코드에 너무 많은 기능을 엮어서 기술하는 것을 피해야 한다.

`지연 연산` 은 데이터가 정말로 필요하기 전까지는 장고가 SQL을 호출하지 않는 특징이다. 따라서 ORM 메서드와 함수를 얼마든지 원하는 만큼 연결해서 코드를 쓸 수 있다. 결과를 실행하기 전까지 장고는 실제 데이터베이스에 연동되지 않는다. 한 줄에 여러 메소드와 데이터베이스의 각종 기능을 엮어 넣는 대신에, 여러 줄에 걸쳐 나눠 쓸 수 있다.

```python
from django.models import Q  # or 연산 시 사용

from promos.models import Promo

def fun_function(**kwargs):
    results = Promo.objects.active()
    results = results.filter(
    			Q(name__startswith=name)|
        		Q(description__icontains=name)
    			)
	results = results.exclude(status='melted')
    results = results.select_related('flavors')
    return results
```

### 7.4 고급 쿼리 도구 이용하기

장고의 ORM은 배우기 쉽고 직관적이며 다양한 경우를 처리할 수 있다. 하지만 ORM이 모든 걸 다 처리할 수는 없다. 그렇다고 파이썬을 사용하여 데이터를 가공하지 말고 장고의 고급 쿼리 도구를 이용한다.

##### 쿼리 표현식

데이터베이스에서 읽기 작업이 수행될 때 쿼리 표현식은 해당 읽기가 실행되는 동안 값을 산출해내거나 연산을 수행하는 데 이용될 수 있다.

쿼리 표현식을 이용하지 않고 처리하는 방법

```python
# 나쁜 예
from models.customers import Customer

customers = []
for customer in Customer.objects.iterate():
    if customer.scoops_ordered > customer.store_visits:
        customers.append(customer)
```

안좋은 점

*   DB 안의 모든 고객 레코드에 대해 하나하나 파이썬을 이용한 루프가 돌고 있다. 느리고 메모리 사용도 많다.
*   코드 자체가 경합 상황(공유 자원에 대해 여러 프로세스가 동시 접근)에 직면한다. 이 코드는 사용자가 데이터와 상호 교류하는 동시에 실행되는 코드다. UPDATE가 처리되는 환경에서라면 분실이 생길 여지가 있다.

```python
from django.db.models import F
from models.customers import Customer
customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
```

위 코드는 DB 자체 내에서 해당 조건을 비교하는 기능을 가지고 있다. 내부적으로 다음과 같은 코드를 실행한다.

>   SELECT * from customers_customer where scoops_ordered > store_visits

쿼리 표현식은 프로젝트의 안전성과 성능을 대폭 향상시켜준다.

##### 데이터베이스 함수들

장고 1.8에서 UPPER(), LOWER(), COALESCE(), CONCAT(), LENGTH(), SUBSTR() 등의 일반적인 데이터베이스 함수를 이용할 수 있다.

1.  이용이 쉽고 간결.
2.  데이터베이스 함수들은 로직을 파이썬 코드에서 데이터베이스로 더 많이 이전할 수 있게 해준다. 파이썬으로 데이터 처리하는 것보다 빠르다.
3.  데이터베이스 함수들은 데이터베이스별로 다르게 구현되어 있지만 장고의 ORM은 이를 하나로 통합.
4.  데이터베이스 함수들은 쿼리 표현식이기도 하다. 장고 ORM에서 구현해 놓은 또 다른 종류의 일반적인 패턴을 가진 쿼리 표현식이 된다.

### 7.5 필수불가결한 상황이 아니라면 로우 SQL은 `지양`하자.

ORM이라는 관계형 매핑은 매우 높은 생산성을 제공한다. 쿼리뿐만아니라, 모델에 대한 접근과 업데이트를 할 때 유효성 검사와 보안을 제공한다. raw SQL을 쓰면 이식성이 떨어진다.

특정 DB에 종속된 SQL 쿼리를 작성했다면 데이터베이스 마이그레이션 과정에서 매우 복잡한 문제가 생긴다.

##### 언제 raw SQL을 써야 할까?

rarw SQL을 직접 이용함으로써 코드가 월등히 간결해지는 경우.

### 7.6 필요에 따라 인덱스를 이용하자

언제 추가해야 하는 지 판단이 필요하다.

1.  인덱스가 빈번하게(모든 쿼리의 10~25% 사이에서) 이용될 때
2.  실제 데이터 또는 실제와 비슷한 데이터가 존재해서 인덱싱 결과에 대한 분석이 가능할 때.
3.  인덱싱을 통해 성능 향상되는지 테스트할 수 있을 때

>   PostgreSQL을 이용할 때 pg_stat_activity는 실제로 어떤 인덱스들이 이용되는 지 알려준다.

### 7.7 트랜잭션

장고 1.8부터 기본적으로 ORM이 모든 쿼리를 호출할 때마다 자동으로 커밋하게 되었다. .create()나 .update()가 호출될 때마다 SQL 데이터베이스 값들이 실제로 변한다. 장점은 ORM을 이해하기 수월해진 것이다. 단점은 뷰에서 둘 이상의 데이터베이스 수정이 요구될 때 첫 번째 수정은 문제가 없었지만 두 번째 수정에서 문제가 발생해 데이터베이스상의 충돌이 일어날 위험이 존재하게 되었다는 것이다.

이런 문제를 해결하기 위해 트랜잭션(단일화된 작업)을 이용한다. 특성 ACID.

프로젝트에서 직관적인 패턴의 데코레이터와 콘텍스트 매니저를 이용하여 데이터베이스의 일관성 관리가 매우 쉬워졌다.

##### 각각의 HTTP 요청을 트랜잭션으로 처리하라

```python
# settings/base.py

DATABASES = {
    'default': {
        # ...
        'ATOMIC_REQUESTS': True,
    },
}
```

장고에서는 ATOMIC_REQUESTS 설정을 통해 모든 웹 요청을 트랜잭션으로 쉽게 처리할 수 있다. 값을 True로 설정함으로써 읽기 데이터를 포함한 모든 요청이 트랜잭션으로 처리되게 할 수 있다. 장점은 뷰에서의 모든 데이터베이스 쿼리가 보호되는 안정성을 얻을 수 있다는 것. 단점은 성능 저하를 가져올 수 있다는 것.

ATOMIC_REQUESTS를 이용할 때 주의할 점은 오직 에러가 발생하고 나서야 데이터베이스 상태가 롤백된다는 것이다.

```python
# flavors/views.py
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Flavor

@transaction.non_atomic_requests
def posting_flavor_status(request, pk, status):
    flavor = get_object_or_404(Flavor, pk=pk)
    
    # 여기서 오토커밋 모드가 실행될 것이다.
    flavor.latest_status_change_attempt = timezone.now()
    flavor.save()
    
    with transaction.atomic():
        # 이 코드는 트랜잭션 안에서 실행된다.
        flavor.status = status
        flavor.latest_status_change_success = timezone.now()
        flavor.save()
        return HttpResponse("Hooray")
    # 트랜잭션이 실패하면 해당 상태 코드를 반환한다.
    return HttpResponse("Sadness", status_code=400)
```

##### 명시적 트랜잭션 선언

사이트 성능을 개선하는 방법 중 하나다. 트랜잭션에서 어떤 뷰와 비즈니스 로직이 하나로 엮여 있고, 어떤 것이 그렇지 않은지 명시해 주는 것이다.

*   DB에 변경이 생기지 않는 DB 작업은 트랙잭션으로 처리하지 않는다.
*   DB에 변경이 생기는 DB 작업은 반드시 트랜잭션으로 처리한다.
*   DB 읽기 작업을 수반하는 DB 변경 작업 또는 DB 성능에 관련된 특별한 경우에는 앞의 두 가이드라인을 모두 고려한다.

| 목적            | ORM 메서드                                                   | 트랜잭션을 이용할 것인가? |
| --------------- | ------------------------------------------------------------ | ------------------------- |
| 데이터 생성     | .create(), .bulk_create(), .get_or_create()                  | yes                       |
| 데이터 가져오기 | .get(), .filter(), .count(), .iterate(), .exists(), .exclude(), .in_bulk() |                           |
| 데이터 수정하기 | .update()                                                    | yes                       |
| 데이터 지우기   | .delete()                                                    | yes                       |

>   독립적인 ORM 메서드 호출을 트랜잭션 처리하지 말자
>
>   장고의 ORM은 데이터의 일관성을 위해 내부적으로 트랜잭션을 이용한다. 접합 상속으로 인해 업데이트가 여러 테이블에 걸쳐 영향을 준다고 할 때 장고는 이를 트랜잭션으로 처리한다.
>
>   독립적 ORM 메서드 .create(), .update(), .delete()를 트랜잭션 처리하는 건 유용하지 않다. 대신 여러 ORM 메서드들을 뷰나 함수 또는 메서드 내에서 호출할 때 트랜잭션을 이용한다.

##### django.http.StreamingHttpResponse와 트랜잭션

뷰가 django.http.StreamingHttpResponse를 반환한다면 일단 응답이 시작된 이상 트랜잭션 에러를 중간에 처리하기란 불가능하다. 프로젝트에서 이 응답 메서드가 쓰이고 있다면 ATOMIC_REQUESTS가 다음 중 하나를 따라야 한다.

1.  ATOMIC_REQUESTS의 장고 기본값을 False로 설정. 그리고 위 `명시적 트랜잭션 선언` 에 있는 기술 고려
2.  뷰를 django.db.transaction.non_atomic_requests 데코레이터로 감싸 본다.

ATOMIC_REQUESTS를 스트리밍 응답과 같이 쓸 수 있지만 트랜잭션은 뷰에서만 적용된다. 스트림 응답이 추가적인 SQL 쿼리를 생성했다면 오토커밋 모드에서일 것이다.

##### MySQL에서의 트랜잭션

DB 타입이 InnoDB이냐 MyISAM이냐에 따라 트랜잭션 지원이 될 수도, 안 될 수도 있다. 트랜잭션이 지원되지 않는다면 늘 오토커밋 모드로 작동한다.

### 7.8 요약

프로젝트 데이터를 쿼리하는 여러 방법. 어떻게 데이터를 저장하는 지 알아 봤다. 다음은 데이터를 어떻게 나타내는지 알아야 한다. 다음은 뷰에 대해 공부한다.
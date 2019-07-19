## Chapter 2 함수

### Better way 15 클로저가 변수 스코프와 상호 작용하는 방법을 알자.

### 핵심정리

* 클로저 함수는 자신이 정의된 스코프 중 어디에 있는 변수도 참조할 수 있다.
* 기본적으로 클로저에서 변수를 할당하면 바깥쪽 스코프에는 영향을 미치지 않는다.
* 파이썬 3에서는 nonlocal문을 사용하여 클로저를 감싸고 있는 스코프의 변수를 수정 할 수 있음을 알린다.



숫자 리스트를 정렬할 때 특정 그룹의 숫자들이 먼저 오도록 우선순위를 매기려고한다

이런 패턴은 사용자 인터페이스를 표현하거나, 다른 것보다 중요한 메시지나 예외 이벤트를 먼저 보여줘야 할 때 유용하다.

```python 
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (1, x)
        return (2,x)
    values.sort(key=helper)
    
numbers = [8,3,1,2,5,4,7,6]
group = {2,3,5,7}
sort_priority(numbers, group)
print(numbers)
```

```shell
>>> [2, 3, 5, 7, 1, 4, 6, 8]
```

함수가 예상대로 동작한 이유는 세가지 이다.

* 파이썬은 클로저를 지원
* `클로저`란
    * 자신이 정의된 스코프에 있는 변수를 참조하는 함수
    * 그래서 `helper` 함수가 sort_priority의 group 인수에 접근할 수 있다.
* 함수는 파이썬에서 일급 객체 이다.
    * 함수를 직접 참조하고, 변수에 할당하고, 다른 함수의 인수로 전달하고, 표현식과 if 문 등에서 비교할 수 있다는 의미
    * sort 메소드에서 클로저 함수를 key 인수로 받을 수 있다.
* 파이썬에는 튜플을 비교하는 특정한 규칙이 있다.
    * 인덱스 0으로 아이템을 비교하고, 그 다음으로 인덱스 1, 인덱스2 와 같이 진행
    * **helper 클로저의 반환 값이 정렬 순서를 분리된 두 그룹으로 나뉘게 한건 이 규칙 때문**
        * (1, x) , (2,x) 
            * 이런 식으로 나뉠 때, (1, x) 에 해당하는게 우선순위를 가진다는 말이다.

```python
def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

found = sort_priority2(numbers, group)
print('Found:', found)
print(numbers)
```

```shell
>>>
Found: False
[2, 3, 5, 7, 1, 4, 6, 8]
```

정렬 결과는 올바르지만 found가 틀리게 나온 이유는

* 표현식에서 변수를 참조할 때 파이썬 인터프리터는 참조를 해결하려고 다음과 같은 순서로 스코프를 탐색한다.

    1. 현재 함수의 스코프
    2. (현재 스코프를 담고 있는 다른 함수 같은) 감싸고 있는 스코프
    3. 코드를 포함하고 있는 모듈의 스코프(전역 스코프)
    4. (len이나, str 같은 함수를 담고 있는) 내장 스코프

    이중 어느 스코프에도 참조한 이름을 ㅗ된 변수가 정의되어 있지 않으면 NameError 예외가 발생

* 변수에 값을 할당할 때는 다른 방식으로 동작, 변수가 이미 현재 스코프에 정의되어 있다면, 새로운 값을 얻는다.

* 새로 정의되는 변수의 스코프는 그 할당을 포함하고 있는 함수가된다.(`helper()`)

    * found 변수는 helper 클로저에서 True로 할당된다. 클로저 할당은 sort_priority2에서 일어나는 할당이 아닌 helper 안에서 일어나는 새 변수 정의로 처리된다.



#### 데이터 얻어오기

```python
def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

found = sort_priority3(numbers, group)
print('Found:', found)
print(numbers)
```

```shell
Found: True
[2, 3, 5, 7, 1, 4, 6, 8]
```

* 파이썬 3에서는 클로저에서 데이터를 얻어오는 특별한 문법이 있는데, `nonlocal` 문은 특정 변수 이름에 할당할 때, 스코프 탐색이 일어나야 함을 나타낸다.

* nonlocal이 모듈 수준 스코프까지는 탐색할 수 없다는 점

* nonlocal은 클로저에서 데이터를 다른 스코프에 할당하는 시점을 알아보기 쉽게 해준다.

* 전역 변수의 안티패턴과 마찬가지로 간단한 함수 이외에는 nonlocal을 사용하지 않도록 한다.

* nonlocal을 사용할 때 복잡해지기 시작하면 헬퍼 클래스로 상태를 감싸는 방법을 이용하는게 좋다.

    ```python
    class Sorter(object):
        def __init__(self, group):
            self.group = group
            self.found = False
            
        def __call__(self, x):
            if x in self.group:
                self.found = True
                return (0, x)
           	return (1, x)
        
        
    sorter = Sorter(group)
    numbers.sort(key=sorter)
    assert sorter.found is True
    ```



* #### 
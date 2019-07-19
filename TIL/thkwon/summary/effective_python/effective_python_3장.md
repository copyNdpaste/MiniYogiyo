## Chapter 3 클래스와 상속

### Better way 22 딕셔너리와 튜플보다는 헬퍼 클래스로 관리하자

### 핵심정리

* 다른 딕셔너리나 긴 튜플을 값을 담은 딕셔너리를 생성하지 말자.
* 정식 클래스의 유연성이 필요 없다면 가벼운 불변 데이터 컨테이너에는 namedtuple을 사용하자.
* 내부 상태를 관리하는 딕셔너리가 복잡해지면 여러 헬퍼 클래스를 사용하는 방식으로 관리 코드를 바꾸자.

```python
class SimpleGradebook(object):
    def __init__(self):
        self._grades = {}
        
    def add_student(self, name):
        self._grades[name] = []
    
    def report_grade(self, name, score):
        self._grades[name].append(score)
        
    def avereage_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)
```



```python
book = SimpleGradebook()
book.add_student('Isaac Newton')
book.report_grade('Isaac Newton', 90)

print(book.avereage_grade('Isaac Newton'))

# 90.0
```



```python
class BySubjectGradebook(object):
    def __init__(self):
        self._grades = {}
        
    def add_student(self, name):
        self._grades[name] = {}
        
    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)
    
    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count
```

```python 
book = BySubjectGradebook()
book.add_student('thkwon')
book.report_grade('thkwon', 'math', 100)
book.report_grade('thkwon', 'math', 90)
book.report_grade('thkwon', 'gym', 90)
book.report_grade('thkwon', 'gym', 80)
print(book.average_grade('thkwon'))

# 90.0
```



여기서 요구사항이 바껴서 수업의 최종 성적에서 각 점수가 차지하는 비중을 매겨서, 중간고사와 기말고사를 쪽지시험보다 중요하게 만들려고한다. 이 기능을 구현하는 방법 중 하나는 가장 안쪽 딕셔너리를 변경해서 과목(키)을 성적(값)에 매핑하지 않고, 성정과 비중을 담은 튜플(score, weight)에 매핑하는 것이다.

```python
class BySubjectGradebook(object):
    def __init__(self):
        self._grades = {}
        
    def add_student(self, name):
        self._grades[name] = {}
        
    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append((score, weight))
    
    def average_grade(self, name):
        by_subject = self._grades[name]
        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, totla_weight = 0, 0
            for score, weight in scores:
                # ...
        return score_sum / score_count
```

```python
book.report_grade('thkwon', 'math', 80, 0.10)
```

*   위와 같이 복잡해지면 딕셔너리와 튜플 대신 클래스의 계층 구조를 하면된다.
*   파이썬의 내장 딕셔너리와 튜플 타입을 쓰면 내부 관리용으로 층츠이 타이비을 추가하는게 쉽다. 하지만, 계층이 한 단계가 넘는 중첩은 피해야 한다.
    *   딕셔너리를 담은 딕셔너리는 쓰지 말아야 한다.
    *   여러 계층으로 중첩하면 코드를 이해하기 어렵고 유지보수가 힘들다.
*   관리가 복잡하다고 느끼는 즉시 클래스로 옮겨가야 한다.



#### 클래스 리팩토링

```python 
grades = []
grades.append((95, 0.45))
# ...

total = sum(score * weight for score, weight in grades)
total_weight = sum(weight for _, weight in grades)
average_grade = total / total_weight
```

* '_'

    *   파이썬에서는 관례적으로 사용하지 않을 변수에 밑줄 변수 이름을 쓴다.

* 튜플이 점점 길게 확장하는 패턴 또한 아이템이 두 개를 넘어가면 다른 방법을 고려해야한다.

    *   `collections` 모듈의 `namedtuple`이 쓰면된다.
    *   `namedtuple` 을 이용하면 작은 불변 데이터 클래스(immutable data class)를 쉽게 정의할 수 있다.

    ```python 
    import collections
    Grade = collections.namedtuple('Grade', ('score', 'weight'))
    ```

```python 
class Subject(object):
    def __init__(self):
        self._grades = []
        
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))
        
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight
    
    
class Student(object):
    def __init__(self):
        self._subjects = {}
        
    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]
    
    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count
    
    
class Gradebook(object):
    def __init__(self):
        self._students = {}
        
    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]
    
book = Gradebook()
albert = book.student('Albert Einstein')
math = albert.subject('math')
math.report_grade(80, 0.10)
math.report_grade(90, 0.10)
math.report_grade(74, 0.2)

print(albert.average_grade())

# 79.5
```



#### namedtuple

>   튜플의 성질을 가졌지만 항목에 이름으로 접급 가능하다.

* 튜플은 항목에 인덱스로 접근하므로 직관적이지 않다.

    * my_tuple[0], my_tuple[1], my_tuple[2], ...

    * but, namedtuple

        *   my_tuple.name , mytuple.age .. 로 접근 가능하다.

        ```python 
        from collections import namedtuple
        
        pin_info = namedtuple('card', 'name age phone_num')
        thkwon = pin_info('thkwon', 30, '010-7331-4120')
        
        ```

        ```python
        thkwon.name # 'thkwon'
        thkwon.age # 30
        thkwon.phone_num # '010-7331-4120'
        
        # 위와 같이 접근 가능하다.
        ```

        >   여기서 중요한 점은 이렇게 만들어진 namedtuple 객체 thkwon은 클래스로부터 만들어졌지만 튜플처럼 속성을 변경하거나 추가할 수 없다는 것이다.

        *   단지 클래스처럼 속성에 접근이 가능하고 인덱스로도 속성에 접근이 가능하다.
        *   클래스와 튜플을 짬봉해놓은 느낌
        *   불변 자료형들은 성능상의 이점이 있기 때문에 수정할 필요가 없다면 사전 대신 namedtuple을 사용하는 것은 좋은 판단이다.





### Better way 23 인터페이스가 간단하면 클래스 대신 함수를 받자.

### 핵심정리

* 파이썬에서 컴포넌트 사이의 간단한 인터페이스용으로 클래스를 정의하고 인스턴스를 생성하는 대신에 함수만 써도 종종 충분하다.
* 파이썬에서 함수와 메서드에 대한 참조는 일급이다. 즉, 다른 타입처럼 표현식에서 사용할 수 있다.
* `__call__` 이라는 특별한 메쏘드는 클래스의 인스턴스를 일반 파이썬 함수처럼 호출할 수 있게 해준다.
* 상태를 보존하는 함수가 필요할 때 상태 보존 클로저를 정의하는 대신 `__call__` 메쏘드를 제공하는 클래스를 정의하는 방안을 고려하자.



파이썬 내장 API의 상당수에는 함수를 넘겨서 동작을 사용자화하는 기능이 있다.

API는 이런 hook 을 이용해, 작성한 코드를 실행 중에 호출한다.

```python 
names = ['Kwon','Tae','Hyoung','hohoho']
names.sort(key=lambda x: len(x))
print(names)
```

```shell
>>> ['Tae', 'Kwon', 'Hyoung', 'hohoho']
```

* 파이썬의 hook 중 상당수는 인수와 반환 값을 잘 정의해놓은 단순히 상태가 없는 함수
* 함수가 hook로 동작하는 이유는 파이썬이 일급함수를 갖추었기 때문

```python
current = {'green': 12, 'blue': 3}
increments = [
    ('red', 5),
    ('blue', 15),
    ('orange', 9),
    ('black', 7),
]

def increment_with_report(current, increments):
    added_count = 0
    
    def missing():
        nonlocal added_count
        added_count += 1
        return 0
    
    result = defaultdict(missing, current)

    for key, amount in increments:
        result[key] += amount
        
    return result, added_count
```

```shell
result,count = increment_with_report(current, increments)
assert count == 3
```

* 위 방법은 간단한 함수를 인터페이스용으로 사용할 때 얻을 수 있는 이점이 있지만
* 상태가 없는 함수의 예제보다 이해하기 어렵다는 점이다.
* 다른 방법으로는 보존할 상태를 캡슐화하는 작은 클래스를 정의하는 것이다.



```python 
class CountMissing(object):
    def __init__(self):
        self.added = 0
    def missing(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter.missing, current)

for key, amount in increments:
    result[key] += amount
assert counter.added == 3
```

* 위의 코드 보다 클로저의 동작을 제공하는 방법이 명확하지만
* 클래스 자체만으로는 용도가 무엇인지 바로 이해하기 어렵다.
* 파이썬에서는 클래스에 `__call__`이라는 특별한 메서드를 정희해서 이런 상황을 명확히 할 수 있따.
* `__call__` 메서드는 객체를 함수처럼 호출할 수 있게 해준다. 



```python
class BetterCountMissing(object):
    def __init__(self):
        self.added = 0
        
    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
result = defaultdict(counter, current)
for key, amount in increments:
    result[key] += amount
print(counter.added)
assert counter.added == 3
```

* 위는 `BetterCountMissing 인스턴스`를 `defaultdict`의 기본값 후크로 사용하여 딕셔너리에 없어서 새로 추가된 키의 개수를 알아내는 코드이다.

> 위의 예제가 `CountMissing.missing` 예제보다 명확하다. `__call__` 메서드는 API Hook 처럼 함수 인수를 사용하기 적합한 위치에 클래스의 인스턴스를 사용할 수 있다는 사실을 알려준다.
>
> 이 코드를 처음 보는 사람을 클래스의 주요 동작을 책임지는 진입점으로 안내하는 역할도 한다.
>
> * 클래스의 목적이 상태 보존 클로저로 동작하는 것이라는 강력한 힌트를 제공한다.
>
> 무엇보다도 `__call__` 을 사용할 때 `defaultdict`는 여전히 무슨 일이 일어나는지 모른다.` defaultdict`에 필요한건 기본값 hook 용 함수 뿐이다. 파이썬ㅇ른 하고자 하는 작업에 따라 간단한 함수 인터페이스를 충족하는 다양한 방법을 제공한다.
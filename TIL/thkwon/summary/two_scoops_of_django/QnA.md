## 잘 모르는 개념 or 다시 한번 봐야 하는 주제들

### 6장

- [ ] 모델 상속의 패턴 예제 익히기
    - 멀티테이블 상속을 왜 쓰면 안되는지 잘 이해가 되지 않았다.
- [ ] 프락시 모델
    - 설명 만으로는 무엇인지 잘 이해가 안된다.
- [ ] 접합 기반의 모델 클래스
    - 접합 기반의 상속은 심각한 성능 문제를 일ㄹ으킬 소지가 있다는 무슨 말인가?
- [ ] `sqlmigrate` 명령어 사용법
    - 사용법에 대해서 숙지
- [ ] `MIGRATION_MODULES`
    - 처음알게된 개념인데 내용에 대해서 잘 모른다.
- [ ] MySQL 에서 migrations 과 관련한 주의 사항들
- [ ] Generic relation에서 **'다른 테이블에 존재하지 않는 레코드를 참조할 수 있는 데이터 충돌의 위험성이 존재'** 의 의미
- [ ] 모델 매니저를 사용할 때, 주의할 사항에 대해서 예제와 함께 이해가 필요하다.
- [ ] 믹스인에 대한 깊이 있는 내용
- [ ] 상태 없는 헬퍼 함수에 대한 깊이 있는 내용

### 8장

- [ ] locals() 란 무엇인가

    - 함수 내 지역변수들을 dict로 만들어 반환해준다.

    ```python 
    def locals_test_func():
    a = 1
    b = 2
    c = 3
    result = locals()
    return result
    ```

    ```shell
    >>> print(locals_test_func())
    >>> {'c':3, 'b':2, 'a':1}
    ```



### 9장

- [ ] CBV에서 dispatch 메소드의 역할은?
- [ ] `functools.wraps()` 는 무엇인가?
- [ ] `Middlewrae.process_request()`
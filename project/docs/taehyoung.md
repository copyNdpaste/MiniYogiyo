## DB 최적화

가장 기본적인 DB 최적화

1. index
2. field의 타입들을 알맞게 정의하는 것



### QuerySet의 특징

1. QuerySet은 게으르다.

    * 코드 상에서, QuerySet을 생성하는 작업은 DB에 아무런 작업을 진행하지 않는다.
    * DB의 쿼리는 실제로 쿼리셋이 결과 값이 연산되기 전까지 실행되지 않는다.
    * 즉, filter를 계획 적용하더라도 DB 쿼리는 일어나지 않는다.

2. QuerySet의 결과값이 연산되는 순간들

    * Iteration( for loop)
    * Slicing
        * Step 파라미터를 사용할 때,
    * Pickling / Caching
    * repr()
    * len()
    * list()
    * bool()

3. 쿼리셋 캐싱

    * 쿼리셋이 연산되면 그 결과 값은 메모리에 캐싱된다.

    * 같은 쿼리셋을 연산하려고하면 캐시된 값이 다시 불려온다.

    * 캐싱이 사용되는 순간

        * callable하지 않은 속성들의 값은 캐시가 된다.

            ```python
            # callable 하지 않은 속성들
            entry = Entry.objects.get(id=1)
            entry.blog # BLog 객체가 DB에서 불려옴
            entry.blog  # Blog 객체가 DB가 아닌 캐시에서 불러옴
            
            # callable한 mehtod들
            entry = Entry.objects.get(id=1)
            entry.authors.all() # DB 쿼리가 진행됨
            entry.authors.all() # DB 쿼리가 다시 한번 진행됨
            ```

            * 커스텀으로 생성한 property들은 cached_property 데코레이터를 사용해서 캐시되게 할 수 있다.
            * iterator()를 사용함으로써 캐시가 Queryset 단에서 진행되는 것을 방지할 수 있다. 
            * 만약 Queryset이 많은 데이터를 가지고 있다면 효율적인 퍼포먼스와 메모리 사용량을 iterator를 통해 확복 가능

    * 캐싱이 사용되지 않는 순간

        * 쿼리셋의 일부만 연산된다면, 캐시된 값이 있는지 확인은 하지만, 결과 값을 새로 캐시 하지 않고,
        * 이전에 쿼리셋의 전체가 연산된 경우가 있다면 그떄 생성된 캐시값을 사용한다.



4. DB에서 가능한 작업은 DB에서 직접 진행

    * filter와 exclude를 이용해 DB에서 직접 원하는 값을 필터링
    * F expression을 사용, DB에서 Python 메모리에 값을 가져오지 않고 바로 DB연산을 진행할 수 있음

5. 필요 없는 것은 가져오지 않는다.

    * Queryet.values()와 values_list()
        * ORM 모델의 객체가 필요 없고 값들만 필요하다면, QuerySet.values()나 values_list()를 사용하자

6. QuerySet.count()와 exists()

    * len() 보다는 count, if query_set 보다는 exists를 사용하면 좋다.

    * 그러나 너무 과하게 쓰지 말아야하며, 언젠가 데이터가 필요하다면, 그냥 Queryset을 연산하는 것이 좋다.

        ```python
        if right_condition:
        	# QuerySet의 laziness덕분에 right_condition이 참이 아니면 DB에 접속하지 않음
        	this_query = user.filter(some_condition)
        	if this_query:
        		# 만약 모델의 값이 존재한다면 어짜피 사용해야함으로 `exists`보다 그냥 DB query를 실행시키는 것이 좋음
        		print("you have {} queries".format(len(this_query)))
        		for cur_query in this_query:
        			do_something()
        	else:
        		print("You have no query")
        ```

        

7. ForeignKey 값은 직접 사용

    * 단지 외래키의 값만 필요할 경우, 관계된 객체를 통째로 가져오기 보다 이미 존재하는 외래키 값을 사용

    ```python
    # Good
    entry.blog_id # 이것은 blog의 id만 가져옴
    
    # bad
    entry.blog.id # 이것은 blog를 전부 다 가져와서 id를 가져온다.
    ```


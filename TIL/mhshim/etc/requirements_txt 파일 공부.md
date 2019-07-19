# requirements.txt 알아보기

각각의 환경에서 동일한 패키지를 사용하고 싶은 경우 유용하다. 패키지가 수십, 수백 개가 되면 일일이 pip install을 하기 힘들다. requirements.txt는 패키지 설치 자동화를 하는 역할을 한다.

> pyenv virtualenv 3.6.5 test1
>
> pyenv virtualenv 3.7.1 test2
>
> pyenv activate test1
>
> (test1) pip freeze  # package 설치 확인
>
> (test1) pip install —upgrade pip  # pip upgrade
>
> (test1) pip install django  # django 및 패키지 설치
>
> (test1) pip install django-crispy-forms
>
> (test1) pip install djangorestframework
>
> (test1) pip freeze  # test1에 설치된 목록 확인

##### requirements.txt 쓰는 이유??

패키지 개수가 많을 경우 pip install로 설치하기 힘들기 때문에 npm처럼 패키지를 관리하는 것이다. 설치 자동화를 위해 사용한다.

새로운 가상환경을 설치한 뒤 이 가상환경에 전에 쓰던 패키지들을 사용하고 싶으면 requirements.txt를 만든다. requirements.txt 파일은 프로젝트 디렉토리 상위(바깥)에 만든다.

> cd ..  # 상위 디렉토리(프로젝트 디렉토리의 상위)로 이동
>
> ##### (test1) pip freeze > requirements.txt  # 설치된 패키지들로 구성된 requirements.txt 생성하기

pyenv activate test2  # test2 가상환경 실행

> ##### (test2) pip install -r requirements.txt  # requirements.txt에 있는 패키지 설치
>
> ##### pip freeze | grep [PACKAGE] >> requirements.txt  # requirements.txt 뒤에 붙이기
>
> ##### pip freeze | grep django  # 패키지 중 django를 포함하는 문자열 찾아 출력하기


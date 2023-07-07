# KT AIVLE School 3기 AI Big Project 11조 Backend Repository

## 🌟 환경 세팅 
ec2에서 python venv를 사용할 것으로 venv로 가상환경을 세팅 

1. 작업할 폴더 만들고 들어가기  
    - ex)
    - `$ mkdir BigProject`
    - `$ cd BigProejct`
2. `$ git clone {url}`
3. `$ \Users\User\AppData\Local\Programs\Python\Python310\python -m venv .venv` : venv 생성 
    - venv 생성 기본 명령어 : `python -m venv .venv`  
    - 근데, python version을 통일하기 위해 python 3.10 version 다운 후 위의 명령어 실행
    - 명령어 앞의 `\Users\~~\python` 은 각자 python 설치 환경에 따라 달라질 수 있음
4. `$ cd Team11-Project-back` : 작업 폴더로 들어가기
5. `$ .venv\Scripts\activate.bat`
    - Windows의 경우는 위의 명령어로 가상환경 실행
    - `$ source venv/bin/activate` : linux 
    - 그럼 아나콘다 가상환경 처럼 앞에 (.venv) 가 붙을 것
6. `$ pip install -r requirements.txt` : 필요한 라이브러리 설치
7. `CREATE DATABASE BACKEND default CHARACTER SET UTF8;` : MYSQL 진입 후 BACKEND라는 이름의 DB 생성
8. `settings_params.py` 각자 환경에 맞게 세팅하고 `manage.py` 와 같은 위치에 두기
9. `$ python manage.py migrate` : models.py 를 db 에 반영

### 🌱 AWS EC2 가상환경 세팅
- python version : `Python 3.8.10`
1. `sudo apt install python3.8-venv` : venv 사용을 위해 다운
2. `python3 -m venv .venv` : 가상환경 생성
3. `source .venv/bin/activate` : 가상환경 활성화
4. `pip install --upgrade pip` : pip upgrade
5. `pip install -r requirements.txt`
6. `settings.py` 에서 `ALLOWED_HOST = ["*"]`
7. `nohup sudo /home/ubuntu/deploy/.venv/bin/python manage.py runserver 0:80&` : 백그라운드에서 서버 실행

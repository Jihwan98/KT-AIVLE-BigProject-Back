# 환경 세팅 
1. `git clone`
2. ~`$ conda install --file requirements.txt` : 패키지 설치~ => 추후 수정 예정
3. `CREATE DATABASE BACKEND default CHARACTER SET UTF8;`
MYSQL 진입 후 BACKEND라는 이름의 DB 생성
4. `$ python manage.py migrate` : models.py 를 db 에 반영

> 💡 settings_params.py 각자 환경에 맞게 세팅

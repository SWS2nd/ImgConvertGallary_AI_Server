- 구해줘(9조) 갤러리! 프로젝트 인공지능 서버용 원격 repository

# 🎨 유화제작 서비스(9해줘갤러리)

<br>

## 소개
<p style="font-size: 1.2rem;">
9해줘갤러리는 미술관을 컨셉으로 하여,체험(유화제작서비스:AI)을 하고 
체험한 결과물을 전시(혹은 저장:CRUD) 하고, 후기(comment:CRUD) 를 남길 수 있는 웹 서비스 이며, 이번 프로젝트에서는, 학습 내용의 복습 및 적용을 주 목적으로 정하였습니다.
</p>


<br>


## 📁 사용한 기술
<img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/0e2fe3e0-cc58-4a1a-b340-858718d8ce47/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220302%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220302T100511Z&X-Amz-Expires=86400&X-Amz-Signature=b819acb29217ec2ba71db38a1bde47af4fb697db0c74e0c6c9d8ea63a68b20be&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject" style="width: 66rem; height: 40rem; display: block; margin: 0 auto;">

- Django, Django-ninja
- Tensorflow
- Pytorch
- Javascript
- mySQL
- AWS: RDS, S3
<br>

# 🗞 프로젝세팅
- 패키지: requirements.txt


- 필요한 파일
  - local setting : db설정
  - .env : SECRETE_KEY 설정
    - 참고 : https://django-environ.readthedocs.io/en/latest/getting-started.html 


## 🗓 프로젝트기간
<p style="font-size: 1.1rem">
2022년 2월22일 ~ 2022년 3월3일
</p>

<br>


## 🧑‍💻👩‍💻 팀구성 및 역할 👨‍💻🧑‍💻
### 프론트
- 김재성님
  * 웹 디자인
  * 기능
    * 네비게이션 언더바 기능
    * Up 버튼 기능
    * 애니메이션 기능
    * Mac 버튼 기능
    * 자연스로운 스크롤 
    * 슬라이드
    * 스크롤 디자인 변경
    * 원형 스피너 적용
  
<br>

### 벡엔드 
- 이가을님
    * commentapp 기능구현
    * RDS생성
    * aws웹서버 

  <br>
  
- 김성연님
  * API문서 작성
  * Activityapp 기능구현
  
<br>

### 머신러닝
- 송원석님
  - 이미지 변환 인공지능 서버 담당
  - AWS EC2에 인공지능 서버 구축

<br>


<br>

## ❗주요기능
<br>

- 웹사이트의 이용은 누구나 할 수 있다.(비회원제)
  - Activty
    - 9개의 화풍 중 선택하거나, 직접 화풍이 될 이미지를 선택하여 이미지를 생성할 수 있다.
    - 생성한 이미지를 로컬에 저장 할 수 있고, 웹사이트에 결과물을 게시할 수 있다.
    - 저장된 결과물은 본인이 작성한 비밀번호를 통해서만 삭제 할 수 있다.
    - 생성된 이미지는 해당하는 화풍에따라 최신순으로 업데이트 된다.
  
    <br>
    
  - Comment
    - 댓글을 작성 할 때, 임의의 프로필 이미지가 함께 추가된다.
    - 삭제는 작성한 비밀번호를 통해서만 삭제 할 수 있다.
    - 페이지네이션을 통해 최신순의 댓글을 볼 수 있다.
    

<br>

- AI
  - 이미지의 화풍 변환이 가능하다.
  - 사용자로부터 입력받은 화풍용 이미지와 Mix 가능하다.


<br>



## 🔍 기획 
<img src="https://blog.kakaocdn.net/dn/dqKNrm/btruUoKW7Wj/bpCkIaDevkDHNAlSBCHWd0/img.png" style="width: 65rem; height: 55rem; display: block; margin: 0 auto;">

## 📖 API
👉 자세한 사항은 https://www.notion.so/API-fbf25514ace94bd7be1005588f38c64f

<img src="https://blog.kakaocdn.net/dn/b9vL1M/btruRLNnAD0/DqkvK4Smjrr43J5XuRT9g1/img.png" style="width: 55rem; height: 65rem;display: block; margin: 0 auto;">


## 💾 DB
👉 자세한 사항은 https://www.notion.so/DB-5270084d4247404290813dcee4727401

<img src="https://blog.kakaocdn.net/dn/bvSYaF/btruXT4gwKn/57xEhraDuQKXCMXPNBkSEk/img.png" style="width: 55rem; height: 59rem; display: block; margin: 0 auto;">

<br>

<br>

<br>

<br>



# 베이스 이미지로 Node.js 사용
FROM node:latest

# npm이 기본적으로 Node.js 이미지에 포함되어 있으므로 추가 설치가 필요하지 않음
# 만약 추가적인 설치가 필요하다면 아래 명령어를 활성화
RUN apt-get update && apt-get install -y npm

# 컨테이너가 실행될 때 기본으로 실행할 명령어 설정
CMD ["npm", "--version"]

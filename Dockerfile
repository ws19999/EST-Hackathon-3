# 베이스 이미지로 Python 3.8 사용
FROM python:3.8

# 작업 디렉토리를 /app으로 설정
WORKDIR /app

# 현재 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리로 복사
COPY . .

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt
CMD ["npm", "start"]

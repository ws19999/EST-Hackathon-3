# EST-Hackathon-3
# 편하게 여기서 작업해도 되고(파일명은 적당히..), 최종 파일만 커밋 및 동기화해서 버전 일치시키기!!
# 커밋 안하시면 개인한테만 보여요!!

# mysql 사용법
docker-compose up -d 누르고 docker ps 눌러서 container id 를 확인하고 docker exec -it <container_id> mysql -u example_user -p<example_user_password> 에 이용하기
mysql 종료할땐 exit

# sql 데이터 백업 중요중요!
docker exec -it mysql bash
mysqldump -u root --password=rootpassword mydatabase > /tmp/mydatabase_backup.sql
exit
docker cp mysql:/tmp/mydatabase_backup.sql /workspaces/EST-Hackathon-3/mysql_backup/mydatabase_backup.sql

# sql 데이터 다시 가져오는 방법!!
docker cp /workspaces/EST-Hackathon-3/mysql_backup/mydatabase_backup.sql mysql:/tmp/mydatabase_backup.sql
docker exec -it mysql bash
mysql -u root --password=rootpassword mydatabase < /tmp/mydatabase_backup.sql
exit



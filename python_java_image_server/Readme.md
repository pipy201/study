java_spring_src
---------------
controller /
Client.java
	파이썬 서버와 연결되는 소켓 클래스
	
FileSender.java
	파이썬 서버와 데이터를 전송하는 스트림 클래스
HandlerFile.java
	파일 객체
HomeController.java
	spring http request controller 클래스
view /
sendview.jsp
	웹 페이지. 이미지 촬영 및 업로드 가능

python_socket_server
--------------------
socket_server.py
	WAS와 연결되어 데이터 주고받는 소켓 객체

connector_predict.py
	이미지를 추론하는 tensorflow 클래스를 호출하는 커낵터 클래스

predict.py
	디스크에서 이미지를 읽어 추론 하는 tensorflow 클래스

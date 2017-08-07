Python socket, Java Spring 을 사용한 이미지 추론 서버
=====================================================
사용자가 웹 페이지에서 이미지를 업로드(촬영)하면 학습된 모델을 기반으로
이미지를 추론하여 결과를 반환 한다


java_spring_src
---------------
클라이언트와 Java Spring Framework 소스 파일


python_socket_server
--------------------
WAS에서 소켓으로 이미지 파일을 받아 Tensorflow 활용하여 추론 후 결과 반환

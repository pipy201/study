package com.client.web;

import java.net.Socket;

public class Client {
	Socket socket = null;
	String serverIp = "220.116.235.28";
	int serverPort = 5000;
	String fileName;
	String result;

	public Client(String fileName) {
		this.fileName = fileName;

		try {
			// 서버 연결
			socket = new Socket(serverIp, serverPort); // socket(),connect();
			System.out.println("서버에 연결되었습니다.");
			System.out.println(serverIp + " : " + serverPort);

			FileSender fileSender = new FileSender(socket, fileName);
			fileSender.start();
			fileSender.join();
			result = fileSender.getResult();
			System.out.println("result from server : " + result);
		} catch (Exception e) {
			e.printStackTrace();
		}// catch
	}
	
	public String getResult() {
		return result;
	}

}

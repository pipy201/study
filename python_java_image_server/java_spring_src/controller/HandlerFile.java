package com.client.web;

import java.io.File;
import java.io.IOException;
import java.net.URLEncoder;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import javax.servlet.http.HttpServletResponse;

import org.apache.commons.io.FileUtils;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

public class HandlerFile {
	   
	  private MultipartHttpServletRequest multipartRequest;
	  private String filePath;
	  private Map<String, List<String>> fileNames;
	  private String oldName;
	  private HttpServletResponse resp;
	  private byte[] fileByte;
	  
	  String fileFullPath;
	   
	  // upload
	  public HandlerFile(MultipartHttpServletRequest multipartRequest, String filePath) {
	    this.multipartRequest = multipartRequest;
	    this.filePath = filePath;
	    fileNames = new HashMap<String, List<String>>();
	  }
	  // down
	  public HandlerFile(HttpServletResponse resp, String filePath, String saveName, String oldName) {
	    this.resp = resp;
	    this.filePath = filePath + "/" + saveName;
	    this.oldName = oldName;
	  }
	  // delete
	  public HandlerFile(String filePath, String saveName) {
	    this.filePath = filePath + "/" + saveName;
	  }
	   
	  // upload
	  public Map<String, List<String>> getUploadFileName() {
	    upload();
	    return fileNames;
	  }
	  // down
	  public byte[] getDownloadFileByte() {
	    dowonload();
	    return fileByte;
	  }
	  // delete
	  public void deleteFileExecute() {
	    File file = new File(filePath);
	    if(file.exists()) {
	      file.delete();
	    }
	  }
	  
	  public String getFileFullPath() {
		  return fileFullPath;
	  }
	   
	  // 파일 업로드 처리
	  private void upload() {
	    Iterator<String> itr = multipartRequest.getFileNames();
	    List<String> oldNames = new ArrayList<String>();
	    List<String> saveNames = new ArrayList<String>();
	    StringBuffer sb = null;
	    while (itr.hasNext()) { // 받은 파일들을 모두 돌린다.
	      MultipartFile mpf = multipartRequest.getFile(itr.next());
	      sb = new StringBuffer();
	      String oldFileName = mpf.getOriginalFilename(); // 파일명
	      String saveFileName = sb.append(new SimpleDateFormat("yyyyMMddhhmmss")
	                              .format(System.currentTimeMillis()))
	                              .append(UUID.randomUUID().toString())
	                              .append(oldFileName.substring(oldFileName.lastIndexOf("."))).toString();
	      fileFullPath = filePath + "/" + saveFileName; // 파일 전체 경로
	      try {
	        // 파일 저장
	        mpf.transferTo(new File(fileFullPath));
	        oldNames.add(oldFileName);
	        saveNames.add(saveFileName);
	      } catch (Exception e) {
	        e.printStackTrace();
	      }
	    }
	    fileNames.put("oldNames", oldNames);
	    fileNames.put("saveNames", saveNames);
	  }
	  // down
	  private void dowonload() {
	    try {
	      fileByte = FileUtils.readFileToByteArray(new File(filePath));
	      resp.setContentType("application/octet-stream");
	      resp.setContentLength(fileByte.length);
	      // 다운로드시 변경할 파일명
	      resp.setHeader("Content-Disposition", "attachment; fileName=\""
	                                                           + URLEncoder.encode(oldName, "UTF-8") + "\";");
	      resp.setHeader("Content-Transfer-Encoding", "binary");
	    } catch (IOException e) {
	      e.printStackTrace();
	    }
	  }
	}

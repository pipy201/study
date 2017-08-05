package com.client.web;

import java.util.List;
import java.util.Map;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.multipart.MultipartHttpServletRequest;

/**
 * Handles requests for the application home page.
 */
@Controller
public class HomeController {

	private static final Logger logger = LoggerFactory.getLogger(HomeController.class);

	/**
	 * Simply selects the home view to render by returning its name.
	 */
	// @RequestMapping(value = "/", method = RequestMethod.GET)
	// public String home(Locale locale, Model model) {
	// logger.info("Welcome home! The client locale is {}.", locale);
	//
	// Date date = new Date();
	// DateFormat dateFormat = DateFormat.getDateTimeInstance(DateFormat.LONG,
	// DateFormat.LONG, locale);
	//
	// String formattedDate = dateFormat.format(date);
	//
	// model.addAttribute("serverTime", formattedDate );
	//
	// return "home";
	// }

	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home(Model model) {
		model.addAttribute("serverTime");
		return "sendView";
	}

	@RequestMapping(value = "/upload.do", method = RequestMethod.POST)
	public void fileUpload(MultipartHttpServletRequest multipartRequest, HttpServletResponse response) {
		// 추가데이터 테스트
		System.err.println(multipartRequest.getParameter("temp"));
		String filePath = "/tmp";

		HandlerFile handlerFile = new HandlerFile(multipartRequest, filePath);

		Map<String, List<String>> fileNames = handlerFile.getUploadFileName();
		// 실제저장파일명과 원본파일명 DB저장처리
		
		// 클라이언트 객체
		System.err.println(fileNames.toString());
		String fileName = handlerFile.getFileFullPath();
		Client client = new Client(fileName);
		String result = client.getResult();

		try {
			response.setContentType("text/html; charset=UTF-8");
			ServletOutputStream out = response.getOutputStream();
			out.println("<script>alert('Result : "+result+"');history.back()</script>");
			out.flush();
		} catch(Exception e) {
			e.printStackTrace();
		}// catch
	}// fileUpload

}

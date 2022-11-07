from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import requests 

url = "디스코드 웹 후크"
driver = webdriver.Chrome('크롬드라이버 주소')
#예 ) driver = webdriver.Chrome('C:/Users/USER/Desktop/stonline/selenium/chromedriver.exe')
driver.implicitly_wait(2)

driver.get("https://eclass.seoultech.ac.kr/ilos/main/member/login_form.acl")
driver.find_element_by_name('usr_id').send_keys('이클래스 아이디')
driver.find_element_by_name('usr_pwd').send_keys('이클래스 ')
driver.find_element_by_class_name('btntype').click()
num1 = 0

while True:
	driver.find_element_by_id('todoList_cnt').click()

	# 페이지 소스 가져오기
	html = driver.page_source

	# soup에 넣어주기
	soup = BeautifulSoup(html, 'html.parser')

	elements3 = soup.select('div.todo_date')
	elements1 = soup.select('div.todo_title')
	elements2 = soup.select('div.todo_subjt')

	num = []
	date = []
	
	for i in range(len(elements1)):
		title=elements1[i].text
		subjt=elements2[i].text
		date1=elements3[i].text.replace('/', '')
		date = date1[0:10]
		datetime = date1[10:]
		print("제목 :", title.strip())
		print("과목 :",subjt.strip())
		print("기한 :",date.strip(), datetime.strip())
		day = date.strip()
		print(day[:4])
		title1 = title.strip()
		if title1[:7]=='[온라인강의]':
			#if day[:5]=='D-Day':
				print(day[:5], "수강할 강의 +1")
				num1+=1
				num.append(i) #0부터 시작
			
	print("들을 강의 수는",num1)
	if(num1==0):
		print("수강할 강의가 없습니다, 프로그램을 종료합니다")
		data = {
		 "content" : "금일 수강할 강의가 없습니다",
		"username" : "온라인강의 수강 도우미"
		}
		result = requests.post(url, json = data)	
		result.raise_for_status()
		break

	time.sleep(1)
	driver.find_elements_by_class_name('todo_title')[num[0]].click() #강의실 들어가기

	# 페이지 소스 가져오기
	html = driver.page_source
	driver.get(driver.current_url)
	# soup에 넣어주기
	soup = BeautifulSoup(html, 'html.parser')
	time.sleep(1)

	lisnum = 0
	listime = -1
	lisname = ""
	perdiv = soup.select("div.lecture-box > div > ul > li:nth-child(1) > ol > li:nth-child(5) > div > div > div:nth-child(2) > div:nth-child(2)")
	timediv = soup.select("div.lecture-box > div > ul > li:nth-child(1) > ol > li:nth-child(5) > div > div > div:nth-child(2) > div:nth-child(3)")
	namediv = soup.select("div.lecture-box > div > ul > li:nth-child(1) > ol > li:nth-child(5) > div > div > div:nth-child(1) > div > span")

	for j in range(len(timediv)):
		time1=timediv[j].text
		perdiv1=perdiv[j].text
		name1=namediv[j].text
		#timef1 = time1.split(":")
		timef0 = time1.split('/')
		timef2 = timef0[0].split(":")
		timef3 = timef0[1].split(":")
		print("현재/목표시간", timef0[0].strip(), timef0[1].strip()) 
		if(perdiv1!='100%'):
			if((int(timef3[0].strip())-int(timef2[0].strip())>0) or int(timef3[0].strip())==0):
				lisnum = j
				listime = int(timef3[0].strip())-int(timef2[0].strip()) + 3
				lisname = name1
				print(lisname, "강의 접속")
				print(listime, "분을 수강할 예정")
				print("수강 필요 강의 중 ",j+1,"번 강의 접속")
				break



	driver.find_elements_by_class_name('site-mouseover-color')[lisnum].click() # 영상 실행 클릭
	#driver.switch_to.frame('contentViewer') #재생 안해도 실행됨
	#driver.find_element_by_xpath('//*[@id="front-screen"]/div/div[2]/div[1]/div').click() #재생버튼 클릭
	time.sleep(1)
	start = time.time()

	data = {
		"username" : "온라인강의 수강 도우미"
	}



	while True:
		if(int(((time.time()-start)/60)) == listime):
			driver.find_elements_by_class_name('contents-view-btn-title')[2].click() # 강의 종료 클릭
			print("강의 1개 수강 완료")
			print(((time.time()-start)/60), "분 지남")
			num1 =0
			data["embeds"] = [
				{
			"description" : lisname,
			"title" : "온라인강의 수강 완료 안내"
				}
			]
			result = requests.post(url, json = data)	
			result.raise_for_status()
			break


driver.quit()

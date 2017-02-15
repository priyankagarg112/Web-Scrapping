import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook


class FinalProject:
    def __init__(self,url= "https://www.class-central.com/subject/data-science"):
        self.url = url
        base_url = 'https://www.class-central.com'
        self.error_flag = False
        self.driver = webdriver.Chrome('/home/priyanka/Downloads/chromedriver')
        self.driver.get(self.url)
        self.count_course_and_scroll()
        self.list_courses()

    def count_course_and_scroll(self):
        self.total_courses = self.driver.find_element_by_xpath("//span[@id='number-of-courses']").text
        self.total_courses = int(self.total_courses)
        if self.total_courses > 50:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            sleep(1)
            load_more = self.driver.find_element_by_xpath('//div[@id="show-more-courses"]')
            load_more.click()
            no_of_scrolls = self.total_courses - 50
            no_of_scrolls = int(no_of_scrolls/50) + 2
            for value in range(no_of_scrolls):
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                sleep(4)

    def list_courses(self):
        page = self.driver.page_source
        base_url = 'https://www.class-central.com'
        soup = BeautifulSoup(page, 'lxml')
        course_table = soup.find('tbody', id='course-listing-tbody')
        rows = course_table.find_all('tr')
        courses = []
        for row in rows:
            course_name_column = row.find('td', class_='course-name-column')  
            if course_name_column is None:
            	continue
            if course_name_column.find('a', class_='course-name ad-name') is not None:
                continue
    	    course_url = course_name_column.find('a', class_='course-name').get('href')
    	    if course_url.startswith('/mooc') == False:
        	continue
    	    course_name = course_name_column.find('a', class_='course-name').get('title')
            course_url = base_url + course_url
            providers = ', '.join([p.a.text for p in course_name_column.find('ul', class_='table-uni-list').find_all('li')])
            platform = course_name_column.find('ul', class_='table-uni-list').find('a', recursive=False).text
            start_date = row.find('td', class_='start-date').text
            rating = row.find('td', class_='course-rating-column').get('data-timestamp')
            course = (course_name, providers, platform, start_date, rating, course_url)
            courses.append(course)
        
        print courses 
        
        workbook = Workbook('courses.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0,0,'course_name')
        worksheet.write(0,1,'providers')
        worksheet.write(0,2,'platform')
        worksheet.write(0,3,'start_date')
        worksheet.write(0,4,'course_name')
        worksheet.write(0,5,'rating')
        worksheet.write(0,6,'course_url')

        row = 1
        for course in courses:
            for i in range(len(course)):        
                worksheet.write(row,i,course[i])
            row += 1

        workbook.close()
        sleep(4)
        self.driver.close()



fp = FinalProject()



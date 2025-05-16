import pickle
import requests
from bs4 import BeautifulSoup
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Whale/4.31.304.16 Safari/537.36'
}

def get_course_info(course):
    # 이미 강의계획서 정보가 존재한다면 스킵
    if 'detailed_info' in course:
        return course

    year = course['year']
    term = course['term']
    grad_cd = course['courgrad_cd']
    col_cd = course['col_cd']
    dept_cd = course['dept_cd']
    cour_cd = course['cour_cd']
    cour_cls = course['cour_cls']
    url = f'https://infodepot.korea.ac.kr/lecture1/lecsubjectPlanViewNew.jsp?year={year}&term={term}&grad_cd={grad_cd}&col_cd={col_cd}&dept_cd={dept_cd}&cour_cd={cour_cd}&cour_cls={cour_cls}&cour_nm=&std_id=&device=WW'

    try:
        res = requests.get(url, headers=headers)

        # 서버에 부담이 가지 않도록 요청당 0.3초의 딜레이 추가
        time.sleep(0.3)

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')

            tmp = soup.find('th', string='수업유형').parent
            yeet = [item for item in tmp.find_all('td') if item.findChildren('input')[0].has_attr('checked')]
            수업유형 = None
            if len(yeet) > 0:
                수업유형 = yeet[0].text.strip()

            tmp = soup.find('th', string='특별유형').parent
            tmp2 = tmp.find_all('td')
            tmp = tmp.find_next('tr')
            tmp2.extend(tmp.find_all('td'))
            특별유형 = [item.text.strip() for item in tmp2 if item.findChildren('input')[0].has_attr('checked')]

            tmp = soup.find('th', string='수업구성요소').parent
            tmp2 = tmp.find_all('td')
            tmp = tmp.find_next('tr')
            tmp2.extend(tmp.find_all('td'))
            tmp = tmp.find_next('tr')
            tmp2.extend(tmp.find_all('td'))
            수업구성요소 = [item.text.strip() for item in tmp2 if item.findChildren('input')[0].has_attr('checked')]

            tmp = soup.find('th', string='성적평가').parent
            성적평가 = [item.text.strip() for item in tmp.find_all('td') if item.findChildren('input')[0].has_attr('checked')]

            tmp = soup.find('span', string='평가방법').find_next('table')
            평가방법 = {}
            tmps = tmp.find_all('th')
            for item in tmps:
                perc = item.find_next_sibling('td')
                if perc != None and '%' in perc.text:
                    평가방법[item.text.strip()] = perc.text.strip()
                    #print('평가방법', item.text.strip(), perc.text.strip())

            #if no == None:
            #    평가방법['출석'] = tmp.find('th', string=re.compile(r'.*출석.*')).find_next('td').text.strip()
            #    평가방법['과제'] = tmp.find('th', string=re.compile(r'.*과제.*')).find_next('td').text.strip()
            #    평가방법['중간고사'] = tmp.find('th', string=re.compile(r'.*중간고사.*')).find_next('td').text.strip()
            #    평가방법['기말고사'] = tmp.find('th', string=re.compile(r'.*기말고사.*')).find_next('td').text.strip()

            course['detailed_info'] = {
                '수업유형': 수업유형,
                '특별유형': 특별유형,
                '수업구성요소': 수업구성요소,
                '성적평가': 성적평가,
                '평가방법': 평가방법,
            }
    except:
        print('error occured', url)

    return course

filepath = 'courses_with_syllabus.pickle'

if not os.path.exists(filepath):
    filepath = 'courses.pickle'

with open(filepath, 'rb') as fr:
    courses = pickle.load(fr)

checkpoint = 0

# 백업이 있다면 불러옴
if os.path.exists('courses_backup.pickle'):
    with open('courses_backup.pickle', 'rb') as fr:
        backup = pickle.load(fr)
        print('backup', len(backup))
        checkpoint = len(backup)
        backup.extend(courses[len(backup):])
        courses = backup

new_courses = []
for i in courses:
    new_courses.append(get_course_info(i))

    # 시간이 오래 걸리기에 중간에 백업 생성
    # 만약 의도치 않게 종료되어도 백업 지점부터 작업 재개
    if len(new_courses) % 3000 == 0 and len(new_courses) > checkpoint:
        print('make backup')
        with open('courses_backup.pickle', 'wb') as fw:
            pickle.dump(new_courses, fw)

with open('courses_with_syllabus.pickle', 'wb') as fw:
    pickle.dump(new_courses, fw)
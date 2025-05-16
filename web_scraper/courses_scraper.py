import requests
import time
from urllib import parse
import pickle

nf_url = 'https://netfunnel.korea.ac.kr/ts.wseq?opcode=5101&nfid=0&prefix=NetFunnel.gRtype=5101;&sid=service_1&aid=sugang_search&js=yes&'
url = 'https://sugang.korea.ac.kr/view?attribute=lectHakbuData&fake='

def get_courses(year, term):
    formdata = {
        'pYear': year,
        'pTerm': term,
        'pCampus': '1',
        'pGradCd': '0136',
        'pCourDiv': '',
        'pCol': '',
        'pDept': '',
        'pCredit': '',
        'pDay': '',
        'pStartTime': '',
        'pEndTime': '',
        'pProf': '',
        'pCourCd': '',
        'pCourNm': '',
        'strYear': '2025',
        'strTerm': '1R',
        'strUserType': '......',
        'strChasu': '',
    }

    nf_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Whale/4.31.304.16 Safari/537.36'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Whale/4.31.304.16 Safari/537.36',
        'Referer': 'https://sugang.korea.ac.kr/core?attribute=coreMain&pWname=395ac829-d4ad-38b0-1c6f-3290f33e2de9&flagx=X&fake=1745034686383',
    }

    nf = requests.get(nf_url + str(int(time.time() * 1000)), headers=nf_headers)

    nf_key = parse.quote(str(nf.content).split("'")[1])

    headers['Cookie'] = f'my-application-browser-tab={{"guid":"395ac829-d4ad-38b0-1c6f-3290f33e2de9","timestamp": {int(time.time() * 1000)}}}; NetFunnel_ID={nf_key}'

    res = requests.post(url + str(int(time.time() * 1000)), data=formdata, headers=headers)

    return res.json()['data']


courses = []

# 2020년부터 2024년까지의 정규학기 강의만
l = [('2024', '1R'), ('2024', '2R'), ('2023', '1R'), ('2023', '2R'), ('2022', '1R'), ('2022', '2R'), ('2021', '1R'), ('2021', '2R'), ('2020', '1R'), ('2020', '2R')]

for y, t in l:
    c = get_courses(y, t)
    
    courses.extend(c)

print(len(courses))

with open('courses.pickle','wb') as fw:
    pickle.dump(courses, fw)
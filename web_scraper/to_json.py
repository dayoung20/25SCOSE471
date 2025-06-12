import pickle
import json

'''

pickle -> json
변환을 위한 임시 코드

'''
if __name__=="__main__":
    with open('courses_with_syllabus.pickle', 'rb') as fr:
        courses = pickle.load(fr)

    data = []

    for c in courses:
        if c['campus'] != '서울':
            continue
        item = {
            '년도': c['year'],
            '학기': c['term'],
            '학수번호': c['cour_cd'],
            '분반': c['cour_cls'],
            '이수구분': c['isu_nm'],
            '개설학과': c['department'],
            '교과목명': c['cour_nm'],
            '담당교수': c['prof_nm'],
            '학점': c['time'],
            '강의시간': c['time_room'],
            '학과제한': c['apply_dept'],
            '상대평가': c['absolute_yn'] == 'N',
            '인원제한': c['lmt_yn'] == 'Y',
            '교환학생': c['exch_cor_yn'] == 'N',
            '출석확인자율화': c['attend_free_yn'] == 'Y',
            '무감독시험': c['no_supervisor_yn'] == 'Y',
            '유연학기': c['flexible_term'] == 'Y',
            '수업유형': c['detailed_info']['수업유형'],
            '특별유형': c['detailed_info']['특별유형'],
            '성적평가': c['detailed_info']['성적평가'],
            '평가방법': c['detailed_info']['평가방법'],
            'MOOC': c['mooc_yn'] == 'Y',
            'Flipped': c['flipped_class_yn'] == 'Y',
            'Tutorial': c['tutorial_yn'] == 'Y',
            'NeMo': c['nemo_yn'] == 'Y',
            'SC': c['eng100'] == 'Y',
            '수강포기제한': c['drop_lmt_yn'] == 'Y',
        }
        data.append(item)

    print(len(data))

    with open('data.json', 'a+', encoding="UTF-8") as fp:
        json.dump(data, fp, ensure_ascii=False)
from datatype.feature import *

def get_features(filter=[], class_type=False, isu_type=False, class_component=False, grade_type=False):
    features = [
        Feature('Year', FeatureType.NOMINAL),
        Feature('인원제한', FeatureType.BOOLEAN),
        Feature('NeMo', FeatureType.BOOLEAN),
        Feature('영강', FeatureType.BOOLEAN),
        Feature('튜토리얼', FeatureType.BOOLEAN),
        Feature('MOOC', FeatureType.BOOLEAN),
        Feature('학점', FeatureType.NUMERICAL),
        Feature('강의시간', FeatureType.NUMERICAL),
        Feature('개설학과', FeatureType.NOMINAL),
        Feature('담당교수', FeatureType.NOMINAL),
        Feature('출석확인자율화', FeatureType.BOOLEAN),
        Feature('Flipped', FeatureType.BOOLEAN),
        Feature('상대평가', FeatureType.BOOLEAN),
        Feature('수강포기제한', FeatureType.BOOLEAN),
        Feature('교환학생', FeatureType.BOOLEAN),
        Feature('무감독시험', FeatureType.BOOLEAN),
        Feature('수업유형', FeatureType.NOMINAL),
    ]

    if filter and len(filter) > 0:
        features = [x for x in features if x.name in filter]

    if class_type:
        ct = ['대면','병행', '원격', '원격(녹화)', '원격(실시간)', '혼합']
        for x in ct:
            features.append(Feature('수업유형_' + x, FeatureType.BOOLEAN))

    if isu_type:
        isu = ['교직', '교직(비사대)', '군사학', '전공선택', '전공필수', '평생교육사',
                    '학문의기초', '학부공통']
        for t in isu:
            features.append(Feature('이수구분.' + t, FeatureType.BOOLEAN))

    if class_component:
        cc = ['Q&A', '개별지도', '발표', '상시상담', '실습', '실험',
                            '이론강의', '집단지도', '체험', '퀴즈', '토론', '특강',
                            '포럼', '프로젝트', '협동학습']
        for c in cc:
            features.append(Feature('수업구성요소_' + c, FeatureType.BOOLEAN))

    if grade_type:
        _grade_type = ['P/F', '상대평가', '절대평가']
        for g in _grade_type:
            features.append(Feature('성적평가_' + g, FeatureType.BOOLEAN))

    #criteria = ['시험', '출석', '과제', '참여도', '발표', '프로젝트', '협동', '보고서', '실험', '태도', '기타']
    #for c in criteria:
    #    features.append(Feature(c, FeatureType.NUMERICAL))

    return features
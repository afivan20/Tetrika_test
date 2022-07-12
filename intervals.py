

def appearance(intervals: dict) -> int:
    lesson = intervals['lesson']
    tutor = intervals['tutor']
    pupil = intervals['pupil']

    INTERVAL = [] # пересечение отрезков урока и ученика
    for indx in range(0, len(tutor)-1, 2):
        start = tutor[indx]
        end = tutor[indx+1]
        if end < lesson[0] or start > lesson[1]: # не пересекаются
            continue
        if (start < lesson[0]) and (lesson[0] < end<=lesson[1]):  # начало отрезк за пределами урока, конец в переделах урока
            INTERVAL.append(lesson[0])
            INTERVAL.append(end)
            continue
        if (lesson[0] <= start <= lesson[1]) and (lesson[0] <= end<= lesson[1]): # отрезок в пределах урока
            INTERVAL.append(start)
            INTERVAL.append(end)
            continue
        if (lesson[0] <= start <= lesson[1]) and (end> lesson[1]): # начала отрезка в пределах урока, конец за пределами
            INTERVAL.append(start)
            INTERVAL.append(lesson[1])
            continue
        if (start < lesson[0]) and (end > lesson[1]):
            INTERVAL.append(lesson[0])
            INTERVAL.append(lesson[1])

    pupil = intersections(pupil)
    # пересечние отрезков ученика и учителя
    COMMON_INTERVALS = 0
    for i in range(0, len(INTERVAL)-1, 2):
        intersection = [-2,-1]
        START = INTERVAL[i]
        END = INTERVAL[i+1]
        for k in range(0, len(pupil)-1, 2):
            start = pupil[k]
            end = pupil[k+1]
            # if is_intersection(start, intersection):
            #     start = intersection[1]
            intersection = [start, end]
            if end < START or start > END: # отрезок до начала пересечений
                continue
            if (start< START) and (START<end<= END):
                COMMON_INTERVALS += end - START # начало отрезк за пределами , конец в пределах
                continue
            if (START <= start <= END) and (START<=end<= END): # отрезок в пределах пересечения
                COMMON_INTERVALS += end - start
                continue
            if (START <= start <= END) and (end> END): # начала отрезка в пределах пересечения, конец за пределами
                COMMON_INTERVALS += END - start
                continue
            if (start < START) and (end > END):
                COMMON_INTERVALS += END - START
                continue
    return COMMON_INTERVALS

def flowerbed(sections, n):
    result=[]
    j=0
    if n != 1:
        for i in range(n-1):
            i+=j
            if i == 0:
                if sections[i][1] > sections[i+1][0] and sections[i][1] >= sections[i+1][1]: # 1ый отрезок полность поглощает (2 4)(3 4)
                    result.append(sections[i])
                    j+=1
                if sections[i][1] >= sections[i+1][0] and sections[i][1] < sections[i+1][1]: # отрезки пересекаются, происходит слияние
                    result.append((sections[i][0],sections[i+1][1]))
                    j+=1
                if sections[i][1] < sections[i+1][0]: # не пересeкаются
                    result.append(sections[i])
                    result.append(sections[i+1])
                    j+=1
            if i != 0:
                if sections[i][0] < result[-1][1] and sections[i][1] < result[-1][1]: # 1ый отрезок полность поглощает (2 4)(3 4)
                    pass
                if sections[i][0] <= result[-1][1] and sections[i][1] > result[-1][1]:
                        ### нужно будет изменить предыдуший result[-1]
                    a= result[-1][0]
                    z= sections[i][1]
                    result[-1]=tuple((a,z))
                if sections[i][0] > result[-1][1]:
                    result.append(sections[i])
        return result
    else:
        return sections

def intersections(pupils):
    extract = []
    for k in range(0, len(pupils)-1, 2):
        extract.append((pupils[k], pupils[k+1]))
    done = flowerbed(extract, len(extract))
    res = []
    for tuple in done:
        res.append(tuple[0])
        res.append(tuple[1])

    return res







tests = [
    {'data': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'data': {'lesson': [1594702800, 1594706400],                                              #                    #  #                    #  #                    #  #                    #  #                    #  #                    #  #                    #  #                    #  #                    #  #                    #  #                    #       
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['data'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

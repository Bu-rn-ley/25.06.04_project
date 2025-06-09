import unicodedata

WEEKDAYS = ['월', '화', '수', '목', '금']

def disp_width(text):
    """영어일때와 한국어일때의 너비가 달라 표에 간격이 안맞게 됨. 그걸 해결하기 위한 함수"""
    return sum(2 if unicodedata.east_asian_width(ch) in 'WF' else 1 for ch in text)

def center(text, width):
    """과목명 가운데 정렬"""
    pad = width - disp_width(text)
    left = pad // 2         #빈칸은 소수개일 수 없으므로 내림 연산자 사용
    right = pad - left      #right = left 라고 했더니 pad 가 홀수일때 오류 발생
    return ' ' * left + text + ' ' * right


class Course:
    def __init__(self, name, day, start_time, end_time):
        self.name = name
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    def overlaps(self, other):
        # 끝나는 시간은 시간표에 표시 X 시작시간이 13시고 끝나는 시간이 15시라면 13시와 14시에만 표시
        return self.day == other.day and not (
            self.end_time <= other.start_time or self.start_time >= other.end_time
        )

    def to_dict(self):
        return {
            'name': self.name,
            'day': self.day,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

    def __str__(self):
        return f"{self.day}요일 {self.start_time}시~{self.end_time}시: {self.name}"
    
def course_from_dict(data):
    return Course(
        data['name'],
        data['day'],
        data['start_time'],
        data['end_time']
    )
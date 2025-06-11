import unicodedata
import json

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

    #--------------------------------여기부터----------------------------



class Schedule:
    def __init__(self):
        self.courses = []
        # 수업 목록 여기있음 <-------------------

    def add_course(self, course):
        for i in self.courses:
            if i.name == course.name:
                print("해당 수업이 이미 추가되었습니다.")
                return False
                # 이미 추가된 수업 다시 추가 방지하는 함수

        for i in self.courses:
            if i.overlaps(course):
                print(f"{i} 와 중복됩니다.")
                return False
        self.courses.append(course)
        # 그 시간에 이미 수업이 있으면 겹쳐지는 문제 방지

        print(f"{course.name} 수업이 추가되었습니다.")
        self.display()
        return True
        # 정상적으로 수업 추가

    def delete_course(self, name):
        for i in self.courses:
            if i.name == name:
                self.courses.remove(i)
                print(f"{name} 수업이 삭제되었습니다.")
                return True
                # 성공적으로 수업 삭제
            
        print("해당 수업을 찾을 수 없습니다.")
        # 삭제하려는 수업 없을때
        return False



    def edit_course(self, name):
        for i in self.courses:
            if i.name == name:
                print(f"{i} 수업을 수정합니다.")
                # 이미 있는 수업 수정
                day = get_valid_day()
                start = get_valid_time("시작 시간")
                end = get_valid_time("끝나는 시간")
                # 날짜, 시간 범위 다시 받기
                self.delete_course(name)
                # 이름도 수정할 시 사용
                return self.add_course(Course(name, day, start, end))
            
        print("해당하는 수업이 없습니다.")
        return False

    def display(self):
        if not self.courses:
            print("등록된 수업이 없습니다.")
            return
            # 등록된 수업 없는데 수업을 불러오려 할때
        longest = max([disp_width(i.name) for i in self.courses] + [6])
        sero_width = longest + 4
        sero_width = longest + 4  
        #크기 키우기
        print("\n전체 시간표:")
        header = f"{'시간':<6}" + "|".join(center(day, sero_width) for day in WEEKDAYS) + "|"
        print(header)
        print("-" * len(header))
        #출력
        
        timetable = {day: [''] * 24 for day in WEEKDAYS}
        #틀에 맞게 수정해 출력

        for course in self.courses:
            for hour in range(course.start_time, course.end_time):
                timetable[course.day][hour] = course.name
            #틀에 맞게 수정해 출력
        for hour in range(24):
            row = f"{hour:02d}시  "
            for day in WEEKDAYS:
                row += "|" + center(timetable[day][hour], sero_width)
            row += "|"
            print(row)
            #설정된 틀 변경
    def display_day(self, day):
        same_day = [i for i in self.courses if i.day == day]

        if not same_day:
            print(f"{day}요일은 수업이 없습니다.")
            return
        # 요일에 해당하는 수업을 찾는데 없을때

        print(f"\n {day}요일 시간표:")
        for j in sorted(same_day, key=lambda k: k.start_time):
            print("  ", j)
            # lambda => key로 함수를 설정할때 직관적으로 정렬 기준 지정

    def search(self, keyword):
        results = [l for l in self.courses if keyword.lower() in l.name.lower()]
        if not results:
            print("검색 결과가 없습니다.")
            return
        # 검색한 수업을 찾을 수 없을때

        print("검색 결과:")
        for m in results:
            print("  ", m)
        # 검색 결과 불러오기

    def save_to_file(self, filename):

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([i.to_dict() for i in self.courses], f, ensure_ascii=False, indent=2)
        print(f"{filename}에 저장되었습니다.")
    #    파일에 저장


    def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.courses = [Course.from_dict(d) for d in json.load(f)]
            print(f"{filename}에서 시간표를 불러왔습니다.")
        # 파일에서 불러오기
        except FileNotFoundError:
            print("파일이 존재하지 않습니다.")
    #  불러오려는데 불러올 파일이 없을때  


def get_valid_day():
    #요일 선택
    while True:
        day = input("요일 (월~금): ").strip()
        if day in WEEKDAYS:
            return day
        print("올바른 요일을 입력해주세요.")


def get_valid_time(label):
    #시간 입력
    while True:
        try:
            time = int(input(f"{label} (0~23): "))
            if 0 <= time <= 23:
                return time
        except ValueError:
            pass
        print("올바른 시간을 입력해주세요.")


def menu():
    print("""
시간표 짜기 명령어 도움말
1. 수업 추가  2. 수업 삭제  3. 수업 수정  4. 전체 출력
5. 요일별 보기  6. 검색  7. 저장  8. 불러오기  9. 종료
""")


def main():
    schedule = Schedule()
    menu()

    while True:
        print("\n[메뉴] 1.추가 2.삭제 3.수정 4.전체출력 5.요일별보기 6.검색 7.저장 8.불러오기 9.종료")
        input_text = input("선택: ").strip()

        if input_text == '1':
            name = input("수업 이름: ")
            day = get_valid_day()
            start = get_valid_time("시작하는 시간")
            end = get_valid_time("끝나는 시간")
            schedule.add_course(Course(name, day, start, end))
        elif input_text == '2':
            schedule.delete_course(input("삭제할 수업 이름: "))
        elif input_text == '3':
            schedule.edit_course(input("수정할 수업 이름: "))
        elif input_text == '4':
            schedule.display()
        elif input_text == '5':
            schedule.display_day(get_valid_day())
        elif input_text == '6':
            schedule.search(input("검색할 수업 키워드: "))
        elif input_text == '7':
            schedule.save_to_file(input("저장할 파일 이름(.json 포함): ").strip())
        elif input_text == '8':
            schedule.load_from_file(input("불러올 파일 이름(.json 포함): ").strip())
        elif input_text == '9':
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 번호를 입력해주세요.")


if __name__ == "__main__":
    main()


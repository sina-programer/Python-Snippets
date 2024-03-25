def type_converter(*p_filters, **k_filters):
    """
    A decorator function for converting argument's types
    The input must be a function to be applied on argument
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            args = list(args)
            for idx, (converter, value) in enumerate(zip(p_filters, args)):  # using zip() to avoid extra values
                if converter is not None:
                    args[idx] = converter(value)
            for arg, converter in k_filters.items():
                if arg in kwargs and converter is not None:
                    kwargs[arg] = converter(kwargs[arg])
            return func(*args, **kwargs)

        return wrapper

    return decorator


class BaseItem:
    _extra_attrs = {}  # these extra attributes will be shown in __repr__

    @property
    def attrs(self):
        return list(filter(lambda attr: '_' not in attr , self.__dict__.keys()))

    @staticmethod
    def _represent_value(x):
        for dtype in [list, tuple, set, dict, frozenset]:
            if type(x) == type(dtype()):
                return f"{dtype.__name__}({len(x)})"
        return str(x)

    def _represent_attributes(self):
        origin_attrs = [f'{attr}={self._represent_value(getattr(self, attr))}' for attr in self.attrs]
        extra_attrs = [f'{key}={self._represent_value(value)}' for key, value in self._extra_attrs.items()]
        return ', '.join(origin_attrs + extra_attrs)

    def __repr__(self):
        return f"{type(self).__name__}({self._represent_attributes()})"


class Student(BaseItem):
    def __init__(self, code, faculty):
        self.code = code
        self.faculty = faculty
        self.course_score = {}  # course-name: score
        self.dropped = False

    @property
    def courses(self): return list(self.course_score.keys())

    @property
    def scores(self): return list(self.course_score.values())

    @property
    def _extra_attrs(self):
        return {
            'courses': self.courses
        }

    def has_score(self):
        # return bool(len(list(filter(lambda x: x is not None, self.scores))))
        for score in self.scores:
            if score is not None:
                return True
        return False

    def has_course(self, course_name):
        return course_name in self.courses

    def take_course(self, course_name):
        self.course_score[course_name] = None

    def drop_course(self, course_name):
        self.course_score.pop(course_name)
        self.dropped = True

    def get_course_score(self, course_name):
        return self.course_score.get(course_name, None)

    def set_course_score(self, course_name, score):
        self.course_score[course_name] = min(score, 20)

    def average(self):
        if not self.has_score():
            return -1

        total_score = 0
        total_units = 0
        for course_name, score in self.course_score.items():
            if score is not None:
                course = Courses.get_by_name(course_name)
                total_score += score * course.units
                total_units += course.units
        return total_score / total_units

    def show_report(self):
        print('student number:', self.code)
        print('department:', self.faculty)
        for course_name in sorted(self.courses):
            course = Courses.get_by_name(course_name)
            student_score = self.get_course_score(course.name)
            print(
                course.name,
                course.units,
                format(student_score, '.2f') if student_score is not None else 'None',
                format(course.average(), '.2f') if student_score is not None else 'None'
            )

    @staticmethod
    def _get_rank(scores, x):
        lv = None
        lr = 0
        for idx, n in enumerate(sorted(scores, reverse=True)):
            if n != lv:
                lv = n
                lr = idx
            if n == x:
                return lr + 1

    def get_faculty_rank(self):
        averages = list(map(lambda st: st.average(), self.fetch_faculty_students()))
        average = self.average()
        # return self._get_rank(averages, average)
        return averages.index(average) + 1

    def fetch_faculty_students(self):
        fstudents = Students.get_by_faculty(self.faculty)
        if fstudents:
            return fstudents
        return []

    def fetch_courses(self):
        for course_name in self.courses:
            if (course := Courses.get_by_name(course_name)) is not None:
                yield course


class Professor(BaseItem):                  
    def __init__(self, code, name, age, faculty, available_courses):
        self.code = code
        self.name = name
        self.age = age
        self.faculty = faculty
        self.available_courses = available_courses
        self.courses = []

    def is_able_course(self, course_name):
        return course_name in self.available_courses

    def has_course(self, course_name):
        return course_name in self.courses

    def take_course(self, course_name):
        self.courses.append(course_name)

    def check_time(self, day, start, end):
        for course_name in self.courses:
            course = Courses.get_by_name(course_name)
            if course and course.day==day and (course.start <= start <= course.end or course.start <= end <= course.end):
                return False
        return True

    def fetch_courses(self):
        for course_name in self.courses:
            if (course := Courses.get_by_name(course_name)) is not None:
                yield course


class Course(BaseItem):
    def __init__(self, name, units, day, start, end, faculty, professor_code):
        self.name = name
        self.units = units
        self.day = day
        self.start = start
        self.end = end
        self.faculty = faculty
        self.professor_code = professor_code

    def average(self):
        scores = []
        for student in self.fetch_students():
            if (score := student.get_course_score(self.name)) is not None:
                scores.append(score)
        return sum(scores) / len(scores)

    def add_scores(self, scores):
        students = list(self.fetch_students())
        for student, score in zip(sorted(students, key=lambda student: student.code), scores):
            student.set_course_score(self.name, score)

    def have_mercy(self, avg):
        diff = avg - self.average()
        for student in self.fetch_students():
            student.set_course_score(self.name, student.get_course_score(self.name) + diff)

    def are_scores_set(self):
        for student in self.fetch_students():
            if student.get_course_score(self.name) is not None:
                return True
        return False

    def fetch_students(self):
        students = Students.get_by_course(self.name)
        if students:
            for student in students:
                yield student
        return []

    def fetch_professor(self):
        return Professors.get_by_code(self.professor_code)



class BaseGroup:
    dtype = None
    members = list()

    def __contains__(self, x):
        return x in self.members

    def __iter__(self):
        return iter(self.members)

    @classmethod
    def add(cls, *args, **kwargs):
        new_member = cls.dtype(*args, **kwargs)
        cls.members.append(new_member)
        return new_member

    @classmethod
    def get(cls, function=None, unary=True, **filters):
        objects = cls.members.copy()
        if function is not None:
            objects = list(filter(function, objects))
        for key, value in filters.items():
            objects = list(filter(lambda x: getattr(x, key) == value, objects))
        if len(objects) == 0:
            return None
        elif unary:
            return objects[0]
        return objects


class Students(BaseGroup):
    dtype = Student
    members = []

    @classmethod
    @type_converter(None, str, int)
    def add(cls, faculty, code):
        if cls.get_by_code(code):
            print('student with this student number already exists')
            return

        return super().add(code, faculty)

    @classmethod
    @type_converter(None, int)
    def find_gpa(cls, student_id):
        student = cls.get_by_code(student_id)

        if student is None:
            print('there is no student with this number')
            return

        if not student.has_score():
            print('no grades have been recorded for this student')
            return

        print(format(student.average(), '.2f'))

    @classmethod
    @type_converter(None, int)
    def find_rank(cls, student_id):
        student = cls.get_by_code(student_id)
        if student is None:
            print('there is no student with this number')
            return

        print(student.get_faculty_rank())

    @classmethod
    @type_converter(None, int)
    def show_report(cls, student_id):
        student = cls.get_by_code(student_id)
        if student is None:
            print('there is no student with this number')
            return
        student.show_report()

    @classmethod
    def faculty_average(cls, faculty):
        averages = list(map(lambda student: student.average(), cls.get_by_faculty(faculty)))
        return sum(averages) / len(averages)

    @classmethod
    @type_converter(None, str, int)
    def take_course(cls, course_name, student_id):
        student = Students.get_by_code(student_id)
        course = Courses.get_by_name(course_name)
        if course is None or student is None or student.has_course(course.name):
            print('invalid command')
            return

        if course.are_scores_set():
            print('it is too late to take this course')

        student.take_course(course.name)

    @classmethod
    @type_converter(None, str, int)
    def find_grade(cls, course_name, student_id):
        course = Courses.get_by_name(course_name)
        student = Students.get_by_code(student_id)

        if course is None or student is None:
            print('invalid course name or student number')
            return

        if not student.has_course(course.name):
            print('the student has not taken this course')
            return

        if not course.are_scores_set():
            print('course grades are not recorded')
            return

        print(format(student.get_course_score(course.name), '.2f'))

    @classmethod
    @type_converter(None, str, int)
    def drop_course(cls, course_name, student_id):
        course = Courses.get_by_name(course_name)
        student = Students.get_by_code(student_id)
        if student is None or course is None or not student.has_course(course_name):
            print('invalid command')
            return

        if student.get_course_score(course.name) is not None:
            print('it is too late to drop this course')
            return

        if student.dropped:
            print('the student has already dropped another course')
            return

        student.drop_course(course_name)

    @classmethod
    def get_by_course(cls, course_name, unary=False):
        return cls.get(function=lambda student: course_name in student.courses, unary=unary)

    @classmethod
    def get_by_faculty(cls, faculty, unary=False):
        return cls.get(faculty=faculty, unary=unary)

    @classmethod
    def get_by_code(cls, code):
        return cls.get(code=code)


class Professors(BaseGroup):
    dtype = Professor
    members = []

    @classmethod
    @type_converter(None, str, int, str, int)
    def add(cls, faculty, code, name, age):
        if cls.get_by_code(code):
            print('professor with this id already exists')
            return

        return super().add(code, name, age, faculty, available_courses=input().split())

    @classmethod
    def filter_professors(cls, course_name, day, start, end):
        for professor in cls.members:
            if not professor.is_able_course(course_name):
                continue
            if not professor.check_time(day, start, end):
                continue
            yield professor
 
    @classmethod
    def get_by_faculty(cls, faculty, unary=False):
        return cls.get(faculty=faculty, unary=unary)

    @classmethod
    def get_by_name(cls, name):
        return cls.get(name=name)

    @classmethod
    def get_by_code(cls, code):
        return cls.get(code=code)


class Courses(BaseGroup):
    dtype = Course
    members = []

    @classmethod
    @type_converter(None, str, str, int, str, int, int)
    def add(cls, faculty, name, units, day, start, end):
        if cls.get_by_name(name) is not None:
            print('course with this name already exists')
            return

        professors = list(Professors.filter_professors(name, day, start, end))
        if not professors:
            print('there is no professor for this course')
            return

        professor = min(professors, key=lambda professor: professor.code)
        course = super().add(name, units, day, start, end, faculty, professor.code)
        professor.take_course(course.name)
        print(professor.code)
        return course

    @classmethod
    def add_grades(cls, course_name):
        course = cls.get_by_name(course_name)
        if course is None:
            print('there is no course with this name')
            return

        if len(students := list(course.fetch_students())) == 0:
            print('no student has taken this course')
            return

        if course.are_scores_set():
            print('grades have already been recorded')
            return

        scores = list(map(float, input().split()))
        if len(scores) != len(students):
            print("the number of grades and students are not equal")
            return

        course.add_scores(scores)

    @classmethod
    @type_converter(None, str, float)
    def have_mercy(cls, course_name, desired_avg):
        course = Courses.get_by_name(course_name)
        if course is None or not len(list(course.fetch_students())) or not course.are_scores_set():
            print('invalid command')
            return

        current_avg = course.average()
        if current_avg >= desired_avg:
            print('sorry, that is not fair')
            return

        course.have_mercy(desired_avg)

    @classmethod
    def get_by_faculty(cls, faculty, unary=False):
        return cls.get(faculty=faculty, unary=unary)

    @classmethod
    def get_by_name(cls, name):
        return cls.get(name=name)



if __name__ == '__main__':
    while True:
        prompt = input().strip()
        args = prompt.split()

        if prompt.startswith('add student '):
            Students.add(*args[2:])
        elif prompt.startswith('add professor '):
            Professors.add(*args[2:])
        elif prompt.startswith('add course '):
            Courses.add(*args[2:])
        elif prompt.startswith('take course '):
            Students.take_course(args[2], args[5])
        elif prompt.startswith('add grades '):
            Courses.add_grades(args[3])
        elif prompt.startswith('find grade '):
            Students.find_grade(args[3], args[-1])
        elif prompt.startswith('find GPA '):
            Students.find_gpa(args[-1])
        elif prompt.startswith('find rank '):
            Students.find_rank(args[-1])
        elif prompt.startswith('drop course '):
            Students.drop_course(args[2], args[-1])
        elif prompt.startswith('show the report '):
            Students.show_report(args[-1])
        elif prompt.startswith('have mercy '):
            Courses.have_mercy(args[6], args[-1])
        elif prompt == 'exit':
            exit()

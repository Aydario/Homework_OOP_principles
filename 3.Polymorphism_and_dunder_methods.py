class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {self.get_average_grade():.2f}\n'
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
            f'Завершенные курсы: {", ".join(self.finished_courses) if self.finished_courses else "отсутствуют"}'
        )

    def __lt__(self, other):
        return self.get_average_grade() < other.get_average_grade()

    def __eq__(self, other):
        return self.get_average_grade() == other.get_average_grade()

    def __gt__(self, other):
        return self.get_average_grade() > other.get_average_grade()

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and
                course in lecturer.courses_attached and
                course in self.courses_in_progress):
            lecturer.received_grades[course] = lecturer.received_grades.get(course, [
            ])
            lecturer.received_grades[course] += [grade]
        else:
            return 'Ошибка'

    def get_average_grade(self):
        self.list_grades = []
        for grades in self.grades.values():
            self.list_grades += grades
        return sum(self.list_grades) / len(self.list_grades)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.received_grades = {}

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {self.get_average_grade_lectures():.2f}'
        )

    def __lt__(self, other):
        return self.get_average_grade_lectures() < other.get_average_grade_lectures()

    def __eq__(self, other):
        return self.get_average_grade_lectures() == other.get_average_grade_lectures()

    def __gt__(self, other):
        return self.get_average_grade_lectures() > other.get_average_grade_lectures()

    def get_average_grade_lectures(self):
        self.list_grades = []
        for grades in self.received_grades.values():
            self.list_grades += grades
        return sum(self.list_grades) / len(self.list_grades)


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress):
            student.grades[course] = student.grades.get(course, [])
            student.grades[course] += [grade]
        else:
            return 'Ошибка'

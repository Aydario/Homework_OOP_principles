from itertools import chain

class Student:
    """
    Represents a student with attributes such as name, surname, gender, finished courses,
    courses in progress, and grades.
    """
    def __init__(self, name, surname, gender):
        """
        Initializes a Student instance.

        :param name: The first name of the student.
        :param surname: The last name of the student.
        :param gender: The gender of the student.
        """
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        """
        Returns a string representation of the student.

        :return: A formatted string with student details.
        """
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {self.get_average_grade():.2f}\n'
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
            f'Завершенные курсы: {", ".join(self.finished_courses) if self.finished_courses else "отсутствуют"}'
        )

    def __lt__(self, other):
        """
        Compares the average grade of this student with another student.

        :param other: Another Student instance.
        :return: True if this student's average grade is less than the other's, False otherwise.
        """
        return self.get_average_grade() < other.get_average_grade()

    def __eq__(self, other):
        """
        Compares the average grade of this student with another student.

        :param other: Another Student instance.
        :return: True if this student's average grade is equal to the other's, False otherwise.
        """
        return self.get_average_grade() == other.get_average_grade()

    def __gt__(self, other):
        """
        Compares the average grade of this student with another student.

        :param other: Another Student instance.
        :return: True if this student's average grade is greater than the other's, False otherwise.
        """
        return self.get_average_grade() > other.get_average_grade()

    def rate_lecture(self, lecturer, course, grade):
        """
        Rates a lecture given by a lecturer.

        :param lecturer: A Lecturer instance.
        :param course: The course name.
        :param grade: The grade given to the lecture.
        :return: 'Ошибка' if the rating is not possible, None otherwise.
        """
        if (isinstance(lecturer, Lecturer) and
                course in lecturer.courses_attached and
                course in self.courses_in_progress):
            lecturer.received_grades[course] = lecturer.received_grades.get(course, [])
            lecturer.received_grades[course] += [grade]
        else:
            return 'Ошибка'

    def get_average_grade(self):
        """
        Calculates the average grade of the student across all courses.

        :return: The average grade.
        """
        self.list_grades = list(chain(*self.grades.values()))
        if not self.list_grades:
            return 0
        return sum(self.list_grades) / len(self.list_grades)


class Mentor:
    """
    Represents a mentor with attributes such as name, surname, and attached courses.
    """
    def __init__(self, name, surname):
        """
        Initializes a Mentor instance.

        :param name: The first name of the mentor.
        :param surname: The last name of the mentor.
        """
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    """
    Represents a lecturer who is a type of mentor with additional attributes for received grades.
    """
    def __init__(self, name, surname):
        """
        Initializes a Lecturer instance.

        :param name: The first name of the lecturer.
        :param surname: The last name of the lecturer.
        """
        super().__init__(name, surname)
        self.received_grades = {}

    def __str__(self):
        """
        Returns a string representation of the lecturer.

        :return: A formatted string with lecturer details.
        """
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {self.get_average_grade_lectures():.2f}'
        )

    def __lt__(self, other):
        """
        Compares the average lecture grade of this lecturer with another lecturer.

        :param other: Another Lecturer instance.
        :return: True if this lecturer's average grade is less than the other's, False otherwise.
        """
        return self.get_average_grade_lectures() < other.get_average_grade_lectures()

    def __eq__(self, other):
        """
        Compares the average lecture grade of this lecturer with another lecturer.

        :param other: Another Lecturer instance.
        :return: True if this lecturer's average grade is equal to the other's, False otherwise.
        """
        return self.get_average_grade_lectures() == other.get_average_grade_lectures()

    def __gt__(self, other):
        """
        Compares the average lecture grade of this lecturer with another lecturer.

        :param other: Another Lecturer instance.
        :return: True if this lecturer's average grade is greater than the other's, False otherwise.
        """
        return self.get_average_grade_lectures() > other.get_average_grade_lectures()

    def get_average_grade_lectures(self):
        """
        Calculates the average grade received by the lecturer across all courses.

        :return: The average grade.
        """
        self.list_grades = list(chain(*self.received_grades.values()))
        if not self.list_grades:
            return 0
        return sum(self.list_grades) / len(self.list_grades)


class Reviewer(Mentor):
    """
    Represents a reviewer who is a type of mentor with the ability to rate students' homework.
    """
    def __init__(self, name, surname):
        """
        Initializes a Reviewer instance.

        :param name: The first name of the reviewer.
        :param surname: The last name of the reviewer.
        """
        super().__init__(name, surname)

    def __str__(self):
        """
        Returns a string representation of the reviewer.

        :return: A formatted string with reviewer details.
        """
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def rate_hw(self, student, course, grade):
        """
        Rates a student's homework for a given course.

        :param student: A Student instance.
        :param course: The course name.
        :param grade: The grade given to the homework.
        :return: 'Ошибка' if the rating is not possible, None otherwise.
        """
        if (isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress):
            student.grades[course] = student.grades.get(course, [])
            student.grades[course] += [grade]
        else:
            return 'Ошибка'


def get_average_grade_students(list_students, course):
    """
    Calculates the average grade of all students for a given course.

    :param list_students: A list of Student instances.
    :param course: The course name.
    :return: A formatted string with the average grade or a message if no grades are available.
    """
    list_grades = list(chain(*(student.grades.get(course, []) for student in list_students)))
    if not list_grades:
        return f'Оценки за курс {course} отсутствуют'
    return f'Средняя оценка всех студентов за курс {course} равна {sum(list_grades) / len(list_grades):.2f}'


def get_average_grade_lecturers(list_lecturers, course):
    """
    Calculates the average grade of all lecturers for a given course.

    :param list_lecturers: A list of Lecturer instances.
    :param course: The course name.
    :return: A formatted string with the average grade or a message if no grades are available.
    """
    list_grades = list(chain(*(lecturer.received_grades.get(course, []) for lecturer in list_lecturers)))
    if not list_grades:
        return f'Оценки за курс {course} отсутствуют' 
    return f'Средняя оценка всех лекторов за курс {course} равна {sum(list_grades) / len(list_grades):.2f}'


best_student = Student('Ruoy', 'Eman', 'male')
best_student.courses_in_progress += ['Python', 'Ruby']
best_student.finished_courses += ['Java', 'Go']

worst_student = Student('Rayan', 'Gosling', 'male')
worst_student.courses_in_progress += ['Python', 'Ruby']

first_lecturer = Lecturer('Some', 'Buddy')
first_lecturer.courses_attached += ['Python', 'Ruby']

second_lecturer = Lecturer('Phill', 'Jones')
second_lecturer.courses_attached += ['Python', 'Ruby']

ruby_reviewer = Reviewer('Nick', 'Jonson')
ruby_reviewer.courses_attached += ['Ruby']

python_reviewer = Reviewer('Paul', 'Lemann')
python_reviewer.courses_attached += ['Python']

students = [best_student, worst_student]
lecturers = [first_lecturer, second_lecturer]
reviewers = [ruby_reviewer, python_reviewer]

best_student.rate_lecture(first_lecturer, 'Python', 10)
best_student.rate_lecture(first_lecturer, 'Python', 10)
best_student.rate_lecture(first_lecturer, 'Ruby', 9)
best_student.rate_lecture(first_lecturer, 'Ruby', 9)

worst_student.rate_lecture(second_lecturer, 'Python', 7)
worst_student.rate_lecture(second_lecturer, 'Python', 7)
worst_student.rate_lecture(second_lecturer, 'Ruby', 8)
worst_student.rate_lecture(second_lecturer, 'Ruby', 9)

ruby_reviewer.rate_hw(best_student, 'Ruby', 9)
ruby_reviewer.rate_hw(best_student, 'Ruby', 7)
python_reviewer.rate_hw(best_student, 'Python', 9)
python_reviewer.rate_hw(best_student, 'Python', 10)

ruby_reviewer.rate_hw(worst_student, 'Ruby', 6)
ruby_reviewer.rate_hw(worst_student, 'Ruby', 5)
python_reviewer.rate_hw(worst_student, 'Python', 6)
python_reviewer.rate_hw(worst_student, 'Python', 5)

for student in students:
    print(student)

for lecturer in lecturers:
    print(lecturer)

for reviewer in reviewers:
    print(reviewer)


def get_average_grade_students(list_students, course):
    list_grades = list(chain(*(student.grades.get(course, []) for student in list_students)))
    if not list_grades:
        return f'Оценки за курс {course} отсутствуют'
    return f'Средняя оценка всех студентов за курс {course} равна {sum(list_grades) / len(list_grades):.2f}'
    

def get_average_grade_lecturers(list_lecturers, course):
    list_grades = list(chain(*(lecturer.received_grades.get(course, []) for lecturer in list_lecturers)))
    if not list_grades:
        return f'Оценки за курс {course} отсутствуют'
    return f'Средняя оценка всех лекторов за курс {course} равна {sum(list_grades) / len(list_grades):.2f}'


print(get_average_grade_students(students, 'Python'))
print(get_average_grade_students(students, 'Ruby'))
print(get_average_grade_lecturers(lecturers, 'Python'))
print(get_average_grade_lecturers(lecturers, 'Ruby'))

print(best_student > worst_student, best_student <
      worst_student, best_student == worst_student)
print(first_lecturer > second_lecturer, first_lecturer <
      second_lecturer, first_lecturer == second_lecturer)

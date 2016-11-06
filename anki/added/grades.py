'''
Grades | Exam statistics (Codecademy)

'''


grades = [100, 100, 90, 40, 80, 100]


def grades_std_deviation(variance):
    return variance ** 0.5  # v ** (1/2)


def grades_variance(scores):
    average = grades_average(scores)
    variance = 0

    for score in scores:
        variance += (average - score) ** 2

    variance /= len(scores)
    return variance


def grades_sum(grades):
    total = 0
    for grade in grades:
        total += grade
    return total


def grades_average(grades):
    sum_of_grades = grades_sum(grades)
    average = sum_of_grades / float(len(grades))
    return average


variance = grades_variance(grades)     # 458.333...
print(grades_std_deviation(variance))  # 21.4087...

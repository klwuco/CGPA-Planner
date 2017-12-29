#!/usr/bin/python3
"""
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
from itertools import combinations_with_replacement, chain, product, groupby
from subject import Subject
"""
Grade Analyzer v1.0
by klwuco (Wu Ka Lok, Cousin)
Printing out the hypothetical CGPA and the grades per subject needed to achieve a target CGPA target range.

Variables to change:
1) current_grade / (current_grade_point and current_credits_taken)
    i)  tuple current_grade: A tuple of the Subject class. (Subject(credit:int, grade:str))
        eg: (Subject(3, 'B'), Subject(3, 'B-'), Subject(3, 'C'), Subject(4, 'A+'), Subject(1, 'F'))
            stands for 4 3-credit course with B, B- and C, a 4-credit course with an A+ and
            a failed 1-credit course. Do not put in P/PP/F courses.
    ii) float current_grade_point
        int   current_credits_taken -- only use the credits counted for GPA, not those with P/PP/F
        self-explanatory. To check both, head to sis -> enroll -> term information -> View my grades
    Note:
        a) Only one (can use both) are needed to be filled for the script to work.
        b) If current_grade, current_grade_point and current_credits_taken are left empty (current_grade set to empty tuple ()),
           hypothetical TGA is calculated instead.

2) float target: Your target CGPA
   float target_max: A cap for the target CGPA.
   Note:
        a) target_max >= target
        b) It is better to have (target_max - target) be small (less than 0.3?)
           or there may be a huge number of results.

3) dict load
   Course credits and number of courses that have that credit for your course to be taken.
   eg: {3:3,4:1,1:2} corresponds to 3 3-credit course, 1 4-credit course and 2 1-credit course.

4) Union(None, tuple) expected
   A tuple of Subject class for any assumed grades for the course to be taken.(Subject(credit:int, grade:str))
   None if there is none expected grades.
   eg: (Subject(4, 'A'), Subject(3, 'B'))

5)
    i) bool write_to_file
       If set to true: redirect the output to a file
    ii)str file_name
       The file to redirect the output to
"""

# Variables
current_grade = (Subject(3, 'B'), Subject(3, 'A-'), Subject(3, 'D'), Subject(4, 'B+'))
current_grade_point = 0
current_credits_taken = 0
target = 3
target_max = 3.02
load = {3: 3, 4: 1}
# expected = (Subject(4, 'A'), Subject(3, 'B'))
expected = None
write_to_file = True
file_name = "result.txt"


def gpa(gradelist=(), current_grade_point=0, current_credits_taken=0):
    weighted_gp = sum(sbj.weighted_grade_point for sbj in gradelist) + current_grade_point * current_credits_taken
    total_load = sum(sbj.credit for sbj in gradelist) + current_credits_taken
    try:
        return weighted_gp / total_load
    except ZeroDivisionError:  # How is that even possible?
        return 0


def main():
    # Generate combinations of grades for each credit
    grades_dict = {}
    for c, r in load.items():
        grades_dict[c] = list(combinations_with_replacement((Subject(c, g) for g in Subject.grade_lookup.keys()), r))
    all_possible_grades_without_expect = list(tuple(chain(*i)) for i in product(*grades_dict.values()))

    # Only choose those that have the expected grade.
    # Can't just use set intersection due to there being repeats
    all_possible_grades = []
    if expected:
        for possible_grades in all_possible_grades_without_expect:
            g = list(possible_grades)
            for grades in possible_grades:
                if grades in expected:
                    g.remove(grades)
            if len(g) == len(possible_grades) - len(expected):
                all_possible_grades.append(possible_grades)
    else:
        all_possible_grades = all_possible_grades_without_expect

    # Compare
    possible_list = []
    for possible_grades in all_possible_grades:
        possible_gpa = gpa(possible_grades + current_grade, current_grade_point, current_credits_taken)
        if target_max >= possible_gpa >= target:
            possible_list.append([possible_gpa, possible_grades])
    possible_list.sort(key=lambda l: l[0])

    # Printing
    if write_to_file:
        import sys
        stdout = sys.stdout
        sys.stdout = open(file_name, 'w')

    print("Your current (C)GPA: {}".format(gpa(current_grade)))
    print("Number of results: {}\n".format(len(possible_list)))
    for possible_gpa, possible_grades in possible_list:
        grades_by_credits = groupby(possible_grades, lambda x: x.credit)
        print("CGPA: {0:.2f}\nGrades required to achieve:".format(possible_gpa))
        for credits, group in grades_by_credits:
            print("{}-credit course: ".format(credits), end="")
            for sbj in group:
                print(sbj.grade, end=" ")
            print()
        print()

    if write_to_file:
        print("The program ran successfully.", file=stdout)
        sys.stdout.close()
        sys.stdout = stdout


if __name__ == "__main__":
    assert 4.3 >= target_max >= target >= 0, "You need to set a realistic target! (need 4.3 >= target_max >= target >= 0)"
    assert sum(load.values()) >= 1, "You need to take SOME course to set a goal do you? (No load)"
    if expected is not None:
        assert len(expected) <= sum(load.values()), "You have so many what-ifs (length of expected too big)! Or invalid input of expected."
    main()

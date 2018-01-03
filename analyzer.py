#!/usr/bin/python3
"""
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

CGPA Planner v1.3
by klwuco (Wu Ka Lok, Cousin)
Printing out the hypothetical CGPA and the grades per subject needed to achieve a target CGPA target range.

For use of analyzer.py, go to README.md.
"""
from itertools import combinations_with_replacement, chain, product, groupby
from subject import Subject

# Variables (for details, please look for readme)
# 1
current_grade_point = 39.1
current_credits_taken = 13

# 2
target = 3.5
target_max = 3.51

# 3
load = {3: 3, 4: 2}

# 4A
# expected = [Subject(4, 'A+'), Subject(3, 'B')]
expected = []

# 4B
min_grade = 'C-'
max_grade = 'A+'

# 5
write_to_file = True
file_name = "result.txt"


def gpa(gradelist=(), current_grade_point=0, current_credits_taken=0):
    weighted_gp = sum(sbj.weighted_grade_point for sbj in gradelist) + current_grade_point
    total_load = sum(sbj.credit for sbj in gradelist) + current_credits_taken
    try:
        return weighted_gp / total_load
    except ZeroDivisionError:
        return 0


def analyze(current_grade_point=0,
            current_credits_taken=0,
            load={},
            target=0, target_max=4.3,
            min_grade='F', max_grade='A+',
            expected=[]):
    assert 4.3 >= target_max >= target >= 0, "You need to set a realistic target! (need 4.3 >= target_max >= target >= 0)"
    assert sum(load.values()) >= 1, "You need to take SOME course to set a goal do you? (No load)"
    assert len(expected) <= sum(load.values()), "You have so many what-ifs (length of expected too big)! Or invalid input of expected."
    # Only generate the combinations using the allowed grades
    allowed_grades = {}
    for key, lookup in Subject.grade_lookup.items():
        if Subject.grade_lookup[min_grade] <= lookup <= Subject.grade_lookup[max_grade]:
            allowed_grades[key] = lookup

    # Generate combinations of grades for each credit without courses with predicted grades
    accounted_load = {}
    if expected:
        for c in load:
            accounted_load[c] = load[c] - len([sbj for sbj in expected if sbj.credit == c])
    else:
        accounted_load = load
    grades_dict = {}
    for c, r in accounted_load.items():
        grades_dict[c] = list(combinations_with_replacement((Subject(c, g)
                                                             for g in allowed_grades.keys()), r))

    # Append back the predicted grades
    if expected:
        all_possible_grades = []
        for i in product(*grades_dict.values()):
            append_list = list(chain(*i)) + list(expected)
            all_possible_grades.append(append_list)
    else:
        all_possible_grades = list(list(chain(*i))
                                   for i in product(*grades_dict.values()))

    # Compare
    possible_list = []
    for possible_grades in all_possible_grades:
        possible_gpa = gpa(possible_grades, current_grade_point, current_credits_taken)
        if target_max >= possible_gpa >= target:
            possible_grades.sort(key=lambda x: (x.credit, -x.grade_point))  # Sort with credit first, then grade in descending order
            possible_list.append([possible_gpa, possible_grades])
    possible_list.sort(key=lambda l: l[0])

    # min tgpa needed
    provisional_credits = sum(c * n for c, n in load.items())
    total_credits = current_credits_taken + provisional_credits
    min_tgpa = (target * total_credits - current_grade_point) / provisional_credits

    # Printing
    if write_to_file:
        import sys
        stdout = sys.stdout
        sys.stdout = open(file_name, 'w')

    print("Your current (C)GPA: {0:.2f}".format(gpa((), current_grade_point, current_credits_taken)))
    print("Current total credits taken: {0}".format(current_credits_taken))
    print("Credits to be taken: {0}".format(provisional_credits))
    print("Target: from {0} to {1}".format(target, target_max))
    print("Minimum TGPA needed: {0:.2f}".format(min_tgpa))
    print("Number of results: {0}\n".format(len(possible_list)))
    for possible_gpa, possible_grades in possible_list:
        grades_by_credits = groupby(possible_grades, lambda x: x.credit)
        tgpa = gpa(possible_grades)
        print("CGPA: {0:.2f} TGPA: {1:.2f}\nGrades required to achieve:".format(possible_gpa, tgpa))
        for credits, group in grades_by_credits:
            print("{0}-credit course: ".format(credits), end="")
            for sbj in group:
                print(sbj.grade, end=" ")
            print()
        print()

    if write_to_file:
        print("The program ran successfully.", file=stdout)
        sys.stdout.close()
        sys.stdout = stdout


if __name__ == "__main__":
    analyze(current_grade_point=current_grade_point,
            current_credits_taken=current_credits_taken,
            load=load,
            target=target, target_max=target_max,
            min_grade=min_grade, max_grade=max_grade,
            expected=expected)

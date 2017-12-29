"""
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""


class Subject:

    # Change this if your grade point system is different
    grade_lookup = {'F': 0, 'D': 1, 'C-': 1.7, 'C': 2, 'C+': 2.3,
                    'B-': 2.7, 'B': 3, 'B+': 3.3, 'A-': 3.7,
                    'A': 4, 'A+': 4.3}

    def __init__(self, credit, grade):
        self.credit = credit
        self.grade = grade

    @property
    def grade_point(self):
        return self.grade_lookup[self.grade]

    @property
    def weighted_grade_point(self):
        return self.credit * self.grade_point

    def __eq__(self, other):
        return self.credit == other.credit and self.grade == other.grade

    def __repr__(self):
        return "({0},{1})".format(self.credit, self.grade)

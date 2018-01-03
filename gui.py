import tkinter as tk
import pygubu
from tkinter.messagebox import showinfo
from subject import Subject
import analyzer


class Application:
    def __init__(self, master):

        self.master = master
        self.builder = builder = pygubu.Builder()

        # Load an ui file
        builder.add_from_file('analyzer.ui')

        # Create the widget using a master as parent
        self.mainwindow = builder.get_object('Frame', master)
        self.title()

        builder.connect_callbacks(self)

        # Initialize defaults
        self.builder.tkvariables['min_grade'].set("F")
        self.builder.tkvariables['max_grade'].set("A+")

    def clicked_how_to_check_value(self):
        showinfo("How to check the values?",
                 """Check your current total grade points and credits at sis -> enroll -> term information -> View my grades"""
                 )

    def title(self):
        self.master.title("CGPA Planner")

    def analyze(self):
        """A wrapper for analyzer.analyze"""
        current_credits_taken = self.builder.tkvariables['current_credits_taken'].get()
        current_grade_point = self.builder.tkvariables['current_grade_point'].get()
        load = {}
        for credit in range(1, 6):
            i = self.builder.tkvariables['load_{}c'.format(credit)].get()
            if i != 0:
                load[credit] = i

        min_grade = self.builder.tkvariables['min_grade'].get()
        max_grade = self.builder.tkvariables['max_grade'].get()

        target = self.builder.tkvariables['target_min'].get()
        target_max = self.builder.tkvariables['target_max'].get()

        expected = []
        for n in range(1, 8):
            credit = self.builder.tkvariables['credit_{}'.format(n)].get()
            expected_grade = self.builder.tkvariables['grade_{}'.format(n)].get()
            if credit != 0 and expected_grade in Subject.grade_lookup.keys():
                expected.append(Subject(credit, expected_grade))
            expected = tuple(expected)

        # Sanity Checks
        if sum(load.values()) < 1:
            showinfo("Error", "You need to take SOME course to set a goal do you?")
            return
        if Subject.grade_lookup[min_grade] > Subject.grade_lookup[max_grade]:
            showinfo("Error", "How is {0} bigger than {1}?".format(min_grade, max_grade))
            return
        if not 0 <= target <= target_max <= 4.3:
            showinfo("Error", "You need to set a realistic target!")
            return

        analyzer.analyze(current_grade_point=current_grade_point,
                         current_credits_taken=current_credits_taken,
                         load=load,
                         target=target, target_max=target_max,
                         min_grade=min_grade, max_grade=max_grade,
                         expected=expected)
        showinfo("Results", "Check results.txt for results.")


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

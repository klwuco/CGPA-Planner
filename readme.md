# Grade analyzer 1.2
By klwuco (Wu Ka Lok, Cousin).<br>
UST itsc: klwuab

## What is this?
This script finds out the hypothetical CGPA and the grades per subject needed to achieve a target CGPA range.


## Requirements
1. python3<br>
    On Mac/Linux, do<br>
    <pre><code>sudo apt-get install python3</code></pre>
    or use your favourite package manager.<br>
    On Windows, download python 3 (Not 2.7) via<br>
    <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>

2. some text editor for opening .py files (eg: vim, gnu nano, notepad, emacs, sublime text, etc.)<br>
    Or use your favourite IDE (eg. vim, PyCharm, VS, etc.)<br>


## Usage
First, edit analyzer.py to change the variables. (refer the the Variables to change section.)

To run the script:
### Mac/Linux
In your terminal, execute
<pre><code>./analyzer.py</code></pre>
or
<pre><code>python3 analyzer.py</code></pre>

### Windows
In cmd, execute
<pre><code>python analyzer.py</code></pre>
or just run analyzer.py directly.<br>
Note: After running the script directly, the program will just exit. To look at your results, change write_to_file to True.


## Variables to change
<pre>
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

4) Results Narrowing options

A) Union(None, tuple) expected
   A tuple of Subject class for any assumed grades for the course to be taken.(Subject(credit:int, grade:str))
   None if there is none expected grades.
   eg: (Subject(4, 'A'), Subject(3, 'B'))

B) str min_grade
   str max_grade
   The min/max (inclusive) grade that are allowed in the results.

5)
    i) bool write_to_file
       If set to True: redirect the output to a file
    ii)str file_name
       The file to redirect the output to
</pre>

## Note
### Grade Point Systems
This script defaults itself to use the 4.3 point system. If your institute uses a different system, change it in subject.py, in the Subject class.<p>

### Results
The number of results can be huge, so narrowing the restrictions, i.e. those in (4) in the section Variable to change, really helps decrease the results, and time taken for you to read it.

# CGPA Planner 1.3
By klwuco (Wu Ka Lok, Cousin).<br>
UST itsc: klwuab

## What is this?
This script finds out the hypothetical CGPA and the grades per subject needed to achieve a target CGPA range.


## Requirements
### Running the frozen gui (Windows only, python 3.6)
1. Get the binary from release.<br>
2. python **3.6**
    On Windows, download python 3.6 via<br>
    <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>

### Running the source code
1. Clone the repo.<br>
2. python3<br>
    On Mac/Linux, do<br>
    <pre><code>sudo apt-get install python3</code></pre>
    or use your favourite package manager.<br>
    On Windows, download python 3 (Not 2.7) via<br>
    <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>

3. some text editor for opening .py files (eg: vim, gnu nano, notepad, emacs, sublime text, etc.)<br>
    Or use your favourite IDE (eg. vim, PyCharm, VS, etc.)<br>

### Running the gui with source code
1. Clone the repo.<br>
2. python3 and text editor
3. install requirements
    Do <br>
    <pre><code>pip3 install -r requirements.txt</code></pre>
    or just do<br>
    <pre><code>pip3 install pygubu</code></pre>

## Usage

### Running the frozen gui (Windows only, python 3.6)
Run gui.exe<br>

### Running the source code
1.Edit analyzer.py to change the variables. (refer the the Variables to change section.)<br>

2.To run the script:<br>
#### Mac/Linux
In your terminal, execute
<pre><code>./analyzer.py</code></pre>
or
<pre><code>python3 analyzer.py</code></pre>

#### Windows
In cmd, execute
<pre><code>python analyzer.py</code></pre>
or just run analyzer.py directly.<br>
Note: After running the script directly, the program will just exit. To look at your results, change write_to_file to True.

### Running the gui from source code
Run gui.py using the instructions above, replacing analyzer.py with gui.py<br>
Be sure to install pygubu first.<br>

## Variables to change
<pre>
1) current_grade_point and current_credits_taken
    i) float current_grade_point
        int   current_credits_taken -- only use the credits counted for GPA, not those with P/PP/F
        self-explanatory. To check both, head to sis -> enroll -> term information -> View my grades
    Note:
        b) If current_grade_point and current_credits_taken are left empty,
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

A) list expected
   A list of Subject class for any assumed grades for the course to be taken.(Subject(credit:int, grade:str))
   None if there is none expected grades.
   eg: [Subject(4, 'A'), Subject(3, 'B')]
   eg: []

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

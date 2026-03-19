# Python Terminal Quiz Program

A simple quiz program that loads a set of questions from a JSON file and asks them to the user.

## User Instructions

### Installing Python
- Download and install the latest version of Python [from the official website](https://www.python.org/downloads/), following the instructions for your operating system.
- This program has no additional dependencies.

### Running the program
From the folder containing the files, run:
```sh
python main.py
```

This will by default attempt to load questions in a file called `questions.json`. To specify a different name for the question file, use:
```sh
python main.py [file-name]
```
for example:
```sh
python main.py test_questions.json
```

### Running the quiz
1. A question will appear in your terminal with all of the possible options.
2. Enter your answer from the list and press Enter.
3. The program will tell you whether your answer is correct.
4. If your answer is wrong:
    1. If the question is set to allow repeated attempts, you will be allowed to choose another option. This will continue until you choose the correct answer
    2. Otherwise, the correct answer(s) will be displayed and the next question will be asked.

### Example quiz
TODO

## Technical Documentation
TODO
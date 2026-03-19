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

### Example quiz flow
```
Question: Who developed the Python Programming Language?
        a: Wick van Rossum
        b: Rasmus Lerdorf
        c: Gudio van Rossum
        d: Niene Stom
Your answer: a
That is not correct. The correct answer was:
        c: Gudio van Rossum
Question: Which type of programming does Python support?
        a: Object-oriented Programming
        b: Structured Programming
        c: Functional Programming
        d: All of the above
Your answer: d
That is correct!
Question: Is Python case sensitive when dealing with identifiers?
        a: Yes
        b: No
        c: Machine dependent
Your answer: a
That is correct!
Question: Which of the following is the correct extension of the Python file?
        a: .python
        b: .pl
        c: .py
        d: .p
Your answer: c
That is correct!
Question: Which of the following is used to define a block of code in Python language?
        a: Indentation
        b: Key
        c: Brackets
        d: All of the above
Your answer: a
That is correct!
```

## Technical Documentation
### Question format
This program uses [JSON](https://www.json.org/json-en.html) to store the question data.

An example question can be seen below:
```json
{
    "question": "An example question", // The question to ask
    "ask_until_correct": false, // Whether to ask the question multiple times. This is optional and defaults to false
    "options": [ // A list of options
        {
            "option": "An example option", // The option text to display
            "correct": false // Whether the option is correct or not. Multiple options can be correct per question. This is optional and defaults to false
        },        
        {
            "option": "Another example option",
            "correct": true
        },

    ]
}
```

A `questions.json` file contains one or more questions in a list, an example can be seen below:

```json
[
    {
        "question": "An example question", // The question to ask
        "ask_until_correct": false, // Whether to ask the question multiple times. This is optional and defaults to false
        "options": [ // A list of options
            {
                "option": "An example option", // The option text to display
                "correct": false // Whether the option is correct or not. Multiple options can be correct per question. This is optional and defaults to false
            },        
            {
                "option": "Another example option",
                "correct": true
            },

        ]
    },    
    {
        "question": "Another example question", // The question to ask
        "ask_until_correct": false, // Whether to ask the question multiple times. This is optional and defaults to false
        "options": [ // A list of options
            {
                "option": "An example option for another question", // The option text to display
                "correct": false // Whether the option is correct or not. Multiple options can be correct per question. This is optional and defaults to false
            },        
            {
                "option": "Another example option for another question",
                "correct": true
            },

        ]
    }

]
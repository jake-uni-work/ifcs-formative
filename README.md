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
```
### Dataclasses
We use dataclasses to hold QuizQuestion information to allow for easier type hinting and validation. These live in `data.py`

```py
# Import dataclasses for data management
from dataclasses import dataclass

# Create two dataclasses for easier data management
@dataclass
class Option:
    """A possible option for a question"""
    option: str # the option text to display
    correct: bool # whether the option is right


@dataclass
class QuizQuestion:
    """A quiz question"""
    question: str # the question itself
    options: list[Option] # a list of possible options for the question
    ask_until_correct: bool # whether we should keep asking the question until the correct answer is entered
    
    @property
    def correct_options(self) -> list[tuple[int, Option]]:
        """Return a list of just the correct options with their original indexes."""
        return [(index, option) for index, option in enumerate(self.options) if option.correct]
```

### Question loader
Questions are loaded via the `load_questions` function in `loader.py`. 

This will:
- Open the specified file in read mode (throwing a `ValueError` if it does not exist)
- Parse the file using `json.load` and check that the root object is an list
- Iterate through the questions in the file and validate and parse them into a `QuizQuestion` dataclass and a list of `Option`s
- Return the parsed `QuizQuestions`


Code:

```py
# Import our dataclasses
from data import QuizQuestion, Option
import os # Import OS for OS level commands
import json # Import JSON for data format parsing

def load_questions(file_name: str) -> list[QuizQuestion]:
    """Load questions from a supplied JSON file"""
    # Check if file exists
    if not os.path.isfile(file_name):
        raise ValueError(f"File {file_name} does not exist.")
    questions: list[QuizQuestion] = []
    with open(file_name, 'r') as fp:
        # Load the JSON data from the questions file
        data = json.load(fp)
        
        # We expect the JSON file to contain an list of questions. If the root is not an list, raise an error
        if not isinstance(data, list):
            raise ValueError(f"File {file_name} is invalid, expected list, found {type(data)!r}")
        
        # Iterate through the questions
        for question_index, question_data in enumerate(data):
            # Check whether the question contains a question
            if "question" not in question_data:
                raise ValueError(f"Invalid question {question_index} in {file_name}: missing question")
            question = question_data["question"]
            
            # This is an optional property which will set whether to keep asking the question until the answer is correct. If it is missing, assume it is False
            ask_until_correct: bool = question_data.get("ask_until_correct", False)

            options: list[Option] = []
            # Check whether the question has options
            if "options" not in question_data:
                raise ValueError(f"Invalid question {question_index} in {file_name}: missing options")
            
            # We assign each answer a letter so we can only have a maximum of 26 per question
            if len(options) > 26:
                raise ValueError(f"Invalid question {question_index} in {file_name}: too many options ({len(options)}), max 26")
            

            for option_index, option_data in enumerate(question_data["options"]):
                # Check whether the option has an option text.
                if "option" not in option_data:
                    raise ValueError(
                        f"Invalid option {option_index} for question {question_index}: missing option text")

                option: str = option_data["option"]
                # Get whether the option is correct. "correct" is not required on all options, so if it is missing from the option, assume it is False
                option_correct: bool = option_data.get("correct", False)

                options.append(Option(option=option, correct=option_correct))
                
            questions.append(QuizQuestion(question, options, ask_until_correct))
    return questions
```

### Utilities
Question options are stored internally as list indexes, but we present them to the user as lettered options. To convert between the two, we use the following utility functions (which convert ASCII codepoints to a list index and vice-versa)

```py
def index_to_letter(index: int) -> str:
    """Convert a list index to an ASCII character a-z"""
    # Only accept from 0-25 (so the 26 letters of the alphabet)
    if index > 25:
        raise ValueError(f"Index must be between 0-25 (got {index})")
    return chr(97 + index)

def letter_to_index(letter: str) -> int:
    """Convert ASCII character a-z or A-Z to a list index"""
    if len(letter) != 1:
        raise ValueError("Letter must be a single character")
    asc = ord(letter)
    # Handle lowercase letters
    if 97 <= asc <= 122:
        return asc - 97
    # Handle uppercase letters
    if 65 <= asc <= 90:
        return asc - 65
    raise ValueError(f"Invalid answer {letter}")
```

### Runner
`main.py` contains a basic `ask_question` function which will ask a `QuizQuestion` to the user.

```py
def ask_question(question: data.QuizQuestion) -> None:
    """Asks a question to the user. By default this will ask until they get it right, set ask_until_correct to True to only ask once."""
    
    # Print the question text and the available options
    print(f"Question: {question.question}")
    for index, opt in enumerate(question.options):
        # We use \t to indent the options
        print(f"\t{util.index_to_letter(index)}: {opt.option}")   
    
    while True:
        # Get the answer from the user
        answer = input("Your answer: ")
        try:
            # Attempt to parse the letter to a list index. letter_to_index will fail if the provided answer is not a letter, so we catch the exception here rather than parsing twice.
            index = util.letter_to_index(answer)
        except ValueError:
            print("That is not a valid answer, please try again!")
            continue
        
        # Check if the parsed index is a valid option
        if index >= len(question.options):
            print(f"{answer} is not an available answer for this question, please try again!")
            continue
        
        option = question.options[index]
        
        if option.correct:
            # If the option is correct, break out of the loop
            print("That is correct!")
            break
        elif question.ask_until_correct:
            # The answer is wrong and this question wants us to keep asking until they get it right
            print("Not quite right, try again!")
        else:
            # The answer is wrong and the question only allows one attempt, so we print the correct answers and exit the loop.
            correct_options = question.correct_options
            correct_options_formatted = "\n".join([f"\t{util.index_to_letter(correct_index)}: {correct_option.option}" for correct_index, correct_option in correct_options])
            answer_text = "answer was" if len(correct_options) == 1 else "answers were"
            print(f"That is not correct. The correct {answer_text}:\n{correct_options_formatted}")
            break
```


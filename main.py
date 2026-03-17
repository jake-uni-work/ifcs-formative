from dataclasses import dataclass
import os  # Import OS library for handling question files
import json  # Import JSON library for parsing question data


# Create two dataclasses for easier data management
@dataclass
class Option:
    option: str
    correct: bool


@dataclass
class QuizQuestion:
    question: str
    options: list[Option]


def index_to_letter(index: int) -> str:
    """Convert a list index to an ASCII character a-z"""
    # Only accept from 0-25 (so the 26 letters of the alphabet)
    if index > 25:
        raise ValueError(f"Index must be between 0-25 (got {index})")
    return chr(97 + index)

def letter_to_index(letter: str) -> int:
    """Convert ASCII character a-z or A-Z to a list index"""
    if len(letter) != 1:
        raise ValueError(f"Letter must be a single character")
    asc = ord(letter)
    # Handle lowercase letters
    if 97 <= asc <= 122:
        return asc - 97
    # Handle uppercase letters
    if 65 <= asc <= 90:
        return asc - 65
    raise ValueError(f"Invalid answer {letter}")


def ask_question(question: QuizQuestion) -> None:
    """Asks a question to the user until they pick the correct answer"""
    print(f"Question:\n{question.question}")
    for index, opt in enumerate(question.options):
        print(f"\t{index_to_letter(index)}: {opt.option}")   
    
    while True:
        answer = input(f"Your answer: ")
        try:
            index = letter_to_index(answer)
        except ValueError:
            print(f"That is not a valid answer, please try again!")
            continue
        
        if index >= len(question.options):
            print(f"{answer} is not an available answer for this question, please try again!")
            continue
        
        option = question.options[index]
        
        if option.correct:
            print(f"That is correct!")
            break
        else:
            print(f"Not quite right, try again!")
        
                   
    


def load_questions(file_name: str) -> list[QuizQuestion]:
    """Load questions from a supplied JSON file"""
    # Check if file exists
    if not os.path.isfile(file_name):
        raise ValueError(f"File {file_name} does not exist.")
    questions: list[QuizQuestion] = []
    with open(file_name, 'r') as fp:
        # Load the JSON data from the questions file
        data = json.load(fp)
        for question_index, question_data in enumerate(data):
            # Check whether the question contains a question
            if "question" not in question_data:
                raise ValueError(f"Invalid question {question_index} in {question_data}: missing question")
            question = question_data["question"]

            options: list[Option] = []
            # Check whether the question has options
            if "options" not in question_data:
                raise ValueError(f"Invalid question {question_index} in {question_data}: missing options")

            for option_index, option_data in enumerate(question_data["options"]):
                # Check whether the option has an option text.
                if "option" not in option_data:
                    raise ValueError(
                        f"Invalid option {option_index} for question {question_index}: missing option text")

                option = option_data["option"]
                # Get whether the option is correct. "correct" is not required on all options, so if it is missing from the option, assume it is False
                option_correct = option_data.get("correct", False)

                options.append(Option(option=option, correct=option_correct))
                
            questions.append(QuizQuestion(question, options))
    return questions


if __name__ == "__main__":
    # TODO: load from file specified on CLI (or default to questions.json if not found)
    questions = load_questions("test_questions.json")
    # Ask the questions
    for question in questions:
        ask_question(question)

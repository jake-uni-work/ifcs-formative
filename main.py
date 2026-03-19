from dataclasses import dataclass
import os  # Import OS library for handling question files
import json  # Import JSON library for parsing question data
import sys # Import sys library to get command line arguments


DEFAULT_QUESTION_FILE_NAME = "questions.json"

# Create two dataclasses for easier data management
@dataclass
class Option:
    option: str
    correct: bool


@dataclass
class QuizQuestion:
    question: str
    options: list[Option]
    ask_until_correct: bool
    
    @property
    def correct_options(self) -> list[tuple[int, Option]]:
        """Return a list of just the correct options with their original indexes."""
        return [(index, option) for index, option in enumerate(self.options) if option.correct]


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


def ask_question(question: QuizQuestion) -> None:
    """Asks a question to the user. By default this will ask until they get it right, set ask_until_correct to True to only ask once."""
    
    # Print the question text and the available options
    print(f"Question: {question.question}")
    for index, opt in enumerate(question.options):
        # We use \t to indent the options
        print(f"\t{index_to_letter(index)}: {opt.option}")   
    
    while True:
        # Get the answer from the user
        answer = input("Your answer: ")
        try:
            # Attempt to parse the letter to a list index. letter_to_index will fail if the provided answer is not a letter, so we catch the exception here rather than parsing twice.
            index = letter_to_index(answer)
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
            correct_options_formatted = "\n".join([f"\t{index_to_letter(correct_index)}: {correct_option.option}" for correct_index, correct_option in correct_options])
            answer_text = "answer was" if len(correct_options) == 1 else "answers were"
            print(f"That is not correct. The correct {answer_text}:\n{correct_options_formatted}")
            break


def load_questions(file_name: str) -> list[QuizQuestion]:
    """Load questions from a supplied JSON file"""
    # Check if file exists
    if not os.path.isfile(file_name):
        raise ValueError(f"File {file_name} does not exist. To specify a different file, run: python main.py [question file name]")
    questions: list[QuizQuestion] = []
    with open(file_name, 'r') as fp:
        # Load the JSON data from the questions file
        data = json.load(fp)
        for question_index, question_data in enumerate(data):
            # Check whether the question contains a question
            if "question" not in question_data:
                raise ValueError(f"Invalid question {question_index} in {question_data}: missing question")
            question = question_data["question"]
            
            # This is an optional property which will set whether to keep asking the question until the answer is correct. If it is missing, assume it is False
            ask_until_correct: bool = question_data.get("ask_until_correct", False)

            options: list[Option] = []
            # Check whether the question has options
            if "options" not in question_data:
                raise ValueError(f"Invalid question {question_index} in {question_data}: missing options")
            

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

# Don't run main code if imported
if __name__ == "__main__":
    # Check if the user has specified a specific question file
    if len(sys.argv) > 1:
        # If they have, use it
        question_file_name = sys.argv[1]
    else:
        # If not, we pick a default
        question_file_name = DEFAULT_QUESTION_FILE_NAME
    
    # Load the questions
    questions = load_questions(question_file_name)
    # Ask the questions
    for question in questions:
        ask_question(question)

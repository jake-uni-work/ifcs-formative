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
import sys # Import sys library to get command line arguments

# Import our other modules
import loader
import data
import util

DEFAULT_QUESTION_FILE_NAME = "questions.json"

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
    questions = loader.load_questions(question_file_name)
    # Ask the questions
    for question in questions:
        ask_question(question)

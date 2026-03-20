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
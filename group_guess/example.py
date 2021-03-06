#! /usr/bin/python3
"""Very basic example code.

Meant to be used as a guide for new games, until a savefile is implemented."""

try:
  # This will work if the group_guess module is installed,
  # as a directory group_guess in sys.path
  import group_guess
except ModuleNotFoundError:
  # If group_guess isn't installed systemwide or per-user, this will import,
  # as it won't look for the module, just a Python source file.
  # Since loading a module group_guess is equivalent to loading __init__
  # within its module folder, and this is within said folder, this just
  # loads the __init__ within group_guess, which is the script folder,
  # manually.
  import __init__ as group_guess

import gi; gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

class ExampleWindow(group_guess.AppWindow):
  def create_questions(self):
    """Create game questions."""
    # group_guess.Answer(displayname, alts=(), ppl=None)
    example_question_answers = [group_guess.Answer("red", ppl=30),
                                group_guess.Answer("blue", ppl=25),
                                group_guess.Answer("yellow", ppl=20)]
    # group_guess.Question(question, the_id, answers)
    example_question_1 = group_guess.Question("What is your favorite color?",
                                              "favorite-color",
                                              example_question_answers)
    # Need to define self.questions
    self.questions = [example_question_1]
    self.game_title = "Example Code"
  # You can define do_subclass_make_widgets() here, although it's optional.

def main():
  test_window = ExampleWindow(debug=True)
  gtk.main()
main()

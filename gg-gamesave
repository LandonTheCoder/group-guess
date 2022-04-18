#! /usr/bin/python3
"""Very basic example code.

Meant to be used as a guide for new games, until a savefile is implemented."""

import group_guess
import gi; gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
import json
from group_guess import debug

class SavedWindow(group_guess.AppWindow):
  def __init__(self, filename, debug=None):
    self.json_fname = filename
    super().__init__(debug)
  def create_questions(self):
    """Create game questions."""
    # Note about json API:
    #>>> json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
    #['foo', {'bar': ['baz', None, 1.0, 2]}]
    f = open(self.json_fname, "r")
    debug(f)
    json_file = json.load(f)
    f.close()
    self.game_title = json_file["game_title"]
    if json_file["debug"] is not None:
      group_guess_debug = json_file["debug"]
      group_guess.group_guess_debug = json_file["debug"]
    tmp_questions = json_file["questions"]
    tmp_questions_obj = []
    debug("json_file = %s" %(json_file))
    for x in tmp_questions:
      tmp_answers = []
      for y in x["answers"]:
        debug("answer_create: y = %s" %(y))
        tmp_answers.append(group_guess.Answer(**y))
      debug("question_create: question=%s," %(x["question"]),
            "the_id = %s" %(x["the_id"]),
            "answers = %s" %(tmp_answers))
      tmp_questions_obj.append(group_guess.Question(x["question"],
                                                    x["the_id"],
                                                    tmp_answers))
    debug("tmp_questions_obj = %s" %(tmp_questions_obj))
    # Need to define self.questions
    self.questions = tmp_questions_obj
  # You can define do_subclass_make_widgets() here, although it's optional.

def example_test():
  from sys import path
  test_window = SavedWindow(path[0] + "/example.json", debug=True)
  gtk.main()
def main(passed_args=None):
  import argparse
  parser = argparse.ArgumentParser(description="Load and play a saved Group Guess game")
  parser.add_argument("file", help="The savefile to open")
  args = parser.parse_args(passed_args)
  test_window = SavedWindow(args.file, debug=True)
  gtk.main()
  
main()

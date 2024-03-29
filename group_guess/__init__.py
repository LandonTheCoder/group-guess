#! /usr/bin/python3
"""This is Group Guess, a digital game kind of like Family Feud, except that
 it doesn't handle as much, and you can write your own questions and answers.

Just know, this is very much a work in progress."""

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk as gtk
from gi.repository import Rsvg as rsvg
from gi.repository import Gio as gio
import pathlib as paths

# To set debugging.
global group_guess_debug; group_guess_debug = True
def debug(*zargs, verbosity=1, **kwargs):
  if group_guess_debug:
    if type(group_guess_debug) == bool:
      print(*zargs, **kwargs)
  if type(group_guess_debug) == int:
    if verbosity <= group_guess_debug:
      print(*zargs, **kwargs)

def find_asset_dir():
  """To locate icons for use."""
  from sys import path
  # sys.path[0] is script directory
  script_dir_path = paths.Path(path[0]).resolve()
  if (script_dir_path.joinpath("assets").exists() and
      script_dir_path.joinpath("assets").is_dir()):
    return script_dir_path.joinpath("assets")
  else:
    # If the importer is separate from the module/library...
    # This also checks for scripts using it as a submodule.
    print("sys.path:", path)
    for x in path[0:]: 
      # x will contain module directories.
      item = paths.Path(x)
      if item.exists():
        # Work around a Python bug that adds invalid paths to sys.path
        print(item, "exists!")
        for y in item.iterdir():
          # y is the actual set of module directories.
          testdir = y.joinpath("assets")
          testfile = testdir.joinpath("cover-1.svg")
          if (testdir.exists() and testdir.is_dir()):
            if (testfile.exists() and testfile.is_file()):
              print("trying %s" %(y.joinpath("assets")))
              return y.joinpath("assets")
      else:
        print("%s is invalid/nonexistent!" %(item))
    # Let's hope this works.
FF_ASSET_PATH_FANCY = find_asset_dir()
# File:/// URIs must be absolute
tmp_asset_uri = FF_ASSET_PATH_FANCY.resolve().as_uri()
if tmp_asset_uri.endswith("/"):
  FF_ASSET_PATH = tmp_asset_uri
else:
  FF_ASSET_PATH = tmp_asset_uri + "/"
del tmp_asset_uri

def _generate_img_asset_item(item_name, scale_factor):
  """Internally fetches the cover file and generates an Image."""
  # There doesn't appear to be a more native creation method.
  cover_file = gio.File.new_for_uri(FF_ASSET_PATH + item_name)
  # rsvg.Handle.new_from_gfile_sync(file: gio.File, flags: rsvg.HandleFlags,
  #                                 cancellable: gio.Cancellable)
  cover_rsvg = rsvg.Handle.new_from_gfile_sync(cover_file,
                                               rsvg.HandleFlags.FLAGS_NONE,
                                               None)
  # I need the DPI! Calculate from scale factor.
  dpi = scale_factor * 96 # Scale factor of 1 is typically 96DPI
  cover_rsvg.set_dpi(dpi)
  cover_pixbuf = cover_rsvg.get_pixbuf()
  cover_img = gtk.Image.new_from_pixbuf(cover_pixbuf)
  cover_img.show()
  return (cover_file, cover_rsvg, cover_pixbuf, cover_img)

class Answer(gtk.Box):
  """This represents an answer to a question."""
  def __init__(self, displayname, alts=(), ppl=None):
    """This initializes the object.

displayname controls what the widget shows.
alts is a list or comparable object containing other names that the answer might be referred to as.
ppl (optional) denotes how many of the Family Feud votes went to this answer. If undesired, pass None."""
    self.displayname = displayname
    self.alts = alts
    self.people = ppl
    self.answers = (displayname,) + tuple(alts)
    self.ppl_lbl = gtk.Label(label="%s" %(ppl if ppl else "?"))
    self.ppl_lbl.set_max_width_chars(3)
    self.displayname_lbl = gtk.Label(label=self.displayname)
    self.displayname_lbl.set_line_wrap(True)
    self.sep = gtk.Separator(orientation=gtk.Orientation.VERTICAL)
    super().__init__(orientation=gtk.Orientation.HORIZONTAL)
    self.set_homogeneous(False)
    # gtk.Box.pack_end(widget, expand, fill, padding)
    self.pack_end(self.ppl_lbl, False, False, 0)
    self.pack_end(self.sep, False, False, 3)
    self.pack_end(self.displayname_lbl, True, True, 0)
    #self.show_all()
class _AnswerWrapper(gtk.Stack):
  """Internal class implementing reveal/switching."""
  def __init__(self, index, answer):
    """Initialize myself."""
    self.index = index
    # self.index Should be between 0 and 7, and is displayed in image as index+1
    self.answer = answer
    super().__init__()
    self.set_homogeneous(True)
    # This creates a gtk.Stack-based wrapper which switches between the answer
    # and its cover item.
    self._generate_cover_item()
    self.add_named(self.cover_img, "cover")
    self.add_named(self.answer, "ans")
    self.set_visible_child_name("cover")
    self.show_all()
    self.set_transition_type(gtk.StackTransitionType.UNDER_UP)
  def _generate_cover_item(self):
    """Internally fetches the cover file and generates an Image."""
    # There doesn't appear to be a more native creation method.
    self.cover_file = gio.File.new_for_uri(FF_ASSET_PATH +
                                           "cover-%s.svg" %(self.index + 1))
    # rsvg.Handle.new_from_gfile_sync(file: gio.File, flags: rsvg.HandleFlags,
    #                                 cancellable: gio.Cancellable)
    self.cover_rsvg = rsvg.Handle.new_from_gfile_sync(self.cover_file,
                                                      rsvg.HandleFlags.FLAGS_NONE,
                                                      None)
    # I need the DPI! Calculate from scale factor.
    scale_factor = self.get_scale_factor()
    dpi = scale_factor * 96 # Scale factor of 1 is typically 96DPI
    self.cover_rsvg.set_dpi(dpi)
    self.cover_pixbuf = self.cover_rsvg.get_pixbuf()
    self.cover_img = gtk.Image.new_from_pixbuf(self.cover_pixbuf)
    self.cover_img.show()
  def show_answer(self):
    """Makes answer visible."""
    self.set_visible_child_name("ans")
    pass # self.stack_switch_something("answer")

class Question(gtk.Box):
  """This represents a question of the game."""
  def __init__(self, question, the_id, answers):
    self.the_id = the_id
    self.question = question
    self.answers = answers # A list-like iterable of Answers
    # An id is necessary to allow selecting the question from the main menu.
    debug("Creating question %s, \"%s\", answers=%s" %(the_id, question, answers))
    super().__init__(orientation=gtk.Orientation.VERTICAL)
    self._make_answers()
    self._make_flow_box()
    self._create_widgets()
    self.show_all()
  def _make_flow_box(self):
    self.flowbox = gtk.FlowBox(orientation=gtk.Orientation.VERTICAL)
    # Flows from top to bottom and wraps to the column to the right, when
    # widgets are added.
    self.flowbox.set_min_children_per_line(4)
    self.flowbox.set_max_children_per_line(4)
    for x in self.switched_answers:
      self.flowbox.add(x)
    if len(self.spacers) > 0:
      for x in self.spacers:
        self.flowbox.add(x)
  def _create_widgets(self):
    self.question_lbl = gtk.Label(label=self.question, wrap=True)
    self.entry_field = gtk.Entry(tooltip_text="Type Guess Here...")
    #gtk.Entry.set_icon_from_icon_name(pos: gtk.EntryIconPosition, name: str)
    self.entry_field.set_icon_from_icon_name(gtk.EntryIconPosition.SECONDARY,
                                             "system-search-symbolic")
    self.entry_field.set_icon_activatable(gtk.EntryIconPosition.SECONDARY,
                                          True)
    # When Enter key pressed
    self.entry_field.connect("activate", self.check_answer)
    # When icon clicked
    self.entry_field.connect("icon-press", self.check_answer_icon)
    self.pack_start(self.question_lbl, False, False, 5)
    self.pack_start(self.flowbox, False, False, 0)
    self.pack_start(self.entry_field, False, False, 5)
  def check_answer_icon(self, guess, *args):
    return self.check_answer(guess)
  def check_answer(self, guess):
    """This checks if the guess matches any of the answers.

    It returns the index of the answer or None."""
    self.entry_field.set_editable(False) #To avoid changing while checking
    text = self.entry_field.get_text()
    the_answer = None
    the_wrapper = None
    has_answer = False
    has_invalid_answer = False
    debug("Question \"%s\" (id %s) checking answers..." %(self.question,
                                                          self.the_id))
    for ans in self.answers:
      debug("Checking answer \"%s\"" %(ans.displayname), verbosity=3)
      for x in ans.answers:
        debug("Checking to see if \"%s\" is in \"%s\"" %(text.casefold().strip(),
                                                         x.casefold().strip())
             )
        # Check for cheats by inputting a tiny string to make more matches
        if len(text.strip()) < 2:
          tiny_answer_dialog = self.make_new_dialog(gtk.MessageType.WARNING,
                                                    "Answer too short")
          tmp_text = "Your answer (\"%s\") was too short." %(text)
          tiny_answer_dialog.format_secondary_text(tmp_text)
          tiny_answer_dialog.run(); tiny_answer_dialog.destroy()
          del tmp_text
          has_invalid_answer = True
          break
        elif text.casefold().strip() in x.casefold().strip():
          the_answer = ans
          has_answer = True
      if has_invalid_answer: break #break can only escape one loop.
    if has_answer:
      for x in self.switched_answers:
        if x.answer is the_answer:
          the_wrapper = x
      if the_wrapper != None:
        the_wrapper.show_answer()
    elif has_invalid_answer:
      debug("Answer invalid. Answer-check loop ended.")
    else:
      self.if_answer_wrong(text) # Place an "Answer Wrong" dialog here.
    self.entry_field.set_text("")
    self.entry_field.set_editable(True)
  #
  def make_new_dialog(self, msgtype, errortext):
    return gtk.MessageDialog(transient_for=self.get_toplevel(),
                             flags=0,
                             message_type=msgtype,
                             buttons=gtk.ButtonsType.OK,
                             text=errortext)
  def if_answer_wrong(self, wrong_answer=None):
    """Display a dialog for a wrong answer."""
    debug("Answer wrong.")
    wrong_answer_dialog = gtk.MessageDialog(transient_for=self.get_toplevel(),
                                            flags=0,
                                            message_type=gtk.MessageType.INFO,
                                            buttons=gtk.ButtonsType.OK,
                                            text="Answer Wrong")
    #wrong_answer_dialog.set_transient_for(self.get_toplevel())
    wrong_answer_dialog.format_secondary_text("The answer you picked "
                                              "(\"%s\") was incorrect." %(wrong_answer))
    wrong_answer_dialog.run(); wrong_answer_dialog.destroy()
    debug("Wrong answer dialog done.")
    #wrong_answer_dialog = gtk.Dialog(modal=True)
    #icon "action-unavailable-symbolic" in gtk.Box
  def _make_answers(self):
    self.switched_answers = []
    for x in range(len(self.answers)):
      self.switched_answers.append(_AnswerWrapper(x, self.answers[x]))
    self.spacers = []
    if (len(self.answers) - 1) < 7:
      for x in range(len(self.answers), 8):
        self.spacers.append(_generate_img_asset_item("cover-answerless.svg",
                                                     self.get_scale_factor())[3]
                           )
    debug("question \"%s\": len(switched_answers) is %s," %(self.question,
                                                            len(self.switched_answers)),
          "len(spacers) is %s" %(len(self.spacers)), verbosity=3)
  def when_button_clicked(self, button, data=None):
    """Need to show myself on the parent window's stack."""
    pass
    if data != None:
      tmp_window = data
    else:
      # Will asking for parent window return the original object?
      tmp_window = self.get_toplevel()
    tmp_window.show_question(self.the_id) #Will this work?
    tmp_window.set_back_button_visible(True)

class AppWindow(gtk.Window):
  """The Window to select and interact with questions."""
  def __init__(self, debug=None):
    """Something"""
    if debug is not None:
      group_guess_debug = debug #Globally configured
    self.game_title = None
    self.create_questions()
    super().__init__()
    self.connect("destroy", gtk.main_quit)
    self._mkwidgets()
    self.add(self.stack)
    pass
    self.hbar.show_all()
    self.set_back_button_visible(False)
    self.show()
  def _mkwidgets(self):
    """Internal widget creator."""
    self.box = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=5)
    self.stack = gtk.Stack()
    self.hbar = gtk.HeaderBar()
    debug("AppWindow.box:", self.box, "\nAppWindow.stack:", self.stack,
         verbosity=3)
    self.hbar.set_show_close_button(True)
    if self.game_title != None:
      self.hbar.set_has_subtitle(True)
      self.hbar.set_title(self.game_title)
      self.hbar.set_subtitle("Group Guess")
    else:
      self.hbar.set_has_subtitle(False)
      self.hbar.set_title("Group Guess")
    # Use back-arrow icon.
    self.back_button = gtk.Button.new_from_icon_name("go-previous-symbolic",
                                                     gtk.IconSize.SMALL_TOOLBAR)
    # Back button goes to homepage
    self.back_button.connect("clicked", self.back_to_home)
    self.hbar.pack_start(self.back_button)
    self.add_box_questions()
    self.box.show_all()
    self.stack.add_titled(self.box, "homepage", "homepage")
    self.add(self.stack)
    self.stack.show_all()
    self.stack.set_visible_child_name("homepage")
    # For debugging: create second window with a StackSwitcher
    if group_guess_debug:
      self.stack_switcher = gtk.StackSwitcher(orientation=gtk.Orientation.VERTICAL)
      self.stack_switcher.set_stack(self.stack)
      self.stack_switch_win = gtk.Window(title="Group Guess Switcher")
      self.stack_switch_win.add(self.stack_switcher)
      self.stack_switch_win.connect("destroy", self.stack_switch_win.destroy)
      self.stack_switch_win.show_all()
    self.do_subclass_make_widgets() # Callback to allow adding additional widgets
    self.set_titlebar(self.hbar)
  def back_to_home(self, item=None):
    """Goes back to home page. Signal item for back_button."""
    self.stack.set_visible_child_name("homepage")
    self.set_back_button_visible(False)
  def add_box_questions(self):
    """Adds Question Buttons, and adds them to the Stack."""
    self.box_buttons = []
    for x in self.questions:
      self.stack.add_titled(x, x.the_id, x.the_id)
      tmp_button = gtk.Button.new_with_label(x.question)
      tmp_button.connect("clicked", x.when_button_clicked, self)
      debug("AppWindow: question %s, id %s, button %s" %(x, x.the_id,
                                                         tmp_button),
            verbosity=3)
      self.box_buttons.append(tmp_button)
      self.box.pack_start(tmp_button, False, False, 0)
  def show_question(self, the_id):
    self.stack.set_visible_child_name(the_id)
  def set_back_button_visible(self, is_visible):
    """Wrapper function to show/hide back button"""
    self.back_button.set_visible(is_visible)
  # Subclass-overridable functions
  def do_subclass_make_widgets(self):
    pass
  def create_questions(self):
    """To be overridden by the subclass.

This will contain the definitions of the questions and their respective answers."""
    # This is required, add the Question objects into here.
    self.questions = []
    # Not required, but game_title should be None if unwanted, not undefined.
    # Must be a string.
    self.game_title = None
    pass

"""Notes to self:
 - If a function doesn't exist, it throws NameError
"""

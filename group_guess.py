#! /usr/bin/python3
"""This is Group Guess, a digital game kind of like Family Feud, except that
 it doesn't handle as much, and you can write your own questions and answers.

Just know, this is very much a work in progress."""

from gi.repository import Gtk as gtk
from gi.repository import Rsvg as rsvg
from gi.repository import Gio as gio
import pathlib as paths

# To set debugging.
global group_guess_debug; group_guess_debug = True

def find_asset_dir():
  """To locate icons for use."""
  from sys import path
  # sys.path[0] is script directory
  script_dir_path = paths.Path(path[0]).resolve()
  if (script_dir_path.joinpath("assets").exists() and
      script_dir_path.joinpath("assets").is_directory()):
    return script_dir_path.joinpath("assets")
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
  cover_pixbuf.set_dpi(dpi)
  cover_pixbuf = self.cover_rsvg.get_pixbuf()
  cover_img = gtk.Image.new_from_pixbuf(self.cover_pixbuf)
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
    self.set_homogenous(False)
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
    self.set_homogenous(True)
    # This creates a gtk.Stack-based wrapper which switches between the answer
    # and its cover item.
    self._generate_cover_item()
    self.add_named(self.cover_img, "cover")
    self.add_named(self.answer, "ans")
    self.set_visible_child_named("cover")
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
    self.cover_pixbuf.set_dpi(dpi)
    self.cover_pixbuf = self.cover_rsvg.get_pixbuf()
    self.cover_img = gtk.Image.new_from_pixbuf(self.cover_pixbuf)
    self.cover_img.show()
  def show_answer(self):
    """Makes answer visible."""
    self.set_visible_child_named("ans")
    pass # self.stack_switch_something("answer")

class Question(object):
  """This represents a question of the game."""
  def __init__(self, question, id, answers):
    self.id = id
    self.question = question
    self.answers = answers # A list-like iterable of Answers
    # An id is necessary to allow selecting the question from the main menu.
    self._make_answers()
    self._make_flow_box()
  def _make_flow_box(self):
    self.flowbox = gtk.FlowBox()
    # Flows from top to bottom and wraps to the column to the right, when
    # widgets are added.
    self.flowbox.set_orientation(gtk.Orientation.VERTICAL)
    self.flowbox.set_max_children_per_line(4)
    for x in self.switched_answers:
      self.flowbox.add(x)
    if len(self.spacers) > 0:
      for x in self.spacers:
        self.flowbox.add(x)
  def _create_widgets(self):
    self.box = gtk.Box(orientation=gtk.Orientation.VERTICAL)
    self.entry_field = gtk.Entry(tooltip_text="Type Guess Here...")
    #gtk.Entry.set_icon_from_icon_name(pos: gtk.EntryIconPosition, name: str)
    self.entry_field.set_icon_from_icon_name(gtk.EntryIconPosition.SECONDARY,
                                             "search-symbolic")
    self.entry_field.set_icon_activatable(gtk.EntryIconPosition.SECONDARY,
                                          True)
    # When Enter key pressed
    self.entry_field.connect("activate", self.check_answer)
    # When icon clicked
    self.entry_field.connect("icon-press", self.check_answer)
  def check_answer(self, guess):
    """This checks if the guess matches any of the answers.

    It returns the index of the answer or None."""
    self.entry_field.set_editable(False) #To avoid changing while checking
    text = self.entry_field.get_text()
    the_answer = None
    the_wrapper = None
    has_answer = False
    print("Question \"%s\" (id %s) checking answers..." %(self.question,
                                                          self.id))
    for ans in self.answers:
      print("Checking answer \"%s\"" %(ans.displayname))
      for x in ans.answers:
        print("Checking to see if \"%s\" is in \"%s\"" %(text.lower().strip(),
                                                         x.lower().strip())
             )
        if text.lower().strip() in x.lower().strip():
          the_answer = ans
          has_answer = True
    if has_answer:
      for x in self.switched_answers:
        if x.answer is the_answer:
          the_wrapper = x
      if the_wrapper != None:
        the_wrapper.show_answer()
    else:
      pass # Place an "Answer Wrong" dialog here.
    self.entry_field.set_editable(True)
  #
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
    print("question \"%s\": len(switched_answers) is %s, len(spacers) is %s" %(len(self.switched_answers),
                                                                               len(self.spacers)))
  def when_button_clicked(self, button, data=None):
    """Need to show myself on the parent window's stack."""
    pass
    if data != None:
      tmp_window = data
    else:
      # Will asking for parent window return the original object?
      tmp_window = self.get_toplevel()
    tmp_window.show_question(self.id) #Will this work?
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
    pass
    self.hbar.show_all()
    self.set_back_button_visible(False)
    self.stack.show_all()
    self.show()
  def _mkwidgets(self):
    """Internal widget creator."""
    self.box = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=5)
    self.stack = gtk.Stack()
    self.hbar = gtk.HeaderBar()
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
    self.stack.set_visible_child_named("homepage")
    self.set_back_button_visible(False)
  def add_box_questions(self):
    """Adds Question Buttons, and adds them to the Stack."""
    for x in self.questions:
      self.stack.add_named(x, x.id)
      tmp_button = gtk.Button.new_with_label(x.question)
      tmp_button.connect("clicked", x.when_button_clicked, self)
      self.box_buttons.append(tmp_button)
      self.box.pack_start(tmp_button, True, True, 0)
  def show_question(self, id):
    self.stack.set_visible_child_named(id)
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
 - Look into a class that transitions between 2 different objects (such as the space filler and the answer)
 - Under Question, use gtk.FlowBox to orient the rows.
 - Window: use gtk.Stack to manage the Questions, and provide a gtk.StackSwitcher for debugging
 - Window: The Questions will be selected by a gtk.Box of gtk.Buttons
 - Use Stack with zstack.set_transition_type(gtk.StackTransitionType.UNDER_UP) for Answer
 - If a function doesn't exist, it throws NameError
"""

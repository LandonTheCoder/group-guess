# group-guess
Group Guess, a Family Feud-like game

This is an attempt to build a game like Family Feud, playable digitally in a manner similar to the Jeopardy games available online. This is still very much a work in progress, with a lot of To-Dos (most importantly testing).

# TODOs #
 - [x] Write the example code. This will show others how to write their own Group Guess game.
 - [ ] Test the code! (The reason why is obvious.)
   - This is partially done. It works, and a single question is answerable. I haven't done more comprehensive testing, though.
 - [ ] Write code to support saved games, so that making a new Group Guess game doesn't require making a subclass, but just importing a save file into data structures. I'm thinking that the save format would use JSON, because that maps quite well to the internal structure of everything, it would just need code to import from JSON.
 - [ ] Making the rest of the icons, including the blank-answer (spacer) icon, most cover icons, and the app icon.
 - [ ] Adding an "Answer wrong" dialog
 - [ ] Adding more debugging hooks
 - [ ] Use gtk.Application API to support app grouping
 - [ ] Optional: Fancy sound effects.
# Helping Out #
You can help out by adding where stuff is missing, and you can find out about the toolkit I used from the website [The Python GTK+ 3 Tutorial](https://python-gtk-3-tutorial.readthedocs.io/en/latest/). See especially Sections 2 (Getting Started), 3 (Basics), and [5 (Widget Gallery)](https://python-gtk-3-tutorial.readthedocs.io/en/latest/gallery.html). Also relevant: [A list of all GTK+ 3 classes in Python 3 bindings](https://lazka.github.io/pgi-docs/Gtk-3.0/classes.html).

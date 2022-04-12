# group-guess
Group Guess, a Family Feud-like game

This is an attempt to build a game like Family Feud, playable digitally in a manner similar to the Jeopardy games available online. This is still very much a work in progress, with a lot of To-Dos (most importantly testing).

# How to use #
The `group_guess.py` file is a library that can be used to create games of Group Guess, which is similar to Family Feud. The `example.py` file is an example of how to use subclasses to create games. The `gg-gamesave.py` file is code that implements JSON-format gamesave importing. The `example.json` file is `example.py` converted into a JSON savefile, with the difference that debugging is disabled on it. The `assets` directory contains the icons used in the game.

The `install*user.sh` script is meant to add an installation within the hierarchy of ~/.local, to support opening a JSON file with the text, `"filetype": "text/x-group-guess+json"` within the first 1, 000 bytes of the text using Group Guess by default. It will register a new MIME type text/x-group-guess+json to make it easier to open Group Guess savefiles, and that change is if that line is present. If you want to use a text editor, simply don't add that property line.
# TODOs #
 - [x] Write the example code. This will show others how to write their own Group Guess game.
 - [ ] Test the code! (The reason why is obvious.)
   - This is partially done. It works, and a single question is answerable. I haven't done more comprehensive testing, though.
   - I also need to test if the asset-finding code works when the group_guess module is separate from the game subclass.
 - [x] Write code to support saved games, so that making a new Group Guess game doesn't require making a subclass, but just importing a save file into data structures. I'm thinking that the save format would use JSON, because that maps quite well to the internal structure of everything, it would just need code to import from JSON.
 - [ ] Making the rest of the icons, including the blank-answer (spacer) icon, most cover icons, and the app icon.
 - [x] Adding an "Answer wrong" dialog
 - [ ] Adding more debugging hooks
 - [ ] Use gtk.Application API to support app grouping
 - [ ] Optional: Fancy sound effects.
# Helping Out #
You can help out by adding where stuff is missing, and you can find out about the toolkit I used from the website [The Python GTK+ 3 Tutorial](https://python-gtk-3-tutorial.readthedocs.io/en/latest/). See especially Sections 2 (Getting Started), 3 (Basics), and [5 (Widget Gallery)](https://python-gtk-3-tutorial.readthedocs.io/en/latest/gallery.html). Also relevant: [A list of all GTK+ 3 classes in Python 3 bindings](https://lazka.github.io/pgi-docs/Gtk-3.0/classes.html).

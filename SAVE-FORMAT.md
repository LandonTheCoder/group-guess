# Group Guess Savefile Format #
This documents the Group Guess savefile format by presenting an example save file and presenting annotations to clarify the purposes of items. I have to include that here, because the JSON format doesn't allow comments in the file.

The Group Guess savefile uses the JSON format, due to the fact it maps well to how it is created internally, and being simpler to parse than something like XML.

# Example Savefile #
Here is the example savefile as of version 1.2.0 (see *group\_guess/example.json*):

```
{
  "game_title": "Example Save",
  "debug": false,
  "filetype": "text/x-group-guess+json",
  "questions": [
    {
      "question": "What is your favorite color?",
      "the_id": "favorite-color",
      "answers": [
        {"displayname": "red", "alts": [], "ppl": 30},
        {"displayname": "blue", "ppl": 25},
        {"displayname": "yellow", "ppl": 20}
      ]
    }
  ]
}
```

# Savefile Properties, Explained #
## The Outer Properties ##

The braces (like "{}") denote an "object" which can contain arbitrarily named properties, which contain either other objects, lists noted by square brackets (like "\[\]"), "strings" of text enclosed in quotes, a true/false type, a numerical type, or a "null" type (meaning that nothing is there). Properties of objects, and items within lists, are separated by commas.

Here is a quote which omits any sub-objects:
```
{
  "game_title": "Example Save",
  "debug": false,
  "filetype": "text/x-group-guess+json",
  "questions": [
    ...something here...
  ]
}
```

The "game\_title" property tells what the game window's title will be. It can be either a string of text, or "null".

The "debug" property controls how much output will be generated when this game is loaded from the console. It is currently a true/false value, but that might change in the future. I would also note that I'm implementing changes that allow the user to enable debugging output with command-line options, by passing the -v (--verbose) option to `gg-gamesave`.

The "filetype" property was an attempt to make Group Guess gamesaves detectable as a subtype of JSON, based on content within. However, that attempt didn't work. This option can be omitted, as it isn't actually used within Group Guess itself. If included, it should be the text string, "text/x-group-guess+json".

The "questions" property contains a list of objects that represent the game's questions within Group Guess. Note the brace at an indent from where the "questions" property occurs. That is an example of a question object.

## Question Objects ##

To make it clearer to read, I will copy the example question here, to make its properties easier to see.

```
{
  "question": "What is your favorite color?",
  "the_id": "favorite-color",
  "answers": [
    {"displayname": "red", "alts": [], "ppl": 30},
    {"displayname": "blue", "ppl": 25},
    {"displayname": "yellow", "ppl": 20}
  ]
}
```

The "question" property is a string of text which contains the question presented to the user.

The "the\_id" property is a string of text, used within Group Guess to uniquely identify the the question as a widget. That ID is necessary, as it utilizes a facility that allows switching between displaying different items, referenced by a text ID (specified by "the\_id" here). It is mandatory, and it must be unique within the game.

The "answers" property contains a list of answer objects that will show, when it is correctly guessed by the user. The answers are added to the question in the order that they appear in the document, so make sure that the list contains the first answer as the first object, second answer as the second object, and so on.

## Answer Objects ##

I also included the answers here for clarity.

```
[
  {"displayname": "red", "alts": [], "ppl": 30},
  {"displayname": "blue", "ppl": 25},
  {"displayname": "yellow", "ppl": 20}
]
```

The "displayname" property defines what will show on the answer card when a correct guess is made. It is a string of text, which is checked case-insensitively when the user makes a guess.

The "alts" property defines what can be accepted as alternative forms of the answer. If present, it should be a list containing either strings of text, or an empty list (shown in the example as "\[\]"). These will also be checked after the "displayname", if present.

The "ppl" property would show how many "people" gave that answer to the question in a hypothetical Family Feud-style survey. If present, it should either be a number (not as a string of text!) or "null".

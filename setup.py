#! /usr/bin/python3
from distutils.core import setup

#email: 100165458+LandonTheCoder@users.noreply.github.com
setup(name="Group Guess",
      version="1.1.2",
      description="Group Guess, a Family Feud clone",
      author="LandonTheCoder",
      author_email="100165458+LandonTheCoder@users.noreply.github.com",
      url="https://github.com/LandonTheCoder/group-guess/",
      packages=["group_guess"],
      scripts=["gg-gamesave.py"],
      package_data={"group_guess": ["assets/*.svg",
                                    "example.json"]
                   }
#      py_modules=["group_guess"]
     )


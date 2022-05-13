#! /usr/bin/python3
##from distutils.core import setup
from setuptools import setup
# Let's hope this works...

#email: 100165458+LandonTheCoder@users.noreply.github.com
setup(name="Group Guess",
      version="1.2.2",
      description="Game implementing a Family Feud clone",
      author="LandonTheCoder",
      author_email="100165458+LandonTheCoder@users.noreply.github.com",
      url="https://github.com/LandonTheCoder/group-guess/",
      packages=["group_guess"],
      scripts=["gg-gamesave"],
      package_data={"group_guess": ["assets/*.svg",
                                    "example.json"]
                   }
#      py_modules=["group_guess"]
     )


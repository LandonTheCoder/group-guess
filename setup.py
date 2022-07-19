#! /usr/bin/python3
# Let's hope this works...
from setuptools import setup
##from distutils.core import setup

#email: 100165458+LandonTheCoder@users.noreply.github.com
setup(name="Group Guess",
      version="1.3.1",
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


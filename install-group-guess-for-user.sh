#! /bin/bash

install_prefix=~/.local
if test -z ${0%%install-group-guess-for-user.sh}; then
  echo "setting to ."
  source_dir=.
else
  source_dir=${0%%install-group-guess-for-user.sh}
fi
echo $source_dir

echo $install_prefix

mkdir -p ~/.local/lib/python3/group_guess
mkdir -p ~/.local/bin
cp -r -t ~/.local/lib/python3/group_guess $source_dir/*
echo "in ~/.local/lib/python3/group_guess:"
ls -l ~/.local/lib/python3/group_guess
ln -s ../lib/python3/group_guess/gg-gamesave.py ~/.local/bin/gg-gamesave
ls -l ~/.local/bin/gg-gamesave

echo "Installing MIME info..."
xdg-mime install ~/.local/lib/python3/group_guess/ltc-group-guess-mime.xml

cat > $install_prefix/share/applications/group-guess.desktop <<EOF
[Desktop Entry]
Version=1.4
Type=Application
Name=Group Guess
Comment=A Digital Family Feud clone
# The input file is a hard requirement, so don't show in the menus
NoDisplay=true;
MimeType=text/x-group-guess+json;
#TryExec=gg-gamesave
Exec=$HOME/.local/bin/gg-gamesave %f
#Icon=fooview
#Actions=Gallery;Create;

#[Desktop Action Gallery]
#Exec=fooview --gallery
#Name=Browse Gallery

#[Desktop Action Create]
#Exec=fooview --create-new
#Name=Create a new Foo!
#Icon=fooview-new

EOF

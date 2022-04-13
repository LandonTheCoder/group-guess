#! /bin/bash

install_prefix=~/.local
if test -z ${0%%install-per-user.sh}; then
  echo "setting to ."
  source_dir=.
else
  source_dir=${0%%install-per-user.sh}
fi
echo "\$source_dir: $source_dir"

echo "\$install_prefix: $install_prefix"

echo "Do know, running this is only necessary if you want Group Guess savefiles
containing \"filetype\": \"text/x-group-guess+json\" to automatically open in
Group Guess. Continue?"

# A variable necessary for POSIX compliance
read -p "Press Enter to Continue, or Ctrl-C to cancel..." add_mime

mkdir -p ~/.local/lib/python3/group_guess
mkdir -p ~/.local/bin
cp -r -t ~/.local/lib/python3/group_guess $source_dir/*
echo "in ~/.local/lib/python3/group_guess:"
ls -l ~/.local/lib/python3/group_guess
ln -s ../lib/python3/group_guess/gg-gamesave.py ~/.local/bin/gg-gamesave
ls -l ~/.local/bin/gg-gamesave

# This is called a "Here document". The <<EOF indicates to stop taking input
# after a line with "EOF". Everything from the line after the one containing
# <<EOF, to the one containing "EOF", is sent to cat, and then sent to
# $install_prefix/share/applications/group-guess.desktop .

cat > $install_prefix/share/applications/group-guess.desktop <<EOF
[Desktop Entry]
Version=1.4
Type=Application
Name=Group Guess
Comment=A Digital Family Feud clone
# The input file is a hard requirement, so don't show in the menus
NoDisplay=true;
# This associates the filetype with Group Guess.
# See "ltc-group-guess-mime.xml" for details.
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

echo "Installing MIME info..."
xdg-mime install ~/.local/lib/python3/group_guess/ltc-group-guess-mime.xml
echo "To stop Group Guess from opening save files automatically, run: "
echo "xdg-mime uninstall $source_dir/ltc-group-guess-mime.xml"

# In-tree PKGBUILD for Arch systems. May break due to the nature of Arch.

# Maintainer: LandonTheCoder <100165458+LandonTheCoder@users.noreply.github.com>
pkgname=group-guess
pkgver=1.3.1
pkgrel=1
pkgdesc="A Family Feud clone"
url="https://github.com/LandonTheCoder/group-guess"
arch=("any")
license=("MIT")
depends=(python gtk3 python-gobject librsvg)
makedepends=(gobject-introspection python-setuptools)
# I don't download source, because this PKGBUILD is in-tree and source is already downloaded.
#source=("$pkgname-$pkgver.tar.gz"::https://github.com/LandonTheCoder/group-guess/archive/v$pkgver.tar.gz")

# I don't include build() because it just copies source anyway. It's pointless.

package() {
  # Debugging output
  echo "srcdir: $srcdir"
  echo "pkgdir: $pkgdir"

  # makepkg does an implied `cd $srcdir`, so PKGBUILD is in the level above it.
  # That is where we need to be.
  cd ..
  echo "Changed directory to \"$PWD\""
  # This builds in PKGBUILD directory, so we do NOT cd $pkgname-$pkgver here.
  python setup.py install --root="$pkgdir"
  install -v -D -m 644 LICENSE -t "$pkgdir/usr/share/licenses/$pkgname/"
  # Install our manpage
  install -v -D -m 644 debian/gg-gamesave.1 -t "$pkgdir/usr/share/man/man1/"
  # Install our README and format documentation to our documentation directory
  install -v -D -m 644 README.md SAVE-FORMAT.md -t "$pkgdir/usr/share/doc/$pkgname/"
  # Install our examples
  install -v -D -m 644 group_guess/example.json \
                       group_guess/example.py -t \
                       "$pkgdir/usr/share/doc/$pkgname/examples/"
}

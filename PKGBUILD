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

package() {
  # Debugging output
  echo "srcdir: $srcdir"
  echo "pkgdir: $pkgdir"
  # makepkg does an implied `cd $srcdir`, so PKGBUILD is in the level above it.
  cd ..
  # This builds in PKGBUILD directory, so we do NOT cd $pkgname-$pkgver here.
  python setup.py install --root="$pkgdir"
  install -v -D -m 644 LICENSE -t "$pkgdir/usr/share/licenses/$pkgname/"
  install -v -D -m 644 debian/gg-gamesave.1 -t "$pkgdir/usr/share/man/man1/"
  # README and format documentation
  install -v -D -m 644 README.md SAVE-FORMAT.md -t "$pkgdir/usr/share/doc/$pkgname/"
  # Examples
  install -v -D -m 644 group_guess/example.json \
                       group_guess/example.py -t \
                       "$pkgdir/usr/share/doc/$pkgname/examples/"
}

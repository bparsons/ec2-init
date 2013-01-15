# ec2-init PKGBUILD
#
# Maintainer: Brian Parsons <brian@pmex.com>
#

pkgname=ec2-init
pkgver=3.4
pkgrel=1
arch=('any')
backup=('etc/conf.d/ec2-init')
license=('MIT')
depends=('postfix' 'python2-boto' 'python2')
source=(ec2-init
        ec2-init.py
        ec2-init.service)
md5sums=('5b2146dd1a1b36fa5bc90422f60895b0'
         'b7fe5fd12f584cf146c6189f68c62664'
         '35a912dd52355d6e3115f396cd694b1d')

package() {

    install -D -m 600 ${srcdir}/ec2-init ${pkgdir}/etc/conf.d/ec2-init
    install -D -m 700 ${srcdir}/ec2-init.py ${pkgdir}/usr/bin/ec2-init.py
    install -D -m 644 ${srcdir}/ec2-init.service ${pkgdir}/usr/lib/systemd/system/ec2-init.service

}


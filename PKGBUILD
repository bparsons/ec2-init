# ec2-init PKGBUILD
#
# Maintainer: Brian Parsons <brian@pmex.com>
#

pkgname=ec2-init
pkgver=3.6
pkgrel=1
arch=('any')
backup=('etc/conf.d/ec2-init')
license=('MIT')
depends=('postfix' 'python2-boto' 'python2')
source=(ec2-init
        ec2-init.py
        ec2-init.service)
md5sums=('7aa841b8f72d34f8beff6aeee013c703'
         '19295c465bab30645f5b485611316aff'
         '85bd3dc0d7c6863a3d5e4a89578644b3')

package() {

    install -D -m 600 ${srcdir}/ec2-init ${pkgdir}/etc/conf.d/ec2-init
    install -D -m 700 ${srcdir}/ec2-init.py ${pkgdir}/usr/bin/ec2-init.py
    install -D -m 644 ${srcdir}/ec2-init.service ${pkgdir}/usr/lib/systemd/system/ec2-init.service

}


# ec2-init PKGBUILD
#
# Maintainer: Brian Parsons <bp@brianparsons.com>
#

pkgname=ec2-init
pkgver=4.0
pkgrel=1
arch=('any')
backup=('etc/conf.d/ec2-init')
license=('MIT')
depends=('python-boto' 'python')
source=(ec2-init
        ec2-init.py
        ec2-init.service)
sha256sums=('79b42c6754209fcb661541e08c1b7af457d3681590bdc40f1a71e22773eac800'
         '3684bf9f2868f3af40990465921ba3d2feb3e877b75d99298a49e9c1f3fa5a3a'
         '45585f8708438cd4fa980f2625531e56beb78221ec426552ff5679bf13c60b05')

package() {

    install -D -m 600 ${srcdir}/ec2-init ${pkgdir}/etc/conf.d/ec2-init
    install -D -m 700 ${srcdir}/ec2-init.py ${pkgdir}/usr/bin/ec2-init.py
    install -D -m 644 ${srcdir}/ec2-init.service ${pkgdir}/usr/lib/systemd/system/ec2-init.service

}


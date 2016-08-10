# ec2-init PKGBUILD
#
# Maintainer: Brian Parsons <brian@pmex.com>
#

pkgname=ec2-init
pkgver=3.8
pkgrel=1
arch=('any')
backup=('etc/conf.d/ec2-init')
license=('MIT')
depends=('python2-boto' 'python2')
source=(ec2-init
        ec2-init.py
        ec2-init.service)
md5sums=('7aa841b8f72d34f8beff6aeee013c703'
         '764a2aa3f7638582392606e7af38fa08'
         'c593bd6d5660038aa6acf4e52d1ab6f7')

package() {

    install -D -m 600 ${srcdir}/ec2-init ${pkgdir}/etc/conf.d/ec2-init
    install -D -m 700 ${srcdir}/ec2-init.py ${pkgdir}/usr/bin/ec2-init.py
    install -D -m 644 ${srcdir}/ec2-init.service ${pkgdir}/usr/lib/systemd/system/ec2-init.service

}


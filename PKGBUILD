# ec2-init PKGBUILD
#
# Brian Parsons <brian@pmex.com>
#

pkgname=ec2-init
pkgver=3.2
pkgrel=1
arch=('any')
license=('proprietary')
depends=('postfix' 'python2-boto' 'python2')
source=(ec2-init.py
        ec2-init.service)
md5sums=('d630c60ea330f95d017020330b538350'
         '35a912dd52355d6e3115f396cd694b1d')

package() {

    install -D -m 700 ${srcdir}/ec2-init.py ${pkgdir}/usr/bin/ec2-init.py
    install -D -m 644 ${srcdir}/ec2-init.service ${pkgdir}/usr/lib/systemd/system/ec2-init.service

}


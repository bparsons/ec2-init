# ec2-init PKGBUILD
#
# Brian Parsons <brian@pmex.com>
#

pkgname=ec2-init
pkgver=3.3
pkgrel=1
arch=('any')
license=('proprietary')
depends=('postfix' 'python2-boto' 'python2')
source=(ec2-init.py
        ec2-init.service)
md5sums=('2e3a4f1f162a8cf695f4a7933d3460f4'
         '35a912dd52355d6e3115f396cd694b1d')

package() {

    install -D -m 700 ${srcdir}/ec2-init.py ${pkgdir}/usr/bin/ec2-init.py
    install -D -m 644 ${srcdir}/ec2-init.service ${pkgdir}/usr/lib/systemd/system/ec2-init.service

}


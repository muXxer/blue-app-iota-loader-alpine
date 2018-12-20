#!/bin/sh
apk update
apk add --no-cache ncurses gnupg curl python3 python3-dev gcc git autoconf pkgconf musl-dev libffi-dev automake libtool libusb-dev eudev-dev linux-headers zlib-dev jpeg-dev
gpg --import public.asc
python3 -m ensurepip
pip3 install --upgrade pip setuptools wheel
pip3 install git+https://github.com/LedgerHQ/blue-loader-python.git
cp iota_loader_blue /etc/init.d/
rc-update add iota_loader_blue
pip3 uninstall pillow
apk del --purge python3-dev gcc git autoconf pkgconf musl-dev libffi-dev automake libtool eudev-dev linux-headers zlib-dev jpeg-dev
rm -r /root/.cache
rm -r /tmp/*
dd if=/dev/zero of=/var/tmp/bigemptyfile bs=4096k ; rm /var/tmp/bigemptyfile
history -c
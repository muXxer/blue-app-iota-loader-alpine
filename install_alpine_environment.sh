#!/bin/sh
apt update
apk add --no-cache curl python3 python3-dev gcc git autoconf pkgconf musl-dev libffi-dev automake libtool libusb-dev eudev-dev linux-headers zlib-dev jpeg-dev
python3 -m ensurepip
rm -r /usr/lib/python*/ensurepip
pip3 install --upgrade pip setuptools wheel
if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi
rm -r /root/.cache
pip3 install git+https://github.com/LedgerHQ/blue-loader-python.git
chmod +x iota_loader
cp iota_loader /etc/init.d/
rc-update add iota_loader

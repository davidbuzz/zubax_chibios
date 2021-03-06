#!/bin/bash
#
# Copyright (c) 2015 Zubax Robotics, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

BM_DEV=$(readlink -f /dev/serial/by-id/usb-Black_Sphere_Technologies_Black_Magic_Probe_*-if00)
PORT=${1:-$BM_DEV}

# Find the firmware ELF
elf=$(ls -1 ../../build/*.elf)
if [ -z "$elf" ]; then
    elf=$(ls -1 build/*.elf)
fi
if [ -z "$elf" ]; then
    echo "No firmware found"
    exit 1
fi

arm-none-eabi-size $elf || exit 1

tmpfile=$(mktemp)
cat > $tmpfile <<EOF
target extended-remote $PORT
mon swdp_scan
attach 1
load
kill
EOF

arm-none-eabi-gdb $elf --batch -x $tmpfile

#!/bin/bash

RR=$(dirname  $1)
FF=$(basename  --suffix=".asm" $1)
SS=$RR/$FF
nasm -felf64  $1 -o $SS.o
ld $SS.o codegen/main.o codegen/crtasm.o \
                -o $SS -dynamic-linker  \
                        /lib64/ld-linux-x86-64.so.2 -lc


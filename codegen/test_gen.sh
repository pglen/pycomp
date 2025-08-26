python codegen.py > aa.asm && \
nasm  -felf64 crt.asm
nasm  -felf64 aa.asm && \
ld  aa.o crt.o -o a.out  &&
./a.out

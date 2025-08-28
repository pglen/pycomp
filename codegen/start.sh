nasm -f elf64 hello.asm
ld hello.o -dynamic-linker /lib64/ld-linux-x86-64.so.2 -lc -melf_x86_64  -o hello

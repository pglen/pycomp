nasm -f elf64 hello.asm
ld hello.o -o hello -dynamic-linker /lib64/ld-linux-x86-64.so.2 -lc -melf_x86_64
#ld hello.o -o hello -dynamic-linker /lib64/ld-linux-x86-64.so.2 -lc -melf_x86_64


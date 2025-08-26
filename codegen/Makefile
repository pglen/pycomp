
all:
	python codegen.py > aa.asm
	nasm  -felf64 -gstabs aa.asm
	nasm  -felf64 -gstabs crt.asm
	ld  aa.o crt.o -o a.out
	./a.out

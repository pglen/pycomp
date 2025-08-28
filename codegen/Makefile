
all:
	@#python codegen.py > aa.asm
	nasm  -felf64 -gstabs main.inc
	nasm  -felf64 -gstabs crtasm.inc
	ld  main.o crtasm.o -o a.out
	./a.out arg1 arg2 arg3

clib:
	nasm  -felf64 -gstabs main.inc
	nasm  -felf64 -gstabs crtasm.inc
	#gcc -v -no-pie -nostdlib main.o crtasm.o -o c.out
	ld -dynamic-linker /lib64/ld-linux-x86-64.so.2 -lc    \
            main.o crtasm.o -lc -o c.out
	./c.out arg1 arg2 arg3

clean:
	@rm -f *.asm
	@rm -f aa.*                                            l
	@rm -f a.out
	@rm -f *.o

# EOF

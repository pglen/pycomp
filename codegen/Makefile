
all:
	python codegen.py > aa.asm
	nasm  -felf64 -gstabs aa.asm
	nasm  -felf64 -gstabs crtasm.inc
	ld  aa.o crtasm.o -o a.out
	./a.out 11 22

clean:
	@rm -f *.asm
	@rm -f aa.*
	@rm -f a.out
	@rm -f *.o

# EOF

extern printf
extern _exit

section .data
    hello:     db 'Hello world!',10

section .text
    global _start
_start:
    xor eax, eax
    mov edi, hello
    call printf
    mov rax, 0
    jmp _exit

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   Compile with NASM

%include "crt.inc"

global main

bits 64

section .text

main:
        ;call    _version

        push    rdx                     ; callee-save registers
        push    rsi                     ; callee-save registers
        push    rdi

        mov     rsi, 1                  ; current value
        mov     rcx, 3                  ; counter

L1:
        push    rsi                     ; caller-save register
        push    rdi                     ; caller-save register

        mov       rdx, rdi              ; third rdx
        mov       rsi, message          ; address of string to output
        mov       rdx, [msg_len]        ; number of bytes

        push      rcx
        call      _print
        pop       rcx

        pop     rdi
        pop     rsi

        loop    L1

        mov     rax, 0xab654321876543ff21

        ;mov     rax, 0x1
        call    _print_num

        ;mov     ax, 'a'
        ;call    _print_char

        call    _printnl

        pop     rdi
        pop     rsi
        pop     rdx
        xor     eax, eax
        ret

section   .data

message:    db        "Hello, World", 10, 0      ; note the newline at the end
msg_len     dq        $ - message



   
END_CODE:
    ;End of program




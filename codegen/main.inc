;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   Compile with NASM

%include "crt.inc"

global main

bits 64

section .text

; main:           %rdi
;  71         argc:           %rsi
;  72         argv:           %rdx
;  73         init:           %rcx
;  74         fini:           %r8
;  75         rtld_fini:      %r9
;  76         stack_end:      stack.  */

main:
        push    rbp
        mov     rbp,rsp

        ;call    _print_regs
        showregs

        mov     rcx, [dumpx_len]
        mov     rsi, dumpx
        call    _print_mem
        call    _printnl

        push    rdx                     ; callee-save registers
        push    rsi                     ; callee-save registers
        push    rdi

        mov     rsi, 1                  ; current value
        mov     rcx, 3                  ; counter
  .L1:
        push    rsi
        push    rdi

        mov       rdx, rdi              ; third rdx
        mov       rsi, message          ; address of string to output
        mov       rdx, [msg_len]        ; number of bytes

        push      rcx
        call      _print
        pop       rcx

        pop     rdi
        pop     rsi

        loop    .L1

        call    _printnl

        mov     rax, 0xfedcba876543210
        call    _print_num

        call    _printnl

        ;mov     ax, 'a'
        ;call    _print_char
        ;call    _printnl

        pop     rdi
        pop     rsi
        pop     rdx

        xor     eax, eax

        mov       rsp, rbp
        pop       rbp

        ret

section   .data
dumpx       db      2, 4, 6, 8, 9, 10, 'a', 'Z', '1', '2', 128, 130

dumpx_len     dq    $ - dumpx

message:    db        "Hello, World", 10, 0      ; note the newline at the end
msg_len     dq        $ - message

; EOF

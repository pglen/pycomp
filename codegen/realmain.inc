;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   Compile with NASM

%include "crt.inc"

global  main

bits 64

section .text
extern printf

main:


     mov     rdi, format2             ; set 1st parameter (format)
     call    printf

    ;mov     rax, 0
    ;mov     rax, [rax]

    ret

format: db      '%d %d', 10, 0
format2: db      "Hello world", 10, 0

test:    db  "test"

; EOF

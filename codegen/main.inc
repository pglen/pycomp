;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   Compile with NASM

%include "crt.inc"

global  _main

bits 64

section .text

extern  main

;; -----------------------------------------------------------------------
; Set up arguments and enviroument like the runtime CRT
;    Strip everything unneeded like trace, debug etc ...
;       but include minimal debugging inf, so gdb cab strp thrue
; Stack layout expected:
;   arg1:    [bp+0]     arg count
;   arg2:    [bp+8]     string arguments back to back
;       passed arg count, environment, till empty string


 extern printf

_main:
        push        rbp
        mov         rbp, rsp

        and     rsp, 0xfffffffffffffff0
        ;call    _print_regs
        ;call    _printnl

        ;xor     rax,rax
        ;mov     rdi, message             ; set 1st parameter (format)
        ;call    printf
        ;call    _print_regs
        ;call    _printnl

        call     main

        mov       rsp, rbp
        pop       rbp

        ret

_print_xargs:

    ;call    _print_regs

        ;call    _printnl
        ;call _getkey
        ;printx "key", rax
        ;call    _printnl

        ; Arguments before stack operations
        ;call    _print_args
        ;call    _printnl

        ;mov rsi, message
        ;call  _print_zstr

        ;mov     rax, "cnt"
        ;call    _print_lab

        lea     rdi, [rbp]
        mov     rcx, [rdi]
        ;add     rcx, 100
        ;printx "cnt", rcx
        mov     rbx, 0

     .L5:
        ;printx  "rbx", rbx
        lea     rdi, [rbp + 8]
        mov     rsi, [rdi]
        add     rsi, rbx

        push    rcx
        push    rbx

        ;call    _print_zstr
        push    rax
        ;printx  "rax", rax
        ;printnl
        pop     rax
        cmp     rax, 0
        je      .end_env

        pop     rbx
        add     rbx, rax
        inc     rbx         ; point to next string
        pop     rcx

        loop .L5
        jmp     .done_scan

     .end_env:
        ;printx  "end", rax
        ;call    _printnl
        pop     rbx
        pop     rcx

     .done_scan:

    ret

_garbage:
 ;      mov     rsi, 1                  ; current value
  ;      mov     rcx, 1                  ; counter
  ;.L1:
  ;      push    rsi
  ;      push    rdi
  ;      mov       rdx, rdi              ; third rdx
  ;      mov       rsi, message          ; address of string to output
  ;      mov       rdx, [msg_len]        ; number of bytes
  ;      push      rcx
  ;      call      _print
  ;      pop       rcx
  ;      pop     rdi
  ;      pop     rsi
  ;      loop    .L1

        ;call    _printnl
        ;mov     rax, 0xfedcba876543210
        ;call    _print_num
        ;call    _printnl

        ;mov     ax, 'a'
        ;call    _print_char
        ;call    _printnl

        ret

section   .data

dumpx       db      2, 4, 6, 8, 9, 10, 'a', 'Z', '1', '2', 128, 130
dumpx_len   dq      $ - dumpx

message:    db      "Hello World in _main.", 10, 0      ; note the newline at the end
msg_len     dq      $ - message
buffer      db      0 dup (4096)

; EOF

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   Compile with NASM

%include "crt.inc"
%include "syscalls.inc"

global  _main, _exit, _start

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

_start:     ; Main entry point

        push      rbp
        mov       rbx, rsp
        mov       rbp, rsp

        mov       [orgstack], rbx
        mov       rbp, rsp
        push      rbp

        mov       rsp, stack_end
        mov       rbp,rsp
        call    _main
        mov     rsp, [orgstack]
        pop     rbp

        mov     rdi, rax                        ; transfer exit code
        jmp     _exit

_main:
        push        rbp
        mov         rbp, rsp

        ;call    _print_regs
        ;call    _printnl
        ;xor     rax,rax
        ;and     rsp, 0xfffffffffffffff0
        ;mov     rdi, message             ; set 1st parameter (format)
        ;call    printf

        ;call    _print_regs
        ;call    _printnl

        call    main
        mov       rsp, rbp
        pop       rbp

        ret

_exit0:
          xor       rdi, rdi                ; Exit code 0
_exit:  ; exit code in rax
          mov       rax, 60                 ; System call for exit
          syscall                           ; Invoke operating system to exit
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

        ;lea     rdi, [rbp]
        ;mov     rcx, [rdi]
        ;add     rcx, 100
        ;printx "cnt", rcx
        ;mov     rbx, 0

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

section   .data

__argc       dq      0
__argv_0     dq      0
__argv_1     dq      0
__argv_2     dq      0
__argv_3     dq      0
__argv_4     dq      0

orgstack    dq      0

dumpx       db      2, 4, 6, 8, 9, 10, 'a', 'Z', '1', '2', 128, 130
dumpx_len   dq      $ - dumpx

message:    db      "Hello World in _main.", 10, 0      ; note the newline at the end
msg_len     dq      $ - message
buffer      db      0 dup (4096)

section .bss

align 64
stack        resb 4096
stack_end:

; EOF

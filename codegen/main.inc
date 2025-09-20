;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   Compile with NASM

%include "crt.inc"
%include "syscalls.inc"

global  _main, _exit, _start
global  __argc, __argv_0, __argv_1, __argv_2, __argv_3, __argv_4
global  __env

bits 64

extern  main

;; -----------------------------------------------------------------------
; Set up arguments and enviroument like the runtime CRT
;    Strip everything unneeded like trace, debug etc ...
;       but include minimal debugging inf, so gdb can step through
; Stack layout expected:
;   arg1:    [bp+8]      arg count
;   arg2:    [bp+16]     string arguments back to back
;       passed arg count, zero, environment. Env ends with empty string.

section .text

_start:     ; Main entry point from kernel

        push      rbp
        mov       rbx, rsp
        mov       rbp, rsp

        ;call    _version

        ; Save environment pointer
        mov         rax, [rbp + 8]  ; Argc +
        add         rax, 3          ; + Argv[0] + Null + Env Ptr
        shl         rax, 3          ; mul by 8

        mov         rbx, rbp
        add         rbx, rax
        lea         rsi, __env
        mov         rcx,[rbx]
        mov         [rsi], rcx

        ; Save passed arguments to local storage. Fixed number of arguments
        lea        rsi, __argc
        mov        rax, [rbp + 1 * 8]
        mov        [rsi], rax
        mov        rsi, __argv_0
        mov        rax, [rbp + 2 * 8]
        mov        [rsi], rax
        lea        rsi, __argv_1
        mov        rax, [rbp + 3 * 8]
        mov        [rsi], rax
        lea        rsi, __argv_2
        mov        rax, [rbp + 4 * 8]
        mov        [rsi], rax
        lea        rsi, __argv_3
        mov        rax, [rbp + 5 * 8]
        mov        [rsi], rax
        lea        rsi, __argv_4
        mov        rax, [rbp + 6 * 8]
        mov        [rsi], rax

        mov       [orgstack], rbx
        mov       rbp, rsp
        push      rbp

        mov       rsp, stack_end
        mov       rbp,rsp

        ;mov rsi, message
        ;call  _print_zstr

        ; ---------------------------
        call    _main               ;; Main entry point
        ; ---------------------------

        mov     rsp, [orgstack]     ; resore stack
        pop     rbp

        mov     rdi, rax            ;; Transfer exit code to rax
        jmp     _exit

; ------------------------------------------------------------------------

_main:
        push        rbp
        mov         rbp, rsp
        sub         rsp, 6 * 8

        ; test: print pointers
        ;mov         rax, [__argc]
        ;call        _print_num
        ;call        _printnl
        ;
        ;mov         rax, [__argv_0]
        ;call        _print_num
        ;call        _printnl
        ;mov         rax, [__argv_1]
        ;call        _print_num
        ;call        _printnl
        ;mov         rax, [__argv_2]
        ;call        _print_num
        ;call        _printnl
        ;mov         rax, [__argv_3]
        ;call        _print_num
        ;call        _printnl
        ;mov         rax, [__argv_4]
        ;call        _print_num
        ;call        _printnl

        ; test: print string
        ;mov         rsi, [__argv_0]
        ;call        _print_zstr
        ;call        _printnl

%if 0
        mov         rsi, [__argv_1]
        cmp         rsi, 0
        je          .env
        call        _print_zstr
        call        _printnl

        mov         rsi, [__argv_2]
        cmp         rsi, 0
        je          .env
        call        _print_zstr
        call        _printnl

        mov         rsi, [__argv_3]
        cmp         rsi, 0
        je          .env
        call        _print_zstr
        call        _printnl

        mov         rsi, [__argv_4]
        cmp         rsi, 0
        je          .env
        call        _print_zstr
        call        _printnl
 %endif

        ; ----------------------------------------------------------------

     .env:

        ;mov     rdi, testenv
        ;printnum rax
        ;extern  getenv
        ;call    getenv
        ;printnum rax
        ;mov     rsi, rax
        ;call    _print_zstr
        ;jmp     .done

        lea         rdi, [ARG1]
        mov         rsi, [__env]
        mov         [rdi], rsi
        lea         rdi, [ARG2]
        mov         qword [rdi], 0
        lea         rdi, [ARG3]
        mov         qword [rdi], 255
        lea         rdi, [ARG4]
        mov         qword [rdi], 0
     .again:
        ;call        _print_zstr
        call        _len_zstr
        lea         rdi, [ARG2]
        mov         [rdi], rax
        ;call        _printnl
    ; Copy key to buffer
    .copy:
        lea         rdi, [ARG1]
        mov         rsi, [rdi]      ; get start of buffer
        lea         rdi, buffer
        mov         rcx, 1024       ; Limit to 1 kb
    ; Parse environment var
    .cagain:
        mov     al, [rsi]
        cmp     al, '='
        je     .labdone
        cmp     al, 0
        je     .labdone
        mov     [rdi], al
        inc     rdi
        inc     rsi
        loop    .cagain
     .labdone:
        mov     byte [rdi], 0
        ;push    rsi
        ;mov     rsi, buffer
        ;call    _print_zstr
        ;pop     rsi
        ;printchar " "

        inc     rsi
        push    rsi
        ;call    _print_zstr
        ;call    _printnl
        pop     rsi

        ; ----------------------------------------------------------------
        ; add environment
        ; Regs:   %rax ; %rdi ; %rsi ; %rdx ; %r10 ;  %r8                                  %r9

        mov     rdi, buffer
        mov     rdx, 1

        call    setenv
        ;printnum rax

        lea         rdi, [ARG2]
        mov         rax, [rdi]
        cmp         rax, 0
        je          .done
        inc         rax

        lea         rdi, [ARG1]
        mov         rsi, [rdi]
        add         rsi, rax
        mov         [rdi], rsi

        dec         qword [ARG3]
        cmp         qword [ARG3], 0
        ja          .again

     .done:

        ;call    _version
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

section   .data

; Save entry values here

__argc       dq      0
__argv_0     dq      0
__argv_1     dq      0
__argv_2     dq      0
__argv_3     dq      0
__argv_4     dq      0
__env        dq      0

orgstack    dq      0
message:    db      "In _main.", 10, 0      ; note the newline at the end

;testenv:     db      "HOME", 0
buffer:      db      4096 dup (0)

section .bss

align 64
stack:        resb 4096
stack_end:

; EOF

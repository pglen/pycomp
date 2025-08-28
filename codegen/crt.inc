;; Macros and exports

bits 64

; Use this macro only as a quick shortcut

%macro pushall 0
            push    rax
            push    rbx
            push    rcx
            push    rdx
            push    rsi
            push    rdi
            push    rbp
%endmacro

%macro popall 0
            pop    rbp
            pop    rdi
            pop    rsi
            pop    rdx
            pop    rcx
            pop    rbx
            pop    rax
%endmacro

%macro showregs 0
    pushall
    call    _print_regs
    call    _printnl
    popall
%endmacro

%macro printx 2
    pushall
    push    %2
    mov     rax,%1
    call    _print_lab
    call    _printsp
    pop     %2
    mov     rax,%2
    call    _print_num
    call    _printsp
    popall
%endmacro

%macro printnl 0
    pushall
    call   _printnl
    popall
%endmacro

%macro showbp 2
        mov rax, %1
        call _print_lab
        call _printsp
        lea   rsi, %2
        mov rax, [rsi ]
        call _print_num
        call _printsp
%endmacro

extern  _print, _print_char, _print_mem, _print_regs
extern  _printsp, _print_num, _print_args, _print_zstr, _print_lab
extern  _printnl, _printsp, _printdot
extern  _exit, _version, _sbrk, _getkey
;, main

; EOF

;; Macros and exports

bits 64

extern  _print, _print_char, _print_mem, _print_regs
extern  _printsp, _print_num, _print_args, _print_zstr, _print_lab
extern  _printnl, _printsp, _printdot
extern  _version, _sbrk, _getkey
extern  _len_zstr, errno

; Library imports
extern  printf, setenv

%define ARG1    rbp-1*8
%define ARG2    rbp-2*8
%define ARG3    rbp-3*8
%define ARG4    rbp-4*8

; The macros have a naming convention of no underscores, they save
; all registers

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

%macro printchar 1
    pushall
    mov     rax, %1
    call    _print_char
    popall
%endmacro

%macro showregs 0
    pushall
    call    _print_regs
    call    _printnl
    popall
%endmacro

%macro printnum 1

    pushall
    mov     rax,%1
    call    _print_num
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

%macro printznl 1
    pushall
    mov     rsi, %1
    call    _print_zstr
    call    _printnl
    popall
%endmacro

%macro showbp 2
    pushall
    mov rax, %1
    call _print_lab
    call _printsp
    lea   rsi, %2
    mov rax, [rsi ]
    call _print_num
    call _printsp
    popall
%endmacro

; EOF

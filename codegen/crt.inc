;; Macros and exports

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

%macro printx 1
    pushall
    mov     rax,%1
    call   _print_num
    popall
%endmacro

%macro printnl 0
    pushall
    call   _printnl
    popall
%endmacro

extern _print, _print_char, _print_mem, _printsp, _print_num, _printnl
extern  _exit, _version

; EOF

;; Macros and exports

; Use this macro only as a quick shortcut

%macro pushall 0
            push    rax
            push    rbx
            push    rcx
            push    rdx
            push    rsi
            push    rdi
%endmacro

%macro popall 0
            pop    rdi
            pop    rsi
            pop    rdx
            pop    rcx
            pop    rbx
            pop    rax
%endmacro

extern _print, _print_char, _print_num, _printnl
extern  _exit, _version

; EOF

; Standard library CRT substitution; only including neccessary functions

global  _exit, _start
global _print, _print_char, _print_num, _printnl
global _version

extern main

bits 64

%include "crt.inc"

section .text

_start:
        ;mov rax, 0                         ; test core dump
        ;mov word [rax], 0
        ;call _version                       ; mostly for testing
        call main
        mov rdi, rax                        ; transfer exit code
        call _exit

_version:
         mov       rsi, message             ; Address of string to output
         mov       rdx, [msg_len]           ; Number of bytes
         call      _print
         mov        eax, 0                  ; Set return value
         ret

_print_char:                                 ; Characteris is in rax

        push      rbp
        mov       rbp, rsp
        sub       rsp, 8

        lea       rsi, [rbp - 4]
        mov       byte [rsi], al

        mov       rdx, 1
        call      _print

        mov       rsp, rbp
        pop       rbp

        ret

_printnl:
         mov       rsi, nl                  ; Address of string to output
         mov       rdx, [nl_len]            ; Number of bytes
         call      _print
         mov        eax, 0                  ; Set return value
         ret

; %rax	arg0 (%rdi)	arg1 (%rsi)	arg2 (%rdx)	arg3 (%r10)	arg4 (%r8)	arg5 (%r9)
;   1	write	0x01	unsigned int fd	  const char *buf	 size_t count
;   arg 0 -- rax    op code  arg 1 -- rdi    handle
;   arg 2 -- rsi    address  arg 3 -- rdx    length

_print:
          mov       rax, 1                  ; System call for write
          mov       rdi, 1                  ; File handle 1 is stdout
          syscall                           ; invoke operating system to do the write
          ret

_print_num:                                 ; Number is in rax

          push      rbp
          mov       rbp, rsp
          sub       rsp, 64

          push      rax
          mov       rcx, 16
          lea       rdi, [rbp - 4]
          mov       qword [rdi], 0
          lea       rsi, [rbp - 8]
   L2:
          push      rax

          push      rax
          and       rax, 0xf
          cmp       rax, 10
          jl        norm_num
          add       rax, 'a' - 10
          jmp       added
         norm_num:
          add       rax, '0'
         added:

          mov       [rsi], al
          dec       rsi
          pop       rax

          push      rax
          and       rax, 0xf0
          shr       rax, 4
          cmp       rax, 15
          jg        err

          cmp       rax, 10
          jl        norm_num2
          add       rax, 'a'- 10
          jmp       added2
         norm_num2:
          add       rax, '0'
         added2:

          mov       [rsi], al
          dec       rsi
          pop       rax

          inc       qword [rdi]

          pop       rax
          shr       rax, 8
          loop      L2

   ;         mov ecx, [rdi]
   ; L3:
   ;         pushall
   ;         mov ax, 's'
   ;         call    _print_char
   ;         popall
   ;         loop    L3

          ;this is a reversed accumulated number
          lea       rsi, [rbp - 8]
          sub       rsi, [rdi]
          mov       rdx, [rdi]
          add       rdx, 1
          call      _print
          pop       rax

        err:

          mov       rsp, rbp
          pop       rbp
          ret

_exit0:
          xor       rdi, rdi                ; Exit code 0
_exit:
          mov       rax, 60                 ; System call for exit
          syscall                           ; Invoke operating system to exit
          ret

section .data

message     db        "CRT Version 1.0", 10  ; Note the newline at the end
msg_len     dq        $-message
message2    db        "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", 10
msg_len2    dq        $-message2
nl          db        10
nl_len      dq        $-nl

; EOF

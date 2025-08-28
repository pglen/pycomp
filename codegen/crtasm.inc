; Standard library CRT substitution; only including neccessary functions
; Named as an .inc so it is not cleaned with the generated assembly

global _print, _print_char, _print_num, _print_lab
global _print_dot, _print_regs, _print_args, _print_zstr
global _printnl, _printsp, _printdot, _getkey
global _exit, _start, _version, _sbrk

%include "crt.inc"

extern _main

section .text

_start:         ; Main entry point
        mov     rbp,rsp

        ;call    _print_args
        ;call    _printnl
        ;lea     rsi, [rsp]
        ;mov     rcx, 8
        ;call    _print_mem
        ;call    _printnl
        ;call    _print_regs

        call    _main
        mov rdi, rax                        ; transfer exit code
        call _exit

_version:       ; Print version
         mov       rsi, message             ; Address of string to output
         mov       rdx, [msg_len]           ; Number of bytes
         call      _print
         mov        eax, 0                  ; Set return value
         ret

_print_lab:       ; String in rax
        push    rax
        shr     rax, 0
        and     rax,0xff
        call    _print_char
        pop     rax
        push    rax
        shr     rax, 8
        and     rax,0xff
        call    _print_char
        pop     rax
        push    rax
        shr     rax, 16
        and     rax,0xff
        call    _print_char
        pop     rax
        push    rax
        shr     rax, 24
        and     rax,0xff
        call    _print_char
        pop     rax
        mov     rax, ':'
        call    _print_char

        mov     rax,0
        ret

_print_zstr:    ; String in rsi

        push      rbp
        mov       rbp, rsp
        sub       rsp, 8
        mov       qword [rbp - 8] , 0

    .again:
        mov     al, byte [rsi]
        cmp     al, 0
        je      .endd
        push    rsi
        push    rbx
        call    _print_char
        pop     rbx
        pop     rsi
        inc     rsi
        inc     qword [rbp - 8]
        inc     rbx
        jmp     .again

    .endd:

        mov       rax, [rbp - 8]
        mov       rsp, rbp
        pop       rbp
        ret

_print_mem:             ; String in rsi, len in rcx

        xor    rax,rax
    .L4:
        push    rcx
        push    rsi

        mov     al, [rsi]
        cmp     rax,127
        ja      .numbers

    .letters:
        cmp     rax,20
        jg      .just_print

    .numbers:
        push      rax
        and       rax, 0xf0
        shr       rax, 4

        cmp       rax, 10
        jl        .norm_num4
        add       rax, 'a' - 10
        jmp       .added4
      .norm_num4:
        add       rax, '0'
      .added4:

        call    _print_char

        pop       rax
        and       rax, 0xf
        cmp       rax, 10
        jl        .norm_num3
        add       rax, 'a'- 10
        jmp       .added3
      .norm_num3:
        add       rax, '0'
     .added3:

    .just_print:
        call    _print_char
        call    _printsp

        pop     rsi
        inc     rsi
        pop rcx

        loop .L4
    ret

_print_char:                                 ; Characteris is in rax

        push      rbp
        mov       rbp, rsp
        sub       rsp, 16

        lea       rsi, [rbp - 4]
        mov       byte [rsi], al

        mov       rdx, 1
        call      _print

        mov       rsp, rbp
        pop       rbp

        ret

_printnl:
        pushall
         mov       rsi, nl                  ; Address of string to output
         mov       rdx, [nl_len]            ; Number of bytes
         call      _print
        popall
         mov        eax, 0                  ; Set return value
         ret

_printsp:
        pushall
         mov       rsi, spx                  ; Address of string to output
         mov       rdx, [spx_len]            ; Number of bytes
         call      _print
        popall
         mov        eax, 0                  ; Set return value
         ret

_printdot:
         pushall
         mov       rsi, dot                  ; Address of string to output
         mov       rdx, [dot_len]            ; Number of bytes
         call      _print
         popall
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

;;  Print number in RAX

_print_num:                                 ; Number is in rax

          pushall

          push      rbp
          mov       rbp, rsp
          sub       rsp, 64

          ; dump stack
          ;mov   rsi, rsp
          ;mov   ecx, 64
          ;call _print_mem

          ; zero stack
          mov       rdi, rsp
          mov       rcx, 64
        .L5:
          ;push      rcx
          mov       byte [rdi], 0
          add       rdi, 1
          ;pop       rcx
          loop      .L5

          ;call _printnl
          ;; dump stack
          ;mov   rsi, rsp
          ;mov   ecx, 64
          ;call _print_mem

          push      rax
          mov       rcx, 16
          lea       rdi, [rbp - 8]              ; Counter
          mov       qword [rdi], 0
          lea       rsi, [rbp - 16]             ; Target end
   .L2:
          push      rax
          push      rax
          and       rax, 0xf
          cmp       rax, 10
          jl        .norm_num
          add       rax, 'a' - 10
          jmp       .added
     .norm_num:
          add       rax, '0'
     .added:
          inc       qword [rdi]
          mov       byte [rsi], al
          dec       rsi
          pop       rax

          push      rax
          and       rax, 0xf0
          shr       rax, 4
          cmp       rax, 15
          jg        .err

          cmp       rax, 10
          jl        .norm_num2
          add       rax, 'a'- 10
          jmp       .added2
     .norm_num2:
          add       rax, '0'
     .added2:

          mov       byte [rsi], al
          dec       rsi
          pop       rax

          inc       qword [rdi]

          pop       rax
          shr       rax, 8
          loop      .L2

          ; this is the reversed accumulated number
          lea       rsi, [rbp - 16]
          sub       qword rsi, [rdi]

          ;back off from last increment
          add       rsi, 1
          mov       rdx, [rdi]
          ;add       rdx, 1
          call      _print
          pop       rax
          jmp       .retx

        .err:
          ; we leave the string blank

        .retx:

          mov       rsp, rbp
          pop       rbp

        popall
        ret

_exit0:
          xor       rdi, rdi                ; Exit code 0
_exit:
          mov       rax, 60                 ; System call for exit
          syscall                           ; Invoke operating system to exit
          ret

_print_regs:        ; print processor registers

        push        rbp
        mov         rbp, rsp
        sub         rsp, 8

        printx  "rax",  rax
        printx  "rbx",  rbx
        call    _printnl
        printx  "rcx",  rcx
        printx  "rdx",  rdx
        call    _printnl
        printx  "rsi",  rsi
        printx  "rdi",  rdi
        call    _printnl
        printx  "r8 ",  r8
        printx  "r9 ",  r9
        call    _printnl
        printx  "r10",  r10
        printx  "r11",  r11
        call    _printnl
        printx  "r12",  r12
        printx  "r13",  r13
        call    _printnl
        printx  "r14",  r14
        printx  "r15",  r15
        call    _printnl
        printx  "rbp",  rbp
        printx  "rsp",  rsp

        printnl

    mov rsp, rbp
    pop rbp
    ret

_print_args:

        showbp "ar0", [rbp ]
        showbp "ar1", [rbp + 1*8]
        printnl
        showbp "ar2", [rbp + 2*8]
        showbp "ar3", [rbp + 3*8]
        printnl
        showbp "ar4", [rbp + 4*8]
        showbp "ar5", [rbp + 5*8]
        printnl
        xor     rax, rax
        ret

_sbrk:  ; get memory boundary add amount in rdi
        mov     rax,  12
        syscall
        ret

buff    db  0, 0

_getkey: ; wait for a key
        mov     rax,  0
        mov     rdi, 1
        mov     rsi, buff
        mov     dx, 1
        syscall
        push rax
        mov ecx, 1
        mov rsi, buff
        call _print_mem
        pop rax
        ret

_addmem:   ; extend memory  amount in rax

        push    rax
        mov     rdi,  0
        call    _sbrk
        ;printx "srax", rax
        mov     rdi,  rax
        pop     rax
        add     rdi, rax
        call    _sbrk
        ;printx "Srax", rax
        mov     rdi,  0
        call    _sbrk
        ;printx "Srax", rax
        ret

section .data

message     db        "CRT Version 1.0", 10  ; Note the newline at the end
msg_len     dq        $-message
nl          db        10
nl_len      dq        $-nl
spx         db        ' '
spx_len     dq        $-spx
dot         db        '.'
dot_len     dq        $-dot

section .bss

section .txt

; EOF

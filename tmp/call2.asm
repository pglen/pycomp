;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                         
;   Compile with NASM                                                     
;                                                                         
;   Automatically generated, will be overwritten.                         
;                                                                         
        extern  printf                                                    
        extern  fflush                                                    
        extern  exit                                                      
        global main                                                       
        bits 64

%include "codegen/crt.inc"

section .text                                                     

main:

    push    rbp
    mov     rbp, rsp

    ;call    _print_regs
    ;mov     rdi, hellodef
    ;and     rsp, 0xfffffffffffffff0
    ;call    printf

    and     rsp, 0xfffffffffffffff0
    mov     rbp, rsp
    mov  rdi  , strz
    mov  rsi  , stry
    mov rax, 0
    mov ax, word [num1]
    mov  rdx  , rax
    mov rax, 0
    mov ax, word [num2]
    mov  rcx  , rax
    mov rax, 0
    mov ax, word [num3]
    mov  r8  , rax
    mov rax, 0
    mov ax, word [num4]
    mov  r9  , rax
    mov rax, 0
    mov ax, word [num5]
    push   rax 
    mov rax, 0
    mov ax, word [num6]
    push   rax 
    xor  rax, rax
    extern printf
    call printf   ; line: 11 -- printf

end_code:    ;  End of program

    ; This is just in case of no exit statement
    ;xor     rax,rax
    ;mov     rdi, endx
    ;and     rsp, 0xfffffffffffffff0
    ;call    printf

    ; Flush stdout, in case of missing terminating newline
    mov     rdi, 0
    call    fflush

    ; Exit here
    ;mov     qword [exit_code], 44   ; test exit code
    mov     rdi, [exit_code]
    call    exit

    ; return value -> exit code
    mov     rax, 0

    mov     rsp, rbp
    pop     rbp

    ret

section .data

exit_code   dq      0
hellodef:   db      "Start program", 10, 0
endx2:      db       "End program.", 10, 0
endx:       db      10, 0

num1 : dw 1234 ; line: 1 -- u16 : num1 = 1234
num2 : dw 5678 ; line: 2 -- u16 : num2 = 5678
num3 : dw 2345 ; line: 3 -- u16 : num3 = 2345
num4 : dw 7890 ; line: 4 -- u16 : num4 = 7890
num5 : dw 9012 ; line: 5 -- u16 : num5 = 9012
num6 : dw 1111 ; line: 6 -- u16 : num6 = 1111
strz : db "Hello World: %s %d %d %d %d %d %d", 10, 0 ; line: 8 -- arr : strz = "Hello World: %s %d %d %d %d %d %d\n"
stry : db "abcd", 0 ; line: 9 -- arr : stry = "abcd"

; EOF

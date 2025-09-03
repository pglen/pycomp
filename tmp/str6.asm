;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                         
;   Compile with NASM                                                     
;                                                                         
;   Automatically generated, will be overwritten.                         
;                                                                         
                                                                          
        global main                                                       
        extern printf                                                     
        section .text                                                     
        bits 64

%include "codegen/crt.inc"

 main:

    push    rbp
    mov     rbp, rsp

    push    rax
    and     rsp, 0xfffffffffffffff0
    ;call   _print_regs
    ;mov     rdi, hellodef
    ;call    printf

str0 = "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605
str0 = "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605
str0 = "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605
str0 = "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605
str0 = "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605
str0 = "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605


    ;mov     rsp, rbp
    ;pop     rbp

   
enc_code:
    ;End of program



    ;call   _print_regs

    ; This is just in case of no exit statement
    ;xor     rax,rax
    ;mov     rdi, endx
    ;and     rsp, 0xfffffffffffffff0
    ;call    printf

    ; return value -> exit code
    mov     rax, 0

    mov     rsp, rbp
    pop     rbp

    ret

section .data

hellodef:   db      "Start program", 10, 0
endx:      db       "End program.", 10, 0
;endx:       db      10, 0


; EOF

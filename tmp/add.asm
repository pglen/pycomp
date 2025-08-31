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



   
enc_code:
    ;End of program



    mov     rdi, endx
    call    printf
    ret
    ret

section .data
format:    db      "Hello world", 10, 0
endx:      db      "End program.", 10, 0


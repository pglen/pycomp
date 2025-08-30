;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                         
;   Compile with NASM                                                     
;                                                                         
                                                                          
        global main                                                       
        extern printf                                                     
        section .text                                                     
        bits 64

%include "codegen/crt.inc"



    main:
        ;mov     rax, 0
        ;mov     rax, [ rax ]

        mov     rdi, format
        call    printf

        ret

    
   
enc_code:
    ;End of program



section .data

    format:    db      "Hello world", 10, 0

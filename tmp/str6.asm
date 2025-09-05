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

str0 : db "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605", 0 ; line: 1 -- arr : str0 = "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605"
str1 : db "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605latin: é00E9 ê00Ea ë00Eb ì00Ec", 0 ; line: 2 -- arr : str1 = "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605"latin: é00E9 ê00Ea ë00Eb ì00Ec"
str2 : db "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605latin: é00E9 ê00Ea ë00Eb ì00Ecpuntuation: ‚201a ‛201b “201c ”201d „201e ‟201f †2020", 0 ; line: 3 -- arr : str2 = "emojies: 😀1F600 😁1F601 😂1F602 😃1F603 😄1F604 😅1F605"latin: é00E9 ê00Ea ë00Eb ì00Ec"puntuation: ‚201a ‛201b “201c ”201d „201e ‟201f †2020"

; EOF

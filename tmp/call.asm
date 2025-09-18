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
    mov  rdi  , strx
    xor  rax, rax
    extern printf
    call printf ; line: 3 -- printf
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

strx : db "Hello World", 10, 0 ; line: 1 -- arr : strx = "Hello World\n" 

; EOF

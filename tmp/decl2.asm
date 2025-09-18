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

aaa : dq 22 ; line: 1 -- u64 : aaa = 22 
bbb : dd 33 ; line: 2 -- u32 : bbb = 33 
ccc : dw 44 ; line: 3 -- u16 : ccc = 44 
ddd : db 55 ; line: 4 -- u8 : ddd = 55 

; EOF

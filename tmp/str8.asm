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

str3 : db "symbols: ✀2700 ✁2701 ✂2702 ✃2703 ✄2704 ✅2705 ✆2706 ", 0 ; line: 1 -- arr : str3 = "symbols: ✀2700 ✁2701 ✂2702 ✃2703 ✄2704 ✅2705 ✆2706 "
str4 : db "symbols: ✀2700 ✁2701 ✂2702 ✃2703 ✄2704 ✅2705 ✆2706 more symbols: ←2190 ↑2191  →2192 ↓2193 ↔2194 ↕2195 ↖2196 ", 0 ; line: 2 -- arr : str4 = "symbols: ✀2700 ✁2701 ✂2702 ✃2703 ✄2704 ✅2705 ✆2706 "more symbols: ←2190 ↑2191  →2192 ↓2193 ↔2194 ↕2195 ↖2196 "
str5 : db "symbols: ✀2700 ✁2701 ✂2702 ✃2703 ✄2704 ✅2705 ✆2706 more symbols: ←2190 ↑2191  →2192 ↓2193 ↔2194 ↕2195 ↖2196 weather: ☀2600 ☁2601 ☂2602 ☃2603 ☄2604 ★2605 ☆2606 ☇2607 ", 0 ; line: 3 -- arr : str5 = "symbols: ✀2700 ✁2701 ✂2702 ✃2703 ✄2704 ✅2705 ✆2706 "more symbols: ←2190 ↑2191  →2192 ↓2193 ↔2194 ↕2195 ↖2196 "weather: ☀2600 ☁2601 ☂2602 ☃2603 ☄2604 ★2605 ☆2606 ☇2607 "

; EOF

section .data
    msg db "Hello World", 0xA  ; Message to display + newline character
    len equ $ - msg             ; Calculate the length of the message

section .text
    global _start               ; Mark _start as the entry point

_start:
    ; syscall: write(1, msg, len)
    mov rax, 1                  ; Syscall number 1 (sys_write)
    mov rdi, 1                  ; File descriptor 1 (stdout)
    mov rsi, msg                ; Pointer to the message
    mov rdx, len                ; Length of the message
    syscall                      ; Make the syscall

    ; syscall: exit(0)
    mov rax, 60                 ; Syscall number 60 (sys_exit)
    xor rdi, rdi                ; Exit code 0
    syscall                      ; Make the syscall
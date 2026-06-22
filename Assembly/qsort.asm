.model small
.stack 100h

.data
msg_n db 'Input n: $'
msg_num db 13,10,'Input number: $'
msg_out db 13,10,'Sorted result: $'

array dw 100 dup(?)
n dw ?

.code

main proc
    mov ax,@data
    mov ds,ax

;---------------- input n ----------------
    lea dx,msg_n
    mov ah,09h
    int 21h

    call input_num
    mov n,ax

;---------------- input array ----------------
    mov cx,n
    mov si,0

input_loop:
    lea dx,msg_num
    mov ah,09h
    int 21h

    call input_num
    mov array[si],ax

    add si,2
    loop input_loop

;---------------- quicksort ----------------
    mov ax,n
    dec ax
    push ax        ; high
    mov ax,0
    push ax        ; low
    call quicksort

;---------------- output ----------------
    lea dx,msg_out
    mov ah,09h
    int 21h

    mov cx,n
    mov si,0

print_loop:
    mov ax,array[si]
    call print_num

    mov dl,' '
    mov ah,02h
    int 21h

    add si,2
    loop print_loop
    
    lea dx,msg_tail
    mov ah,09h
    int 21h

    mov ah,4ch
    int 21h
main endp


;====================================================
; quicksort(low, high)
; [bp+4]=low [bp+6]=high
;====================================================
quicksort proc near
    push bp
    mov bp,sp

    push ax
    push bx
    push cx
    push dx
    push si
    push di

    mov si,[bp+4]     ; low
    mov di,[bp+6]     ; high

    cmp si,di
    jge qs_end

;---------------- pivot = array[low] ----------------
    mov bx,si
    shl bx,1
    mov dx,array[bx]   ; pivot

; i = low, j = high
    mov si,[bp+4]
    mov di,[bp+6]

partition:

;---------------- left scan ----------------
left_scan:
    mov bx,si
    shl bx,1
    cmp array[bx],dx
    jge right_scan
    inc si
    jmp left_scan

;---------------- right scan ----------------
right_scan:
    mov bx,di
    shl bx,1
    cmp array[bx],dx
    jle check_swap
    dec di
    jmp right_scan

;---------------- swap ----------------
check_swap:
    cmp si,di
    jg partition_end

    mov bx,si
    shl bx,1
    mov ax,array[bx]     ; temp1

    mov cx,ax            ; save

    mov bx,di
    shl bx,1
    mov ax,array[bx]     ; temp2

    mov array[bx],cx

    mov bx,si
    shl bx,1
    mov array[bx],ax

    inc si
    dec di
    jmp partition

partition_end:

; quicksort(low, di)
    mov ax,[bp+4]
    push di
    push ax
    call quicksort

; quicksort(si, high)
    mov ax,[bp+6]
    push ax
    push si
    call quicksort

qs_end:
    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    pop bp
    ret 4
quicksort endp


;====================================================
; 输入十进制数
;====================================================
input_num proc near
    push bx
    push cx
    push dx

    xor bx,bx

read:
    mov ah,01h
    int 21h

    cmp al,13
    je done

    sub al,'0'
    mov ah,0

    push ax

    mov ax,bx
    mov dx,10
    mul dx
    mov bx,ax

    pop ax
    add bx,ax
    jmp read

done:
    mov ax,bx

    pop dx
    pop cx
    pop bx
    ret
input_num endp


;====================================================
; 输出十进制数
;====================================================
print_num proc near
    push ax
    push bx
    push cx
    push dx

    mov bx,10
    xor cx,cx

div_loop:
    xor dx,dx
    div bx
    push dx
    inc cx
    cmp ax,0
    jne div_loop

print_loop:
    pop dx
    add dl,'0'
    mov ah,02h
    int 21h
    loop print_loop

    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_num endp

end main
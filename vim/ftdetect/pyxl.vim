function! Detect_pyxl_fasthtml()
	let re = 'coding[:=]\s*pyxl_fasthtml\>'
	if getline(1) =~ re || getline(2) =~ re
		set ft=pyxl_fasthtml
	endif
endfunction

augroup filetypedetect
	au BufRead,BufNewFile *		call Detect_pyxl_fasthtml()
augroup END

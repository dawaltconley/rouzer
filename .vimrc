" set nospell
" set formatoptions=
" set noexpandtab tabstop=8 shiftwidth=8

autocmd Filetype text setlocal formatoptions= nospell noexpandtab tabstop=16 shiftwidth=16

" use @b to mark a word as a section header
let @b = 'biueab2€ýaeaueab3€ýa'
let @n = 'îª±' " newline, unicode hex = eab1
let @d = '¿¿¿Description:¿'
let @r = '¿¿¿Radical¿'

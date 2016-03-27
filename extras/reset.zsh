r() {
local f
f=(~/Projects/dndmake/extras/*(.))
unfunction $f:t 2> /dev/null
autoload -U $f:t
}

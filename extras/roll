_dndmake()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="-h --help -m --male -f --female -t --tall -s --short -b --heavy -l --light"
	races="`{ ls /etc/dndmake/races ; ls ~/.dndmake/races ; } | sed s/_/-/g | sed s/.py//g`"
	alignments="LG NG CG LN NN CN LE NE CE"
	opts="$opts $races $alignments"

	COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
	return 0
}
complete -F _dndmake dndmake

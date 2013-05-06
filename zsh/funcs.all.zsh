typeset -Ux fpath
fpath=( ${ZSH}/functions(N) ${ZSH}/functions/*(/N) ${fpath})
for funcpath in ${^fpath}/*(.N)
do
    autoload -Uz ${funcpath}(:t)
done

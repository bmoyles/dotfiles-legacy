typeset -U fpath
my_fpaths=( ${ZSH}/functions(N) ${ZSH}/functions/*(/N) )
fpath=( ${my_fpaths} ${fpath} )
for func in ${^my_fpaths}/*(.N)
do
    autoload -U ${funcpath}(:t)
done

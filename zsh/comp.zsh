compdir=${ZSH}/completion

autoload -U compinit
compinit

for file in ${COMPDIR}/*.zsh(N)
do
    source ${file}
done

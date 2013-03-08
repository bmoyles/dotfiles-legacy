autoload -U compinit
compinit

zstyle ':completion:*' rehash true

# load more complex completions if they exist
compdir=${ZSH}/completion
for file in ${COMPDIR}/*.zsh(N)
do
    source ${file}
done

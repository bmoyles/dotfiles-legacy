autoload -U colors && colors

#autoload -Uz vcs_info
#zstyle ':vcs_info:*' enable git p4
#precmd() {
#    vcs_info
#}

P_USER_AT="%{$fg[white]%}(%(!.%{$fg[red]%}%U.%{$fg[blue]%})%n %(!.%u.)%{$fg[white]%}at %{$fg[yellow]%}%m%{$fg[white]%})%{$reset_color%}"
P_CURDIR="%{$fg[white]%}(%{$fg[green]%}%~%{$fg[white]%})%{$reset_color%}"
P_TIME="%{$fg[white]%}(%{$fg[magenta]%}%D{%a %Y-%m-%d} %{$fg[cyan]%}%D{%r}%{$fg[white]%})%{$reset_color%}"

PROMPT="
$P_USER_AT-$P_CURDIR
%# "
RPROMPT="$P_TIME"

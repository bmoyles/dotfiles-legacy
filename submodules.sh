#!/bin/sh

DOTFILES=$(dirname $0)
pushd $DOTFILES >/dev/null
git submodule update --init --recursive

popd >/dev/null

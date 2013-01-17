# dotfiles
## deployment
The deployer script will install or remove dotfiles. Things ending in `.link` will get symlinked
to `$HOME/.<thing>`
By default, if `$HOME/.<thing>` exists, it *will* be clobbered. The install command does have a `-b` flag
which will move an existing file or directory (not an existing symlink) to `.<thing>.dotbackup`.
The uninstall action will move your backups back into place if they exist, but will otherwise simply
remove any symlinks that it might be responsible for.
```usage: deployer.py [-h] {install,uninstall} ...

optional arguments:
  -h, --help           show this help message and exit

Actions:
  {install,uninstall}  specify with -h for additional help
    install            Install dotfiles
    uninstall          Remove dotfiles (restoring backups if they exist)


usage: deployer.py install [-h] [-b]

optional arguments:
  -h, --help    show this help message and exit
  -b, --backup  Create backups before clobbering conflicts

```


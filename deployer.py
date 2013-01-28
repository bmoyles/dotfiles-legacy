#!/usr/bin/env python

import argparse
import fnmatch
import logging
import os
import os.path
import shutil
import sys


SCRIPT = os.path.abspath(__file__)
SCRIPT_PATH = os.path.dirname(SCRIPT)
LINKABLE = '.link'
EXCLUDE_DIRS = ('.git',)
BACKUP_EXT = '.dotbackup'

DEST = os.environ['HOME']

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def find_links(path=None):
    links = set()
    for (root, dirs, files) in os.walk(path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        dir_links = [os.path.join(root, d) for d in dirs if d.endswith(LINKABLE)]
        file_links = [os.path.join(root, f) for f in files if f.endswith(LINKABLE)]
        links.update(dir_links, file_links)

        # don't traverse into dirs that are to be linked
        dirs[:] = [d for d in dirs if not d.endswith(LINKABLE)]
    return links


def backup(path=None):
    if path is None:
        return
    backup_path = path + BACKUP_EXT
    log.info("Backing up {} to {}".format(path, backup_path))
    if os.path.exists(backup_path):
        log.info("Clobbering old backup")
        if os.path.isdir(backup_path):
            shutil.rmtree(backup_path, ignore_errors=True)
        else:
            os.remove(backup_path)
    os.rename(path, backup_path)


def install(links, main_args, *args, **kwargs):
    log.info("Executing install action")
    for link in links:
        log.info("Processing link: {}".format(link))
        destfile = "." + os.path.basename(link).rstrip(LINKABLE)
        dest = os.path.join(DEST, destfile)
        if os.path.exists(dest):
            log.info("Destination exists: {}".format(dest))
            if main_args.backup:
                backup(dest)
            else:
                log.info("Removing existing {}".format(dest))
                if os.path.isdir(dest) and not os.path.islink(dest):
                    log.info("Recursivly removing {}".format(dest))
                    shutil.rmtree(dest, ignore_errors=True)
                else:
                    log.info("Removing file or symlink {}".format(dest))
                    os.remove(dest)
        log.info("Symlinking {} to {}".format(link, dest))
        os.symlink(link, dest)


def uninstall(links, main_args, *args, **kwargs):
    log.info("Executing uninstall action")
    files = ["." + os.path.basename(link).rstrip(LINKABLE) for link in links]
    for filename in files:
        log.info("Processing file: {}".format(filename))
        filename = os.path.join(DEST, filename)
        backup = filename + BACKUP_EXT
        if os.path.islink(filename):
            log.info("File {} is symlink, removing".format(filename))
            os.remove(filename)
        if os.path.exists(backup) and not(os.path.exists(filename)):
            log.info("Backup {} found, moving to {}".format(backup, filename))
            os.rename(backup, filename)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Actions', help='specify with -h for additional help')

    install_parser = subparsers.add_parser('install', help='Install dotfiles')
    install_group = install_parser.add_mutually_exclusive_group(required=False)
    install_group.add_argument('-b', '--backup', action='store_true', help='Create backups before clobbering conflicts')
    install_parser.set_defaults(func=install)

    uninstall_parser = subparsers.add_parser('uninstall', help='Remove dotfiles (restoring backups if they exist)')
    uninstall_parser.set_defaults(func=uninstall)

    return parser.parse_args()

def main():
    args = parse_args()
    log.info("Script: [{0}] Dotfile root: [{1}]".format(SCRIPT, SCRIPT_PATH))
    log.info("Gathering links")
    links = find_links(SCRIPT_PATH)

    log.info("Processing links")
    args.func(links, args)


if __name__ == '__main__':
    sys.exit(main())

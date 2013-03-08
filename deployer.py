#!/usr/bin/env python

import argparse
import fnmatch
import logging
import os
import os.path
import shutil
import sys


script = os.path.abspath(__file__)
script_path = os.path.dirname(script)

link_extension = '.link'
backup_extension = '.dotbackup'
target_path = os.environ['HOME']
dotfiles_config = os.path.join(target_path, '.dotrc')
# directories we want to avoid walking
exclude_dirs = set(('.git',))
# link names that we only want symlinked on specific platforms
platform_links= {
    'darwin': (
        'osx.link',
    ),
    'linux2': (
    ),
}

log = logging.getLogger(__name__)
log_format = '%(asctime)s :: [%(levelname)s] :: [%(filename)s(%(lineno)s):%(funcName)s] :: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


def add_dotrc():
    log.info('Configuring dotfiles location ({0}) in dotrc ({1})'.format(script_path, dotfiles_config))
    if os.path.exists(dotfiles_config):
        log.warn('File exists: {0}, overwriting'.format(dotfiles_config))
    with open(dotfiles_config, 'w') as dotrc:
        dotrc.write('DOTFILES="{0}"\n'.format(script_path))


def remove_dotrc():
    log.info('Removing dotfiles configuration file ({0})'.format(dotfiles_config))
    if not os.path.exists(dotfiles_config):
        log.info('Dotfiles configuration file {0} not found'.format(dotfiles_config))
        return
    os.remove(dotfiles_config)


def platform_link_excludes():
    """
    Returns a set of link names to exclude from symlinking on this platform.
    We look at our platforms (platform_links.keys()), filter out sys.platform from
    that list, and then create a flattened set of files for the remaining keys in
    the platform_links dict
    """
    other_platforms = set(platform_links.keys()) - set(sys.platform)
    excludes = set([exclusion for platform in other_platforms for exclusion in platform_links[platform]])
    log.info('Detected platform: {0}. Not linking: {1}'.format(sys.platform, str(excludes)))
    return excludes


def find_links(path=None):
    links = set()
    link_excludes = platform_link_excludes()

    for (root, dirs, files) in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        dir_links = [os.path.join(root, d) for d in dirs if d.endswith(link_extension)]
        file_links = [os.path.join(root, f) for f in files
                if f.endswith(link_extension) and f not in link_excludes]
        links.update(dir_links, file_links)

        # don't traverse into dirs that are to be linked
        dirs[:] = [d for d in dirs if not d.endswith(link_extension)]
    return links


def backup(path=None):
    if path is None:
        return
    backup_path = path + backup_extension
    log.info("Backing up {0} to {1}".format(path, backup_path))
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
        log.info("Processing link: {0}".format(link))
        destfile = "." + os.path.basename(link).rstrip(link_extension)
        dest = os.path.join(target_path, destfile)
        if os.path.exists(dest):
            log.info("Destination exists: {0}".format(dest))
            if main_args.backup:
                backup(dest)
            else:
                log.info("Removing existing {0}".format(dest))
                if os.path.isdir(dest) and not os.path.islink(dest):
                    log.info("Recursivly removing {0}".format(dest))
                    shutil.rmtree(dest, ignore_errors=True)
                else:
                    log.info("Removing file or symlink {0}".format(dest))
                    os.remove(dest)
        log.info("Symlinking {0} to {0}".format(link, dest))
        os.symlink(link, dest)
    add_dotrc()


def uninstall(links, main_args, *args, **kwargs):
    log.info("Executing uninstall action")
    files = ["." + os.path.basename(link).rstrip(link_extension) for link in links]
    for filename in files:
        log.info("Processing file: {0}".format(filename))
        filename = os.path.join(target_path, filename)
        backup = filename + backup_extension
        if os.path.islink(filename):
            log.info("File {0} is symlink, removing".format(filename))
            os.remove(filename)
        if os.path.exists(backup) and not(os.path.exists(filename)):
            log.info("Backup {0} found, moving to {1}".format(backup, filename))
            os.rename(backup, filename)
    remove_dotrc()


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
    log.info("Script: [{0}] Dotfile root: [{1}]".format(script, script_path))
    log.info("Gathering links")
    links = find_links(script_path)

    log.info("Processing links")
    args.func(links, args)


if __name__ == '__main__':
    sys.exit(main())

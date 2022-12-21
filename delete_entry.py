# -*- coding: utf-8 -*-

""" 
Quickly removes the accumulated set of files 
(and empty directories) that are older than --mtime days.

This is usually in demand when many millions of files have accumulated 
and/or they have deep nesting. 
Standard removal methods are ineffective in this case. 
Perl scripts were found as a solution (they are very complex and 
it is not obvious how to update them, and it is also scary to run them), 
and this script was written as an alternative to solving the problem.

Principle of operation:

instead of traversing the entire tree and reading all the service information, 
this script accepts only a flat (1)"snapshot of the tree (2)" as input, 
without requesting service information for each object upon receipt.

Standard methods like rm or find -delete work exactly according 
to this scheme - they bypass the tree, pulling the service info from each file, 
and then they request it again when deleting, 
a lot of expensive operations come out in the case of millions of files.

1. Deletes older INT day --mtime
2. Deletes nested directories if they are completely empty.

Launch example.

python delete_entry.py --folder /home/folder --mtime 10

Feature:

- option 'all' in --mtime (--mtime all). Does not pay attention to the date.

FYI
1) It can load the processor and disks, 
so it may be useful to use the squeak in conjunction with nice/ionice utilities.
2) The script can be run with legacy pyhon2 and also with python3. 
The difference is that the `scandir` module is already included in python3, 
and python2 needs an additional pip - `scandir` package. 
If this is the problem, the creak will inform you.

At the end of the work, a report is displayed.

developed by https://t.me/bot_36

"""

try:
    from os import scandir
except ImportError or ModuleNotFoundError:
    try:
        from scandir import scandir
    except ImportError or ModuleNotFoundError:
        print('need \'pip install scandir\'')
        exit()

from os import rmdir, remove
import time
import argparse


parser = argparse.ArgumentParser(description='Example: \n \n \
                python3 delete_entry.py \
                --folder /home/folder --mtime 10')
parser.add_argument("--folder", type=str,
                    help="Get full path folder,example - /home/folder ")
parser.add_argument("--mtime", type=str, help="Old days for last change files? Or get 'all'")

recived_args = parser.parse_args()
recived_folder = recived_args.folder
recived_mtime = recived_args.mtime


count_deleted_file = 0
count_deleted_empty_dir = 0


def iter_dir_loop(path,threshold_mtime = 0):
    for entry in scandir(path):
        if entry.is_file():
            deleter_file(entry, threshold_mtime)
        if entry.is_dir():
            if deleter_empty_dir(entry):
                continue
            else:
                iter_dir_loop(entry.path, threshold_mtime)
                deleter_empty_dir(entry)

def deleter_empty_dir(entry):
    global count_deleted_empty_dir
    if next(scandir(entry.path), 'empty') == 'empty':
                rmdir(entry.path)
                count_deleted_empty_dir += 1
                return True
    return False


def deleter_file(entry, threshold_mtime = 0):
    global count_deleted_file

    if threshold_mtime == 0:
        remove(entry.path)
        count_deleted_file += 1
    elif threshold_mtime > int(entry.stat().st_mtime):
        remove(entry.path)
        count_deleted_file += 1


def init_delete(recived_folder, recived_mtime):
    start_time = int(time.time())
    print('Script starting in ' + time.ctime())

    try:
        if recived_mtime == 'all':
            iter_dir_loop(recived_folder)
        elif recived_mtime.isdigit():
            mtime_days = int(recived_mtime)
            threshold_mtime = int(time.time() - (mtime_days * 24 * 60 * 60))
            iter_dir_loop(recived_folder, threshold_mtime)
        else:
            raise ValueError(' --- [Error]: wrong value in \'--mtime\' --- ')
    except KeyboardInterrupt as e:
        print('   [!!!] Manual stopping the script [!!!]   ')
    
    finally:
        finished_ctime = time.ctime()
        finished_time = int(time.time())
        total_time = finished_time - start_time
        print('Script finished in %s \n \
                --//--//--/score/--//--//-- \n \
                [deleted files]:  %s, \n \
                [deleted empty dirs]: %s, \n \
                [the deletion took %s second] \n \
                 --//--//--//--//--//--//--' % (finished_ctime, count_deleted_file, count_deleted_empty_dir, total_time ))


if __name__ == '__main__':
    init_delete(recived_folder, recived_mtime)

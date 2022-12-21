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
so it may be useful to use together in conjunction with nice/ionice utilities.
2) The script can be run with legacy pyhon2 and also with python3. 
The difference is that the `scandir` module is already included in python3, 
and python2 needs an additional pip - `scandir` package. 
If this is the problem, the script will inform you.

At the end of the work, a report is displayed.

developed by https://t.me/bot_63
python2



# fast_cleaner_cache
If there are millions of files accumulated in your folder (for example, a cache), or all this is in a large nesting, then try this script.

The main problem of cleaning folders with millions of files, or if all this is in a large nesting, is getting a list of all files/folders.

This script acts differently, it does not first bypass the entire tree. It immediately requests the tree without traversing.
Then recursively traverses the nested directories, one at a time. If there are directories in them, then it passes in them as well. 
Then, if the nesting is reached , it puts all the files in a sheet. 
(This is done so that they do not turn to the tree every time.)
And checks the files with the mtime value.
If the files are all deleted in the end, it checks that there are no files left in the directory and deletes it.
Then it goes to the next directory in the same horizontal of the tree.

For example, you specify the directory to clear /var/www/project/cache
At first, it will clean the deep nesting and only at the very end it will come to clean the one lying directly in the 'cache'.



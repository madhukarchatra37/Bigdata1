import glob, re

file = '~/wiki.txt'     # Output file to home

fo = open(file,'w')     # Open output file
f1 = open("all.txt.xml", 'r')   # Open file from directory
f2 = f1.read().strip('</DOC>').split('</DOC>\n<DOC>')       #Strip DOC tags from each en of file, Split by DOC tags and Newlines
f1.close()          # Close file
for f_sub in f2:    # Loop through all entries in f2 list (single wiki entry)
    f_inc = ''.join(f_sub.split('\n'))                      # Split then join to strip newlines from each entry
    f_inc = '|'.join(re.split('<\D?\w+><\D?\w+>',f_inc)) # Split on tags and join with \001 as a line delimiter
    f_inc = re.sub('</text>|<title>','',f_inc)              # Substitute any remaining tags with an empty string
    fo.write(f_inc+'\n')                                    # Write entry to file
fo.close()              # Close the output file



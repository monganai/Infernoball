lines_seen = set() # holds lines already seen
outfile = open("uniquejohn.pot", "w")
for line in open("john.pot", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
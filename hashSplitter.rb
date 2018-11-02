if ARGV.length != 1
    puts "We need exactly one parameter. The name of a file."
    exit;
end


out_file1 = File.new("sha512.hashes", "w")
out_file2 = File.new("Argon.hashes", "w")
out_file3 = File.new("pbkdf2.hashes", "w")
out_file4 = File.new("sha1.hashes", "w")

 
filename = ARGV[0]
puts "Going to open '#{filename}'"
 
fh = open filename
 
while (line = fh.gets) 
   
	if      line.include? "$6$"
		out_file1.puts(line)

	elsif  line.include? "$argon"
		out_file2.puts(line)

	elsif  line.include? "$pbkdf2"
		out_file3.puts(line)

	elsif  line.include? "$sha1$"
		out_file4.puts(line)

	
    end

end




fh.close


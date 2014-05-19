
puts "\n"
puts "\n"
puts "ruby gh_pages_copy.rb"
puts "====================="
puts "    Copying folders to parent directory"
folders = ['about',
           'assets',
           'blog',
           'images',
           'javascripts',
           'stylesheets']

for folder in folders do
    system('rm -rf ../'+folder)
    system('cp -r _deploy/'+folder+' ../'+folder)
end

puts "    Copying files to parent directory"
files = ['atom.xml',
         'favicon.ico',
         'favicon.png',
         'index.html',
         'robots.txt',
         'sitemap.xml']

for file in files do
    system('rm -f ../'+file)
    system('cp _deploy/'+file+' ../'+file)
end

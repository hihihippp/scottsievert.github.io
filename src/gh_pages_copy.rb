
puts "\n"
puts "\n"
puts "ruby gh_pages_copy.rb"
puts "====================="
puts "    Copying folders to parent directory"
folders = ['about',
           'software',
           'assets',
           'blog',
           'images',
           'javascripts',
           'stylesheets']

for folder in folders do
    system('rm -rf ../'+folder)
    system('cp -r public/'+folder+' ../'+folder)
end

puts "    Copying files to parent directory"
files = ['atom.xml',
         'favicon.png',
         'favicon-apple.png',
         'index.html',
         'robots.txt',
         'sitemap.xml']

for file in files do
    system('rm -f ../'+file)
    system('cp public/'+file+' ../'+file)
end

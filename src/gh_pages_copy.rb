
folders = ['about', 
          'assests', 
          'blog', 
          'images', 
          'javascripts', 
          'stylesheets'
         ]

for folder in folders do
    puts folder
    system('cp -r public/'+folder+' '+folder)
end

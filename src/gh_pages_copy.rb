
folders = ['about',
           'assests',
           'blog',
           'images',
           'javascripts',
           'stylesheets']

for folder in folders do
    system('cp -r public/'+folder+' ../'+folder)
end

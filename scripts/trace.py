import os, sys, shutil, subprocess
from PIL import Image

tracks_base_path = "./tracks"
potrace_exe = "./bin/potrace-1.16.win64/potrace.exe"

class Animal:
    def __init__(self, name):
        self.name = name
        self.directory = ''
        self.files = []

    def log(self, message):
        print('[{0}]  {1}'.format(self.name.upper(), message))
    
    def create_rgb_bmp(self, png_path, bmp_path):
        self.log('Creating RGB bitmap... {0}'.format(bmp_path))
        try:
            with Image.open(png_path) as im:
                width,height = im.size
                mode = im.mode

                if mode == 'RGBA':
                    r,g,b,a = im.split()

                    for x in range(width):
                        for y in range(height):
                            xy = (x,y)
                            pxa = a.getpixel(xy)

                            if pxa < 255:
                                r.putpixel(xy, 255 - pxa)
                                g.putpixel(xy, 255 - pxa)
                                b.putpixel(xy, 255 - pxa) 
                            
                    im = Image.merge(mode, (r,g,b,a))

                im.save(bmp_path)
        except OSError:
            print("cannot convert", png_path)
            raise   

    def create_outline(self, bmp_path, svg_path):
        self.log('Creating SVG outline... {0}'.format(svg_path))
        subprocess.run([potrace_exe, bmp_path, '--output', svg_path, '--svg', '--opaque'])

    def process(self):
        self.log('Beginning processing...')
        try:
            silhouette_names = [f for f in self.files if 'silhouette' in f and '.png' in f]
            
            for silhouette_name in silhouette_names:
                print(silhouette_name)
                png_path = os.path.join(self.directory, silhouette_name)
                bmp_path = png_path.replace('.png', '.bmp')
                svg_path = png_path.replace('silhouette', 'outline').replace('.png', '.svg')
                         
                if os.path.exists(svg_path):
                    continue

                self.create_rgb_bmp(png_path, bmp_path)                
                self.create_outline(bmp_path, svg_path)                

            self.log('Processing complete!')
        except Exception as e:
            self.log('Processing failed: {0}'.format(e))
            raise
    

def execute():
    animals = []

    if os.path.exists(potrace_exe):
        print('found')
    for animal_dir, _, animal_files in os.walk(tracks_base_path):
        animal_name = animal_dir.replace('./tracks', '').strip('\\').strip('/')

        if animal_name == '':
            continue

        animal = Animal(animal_name)
        animal.directory = animal_dir
        animal.files = animal_files

        animal.process()

execute()
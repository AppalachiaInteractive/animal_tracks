import os, sys, shutil, subprocess
from wand.image import Image
import numpy as np
import scipy.ndimage
import scipy.misc
import imageio

tracks_base_path = "./tracks"
bin_path = "./bin/"
potrace_exe = os.path.join(bin_path, "potrace-1.16.win64/potrace.exe")

hq_px_size = 1024
blur_strength = 32
hq_size = (hq_px_size, hq_px_size)
margin = hq_px_size/blur_strength
divisor = 96.0
blur_size = hq_px_size/(blur_strength+4)
blur_sigma = blur_size/2.0
normal_smooth = 0.0
normal_intensity = 1.0

image_key =            'silhouette'
outline_key =          'outline'
suffix_hq =            '_hq'
suffix_height =        '_height'
suffix_normal_dx =     '_normal-directx'
suffix_normal_opengl = '_normal-opengl'

def smooth_gaussian(im, sigma):
    if sigma == 0:
        return im

    im_smooth = im.astype(float)
    kernel_x = np.arange(-3*sigma,3*sigma+1).astype(float)
    kernel_x = np.exp((-(kernel_x**2))/(2*(sigma**2)))

    im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis])

    im_smooth = scipy.ndimage.convolve(im_smooth, kernel_x[np.newaxis].T)

    return im_smooth

def gradient(im_smooth):
    gradient_x = im_smooth.astype(float)
    gradient_y = im_smooth.astype(float)

    kernel = np.arange(-1,2).astype(float)
    kernel = - kernel / 2

    gradient_x = scipy.ndimage.convolve(gradient_x, kernel[np.newaxis])
    gradient_y = scipy.ndimage.convolve(gradient_y, kernel[np.newaxis].T)

    return gradient_x,gradient_y

def sobel(im_smooth):
    gradient_x = im_smooth.astype(float)
    gradient_y = im_smooth.astype(float)

    kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

    gradient_x = scipy.ndimage.convolve(gradient_x, kernel)
    gradient_y = scipy.ndimage.convolve(gradient_y, kernel.T)

    return gradient_x,gradient_y

def compute_normal_map(gradient_x, gradient_y, intensity=1):

    width = gradient_x.shape[1]
    height = gradient_x.shape[0]
    max_x = np.max(gradient_x)
    max_y = np.max(gradient_y)

    max_value = max_x

    if max_y > max_x:
        max_value = max_y

    normal_map = np.zeros((height, width, 3), dtype=np.float32)

    intensity = 1 / intensity

    strength = max_value / (max_value * intensity)

    normal_map[..., 0] = gradient_x / max_value
    normal_map[..., 1] = gradient_y / max_value
    normal_map[..., 2] = 1 / strength

    norm = np.sqrt(np.power(normal_map[..., 0], 2) + np.power(normal_map[..., 1], 2) + np.power(normal_map[..., 2], 2))
    
    normal_map[..., 0] /= norm
    normal_map[..., 1] /= norm
    normal_map[..., 2] /= norm

    normal_map *= 0.5
    normal_map += 0.5

    normal_map_opengl = normal_map.copy()
    normal_map_opengl[..., 1] = 1.0 - normal_map_opengl[..., 1]

    return normal_map, normal_map_opengl


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
            with Image(filename=png_path) as original:
                with original.convert('bmp') as bitmap:
                    for row in bitmap:
                        for color in row:                            
                            if color.alpha < 1.0:
                                color.red = 1.0 - color.alpha
                                color.green = 1.0 - color.alpha
                                color.blue = 1.0 - color.alpha 

                    width,height = bitmap.size

                    if width != height:
                        min_dimension = min(width, height)
                        max_dimension = max(width, height)
                        shift_x = 0 if min_dimension != width  else -int((max_dimension -  width) / 2)
                        shift_y = 0 if min_dimension != height else -int((max_dimension - height) / 2)
                        bitmap.extent(max_dimension, max_dimension, shift_x, shift_y)
                    bitmap.save(filename=bmp_path)                    
        except OSError:
            print("cannot convert", png_path)
            raise   

    def create_outline(self, bmp_path, svg_path):
        self.log('Creating SVG outline... {0}'.format(svg_path))
        size = hq_size

        m = margin / divisor
        width = size[0] / divisor
        height = size[1] / divisor
        width -= (2*m)
        height -= (2*m)
        
        subprocess.run([
            potrace_exe, 
            bmp_path, 
            '--output', 
            svg_path,
            '--svg', 
            '--opaque',
            '-W {0:.3f}'.format(width),
            '-H {0:.3f}'.format(height),
            '-M {0:.3f}'.format(m),
        ])

    def create_hq(self, svg_path, hq_path):
        self.log('Creating HQ render... {0}'.format(hq_path))
        with Image(filename=svg_path) as original:
            with original.convert('png') as converted:
                for row in converted:
                    for color in row:
                        color.alpha = 1.0 - ((color.red + color.green + color.blue)/3.0)
                converted.save(filename=hq_path)

    def create_height(self, hq_path, height_path):
        self.log('Creating height... {0}'.format(height_path))
        with Image(filename=hq_path) as image:
            for row in image:
                for color in row:
                    color.alpha = 1.0
            image.blur(radius=blur_size, sigma=blur_sigma)              
            image.save(filename=height_path)

    def create_normal(self, height_path, normal_dx_path, normal_opengl_path):
        self.log('Creating normal... {0}'.format(normal_dx_path))
          
        im = imageio.imread(height_path)

        if im.ndim == 3:
            im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
            im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
            im = im_grey

        im_smooth = smooth_gaussian(im, normal_smooth)

        sobel_x, sobel_y = sobel(im_smooth)

        normal_map_dx, normal_map_opengl = compute_normal_map(sobel_x, sobel_y, normal_intensity)

        imageio.imsave(normal_dx_path, normal_map_dx)
        imageio.imsave(normal_opengl_path, normal_map_opengl)


    def process(self):
        self.log('Beginning processing...')
        try:
            image_names = [f for f in self.files if (
                image_key in f and 
                '.png' in f and 
                not outline_key in f and
                not suffix_height in f and 
                not suffix_hq in f and 
                not suffix_normal_dx in f and                
                not suffix_normal_opengl in f
            )]
            
            for image_name in image_names:
                png_path = os.path.join(self.directory, image_name)
                bmp_path = png_path.replace('.png', '.bmp')
                svg_path = png_path.replace(image_key, outline_key).replace('.png', '.svg')
                generated_path = png_path.replace(image_key, '').replace('_.', '.')
                hq_path = generated_path.replace('.png', '{0}.png'.format(suffix_hq))
                height_path = generated_path.replace('.png', '{0}.png'.format(suffix_height))
                normal_dx_path = generated_path.replace('.png', '{0}.png'.format(suffix_normal_dx))
                normal_opengl_path = generated_path.replace('.png', '{0}.png'.format(suffix_normal_opengl))

                do_create_rgb_bmp = not os.path.exists(bmp_path)
                do_create_outline = do_create_rgb_bmp or not os.path.exists(svg_path)
                do_create_hq = do_create_outline or not os.path.exists(hq_path)
                do_create_height = do_create_hq or not os.path.exists(height_path)
                do_create_normal = do_create_height or not os.path.exists(normal_dx_path) or not os.path.exists(normal_opengl_path)

                if do_create_rgb_bmp:
                    self.create_rgb_bmp(png_path, bmp_path)
                if do_create_outline:
                    self.create_outline(bmp_path, svg_path)
                if do_create_hq:
                    self.create_hq(svg_path, hq_path)
                if do_create_height:
                    self.create_height(hq_path, height_path)
                if do_create_normal:
                    self.create_normal(height_path, normal_dx_path, normal_opengl_path)
                

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
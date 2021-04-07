import os, shutil

tracks_base_path = "./tracks"
animal_list_path = "./scripts/initial_animal_list.txt"
silhouette_template = "./references/tracks_transparency.png"

class Animal:
    def __init__(self, name):
        self.name = name
        self.directory = ''
        self.silhouette_path = ''
        self.svg_path = ''
        self.normal_path = ''
        self.displacement_path = ''

    def log(self, message):
        print('[{0}]  {1}'.format(self.name.upper(), message))
    
    def create_directory(self):
        self.log('Creating directory: {0}'.format(self.directory))

        try:
            os.mkdir(self.directory)
        except FileExistsError:
            pass

    def create_silhouette_template(self):
        self.silhouette_path = os.path.join(self.directory, '{0}_silhouette.png'.format(self.name))

        if os.path.exists(self.silhouette_path):
            return

        shutil.copy(silhouette_template, self.silhouette_path)


    def process(self):
        self.log('Beginning processing...')
        try:
            self.directory = os.path.join(tracks_base_path, self.name)
            self.create_directory()
            self.create_silhouette_template()        

            self.log('Processing complete!')
        except Exception as e:
            self.log('Processing failed: {0}'.format(e))
            raise
    

def execute():
    with open(animal_list_path, "r") as animal_list:
        animals = []

        for animal_line in animal_list:
            animal_name = animal_line.replace('\n','')

            animal = Animal(animal_name)

            animals.append(animal)
            animal.process()

        

execute()

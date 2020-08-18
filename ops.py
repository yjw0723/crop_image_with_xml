import os
import xml.etree.ElementTree as ET
from PIL import Image
import re
from tqdm import tqdm

class CropImg:
    def __init__(self, xml_folder, img_folder):
        self.xml_folder = xml_folder
        self.img_folder = img_folder
        self.save_folder = re.sub('img', 'crop', self.img_folder)
        os.makedirs(self.save_folder, exist_ok=True)
        self.xml_name_list = os.listdir(self.xml_folder)
        self.img_name_list = os.listdir(self.img_folder)
        self.img_app_num_list = [img_name.split('.')[0] for img_name in self.img_name_list]

    def get_box(self, xml_name):
        xml_path = os.path.join(self.xml_folder, xml_name)
        xml = ET.parse(xml_path)
        root = xml.getroot()
        app_num = xml_name.split('.')[0]
        i = 1
        for child in root:
            if child.tag == 'object':
                xmin, ymin, xmax, ymax = 0, 0, 0, 0
                idx = [i for i, v in enumerate(self.img_app_num_list) if app_num == v][0]
                original_filename = self.img_name_list[idx]
                save_app_num = f'{original_filename.split(".")[0]}_{i}'
                save_file_name = f'{save_app_num}.{original_filename.split(".")[1]}'
                i = i + 1
                for child_1 in child:
                    for child_2 in child_1:
                        if child_2.tag == 'xmin':
                            xmin = child_2.text
                        elif child_2.tag == 'ymin':
                            ymin = child_2.text
                        elif child_2.tag == 'xmax':
                            xmax = child_2.text
                        else:
                            ymax = child_2.text
                            return int(xmin), int(ymin), int(xmax), int(ymax), original_filename, save_file_name

    def crop_img(self, xmin, ymin, xmax, ymax, img_path, save_path):
        area = (xmin, ymin, xmax, ymax)
        img = Image.open(img_path)
        crop_img = img.crop(area)
        crop_img.save(save_path)

    def execute(self):
        for xml_name in tqdm(self.xml_name_list):
            xmin, ymin, xmax, ymax, original_filename, save_file_name = self.get_box(xml_name)
            img_path = os.path.join(self.img_folder, original_filename)
            save_path = os.path.join(self.save_folder, save_file_name)
            self.crop_img(xmin, ymin, xmax, ymax, img_path, save_path)






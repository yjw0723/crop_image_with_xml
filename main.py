from ops import CropImg

IMG_DIR = './data/img'
XML_DIR = './data/xml'

if __name__ == '__main__':
    crop_img = CropImg(XML_DIR, IMG_DIR)
    crop_img.execute()
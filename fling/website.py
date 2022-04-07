import os
import sys
import shutil
import datetime
import glob2

from PIL import Image
from chameleon import PageTemplateLoader

import markdown
import yaml

from fling import defs

class FlingernWebsite:
    def __init__(self, path):
        self.path = path
        site_conf = os.path.join(self.path, "site.yaml")

        with open(site_conf, 'r') as f:
            self.site = yaml.safe_load(f)

        self.site["year"] = datetime.datetime.today().year
        
        # figuring paths
        self.pub_dir = os.path.join(self.path, defs.DIR_PUBLIC)

        # setup pages
        pages = []
        for page in self.site['pages']:
            pages.append(self.setup_page(page))
        self.site["pages"] = pages

    def build(self):
        # create theme structure
        if not os.path.isdir(self.pub_dir):
            os.mkdir(self.pub_dir)

        theme_pub = os.path.join(self.pub_dir, "public/")
        if os.path.isdir(theme_pub):
            shutil.rmtree(theme_pub)
        
        shutil.copytree(
            os.path.join(defs.flingern_directory, defs.DIR_THEME_PUBLIC),
            theme_pub
        )

        # loading templates
        self.site_templates = PageTemplateLoader(os.path.join(defs.flingern_directory, defs.DIR_THEME))
        self.site_page_template = self.site_templates["page.html"]

        # generate pages
        for page in self.site["pages"]:
            self.build_page(page)
            
    def setup_page(self, page_file):
        page_path = os.path.join(self.path, page_file)
        with open(page_path, 'r') as f:
            page_content = f.read()

        content = page_content.split("---MD---")
        
        page = yaml.safe_load(content[0])

        page_name = os.path.basename(page_file).split(".")[0]
        url = page_name + ".html"

        if not "menu" in page:
            page["menu"] = page["title"]

        page["name"] = page_name
        page["url"] = url
        page["content"] = markdown.markdown(content[1], extensions=['tables'])
            

        return page

    def setup_images(self, page):
        images = []

        if "images" in page:
            if len(page["images"]) == 0 or not isinstance(page["images"][0], str): return

            for img in page["images"]:
                imgs = glob2.glob(os.path.join(self.path, img))
                for i in imgs:
                    images.append(self.setup_image(page, i))

        page["images"] = images

    def setup_image(self, page, original_image_path):
        image_name = os.path.basename(original_image_path).split(".")[0]
        image_file = os.path.join(page["images_path"], image_name) + ".jpg"
        image_thumb_file = os.path.join(page["images_path"], image_name) + "_thumb.jpg"

        with Image.open(original_image_path) as im:
            ratio = im.size[0] / im.size[1]
            
            # image
            if not os.path.isfile(image_file):
                dimensions = (int(self.site["images_max_height"] * ratio), self.site["images_max_height"])
                nim = im.resize(dimensions)
                nim.save(image_file, "JPEG", optimize=True, quality=self.site["images_quality"])

            # thumb
            if not os.path.isfile(image_thumb_file):
                dimensions = (int(self.site["thumbs_max_height"] * ratio), self.site["thumbs_max_height"])
                nim = im.resize(dimensions)
                nim.save(image_thumb_file, "JPEG", optimize=True, quality=self.site["thumbs_quality"])

        info = {
            "path": os.path.join(page["name"], image_name) + ".jpg",
            "thumb": os.path.join(page["name"], image_name) + "_thumb.jpg"
        }

        return info


    def build_page(self, page):
        print("Building page %s" % page["url"])

        images_path = os.path.join(self.pub_dir, page["name"])
        if not os.path.isdir(images_path):
            os.mkdir(images_path)

        page["images_path"] = images_path

        # setup images
        self.setup_images(page)

        result = self.site_page_template(site=self.site, page=page)
        
        result_file_path = os.path.join(self.pub_dir, page["url"])
        if os.path.isfile(result_file_path):  os.remove(result_file_path)
        with open(result_file_path, 'x') as f:
            f.write(result)
            


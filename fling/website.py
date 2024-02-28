import os
import sys
import shutil
import datetime
import glob2

from PIL import Image, ImageOps
from chameleon import PageTemplateLoader

import markdown
import yaml

from fling import defs
from fling import util

class FlingernWebsite:
    def __init__(self, path, force):
        self.path = path
        site_conf = os.path.join(self.path, "site.yaml")

        with open(site_conf, 'r') as f:
            self.site = yaml.safe_load(f)

        self.site["year"] = datetime.datetime.today().year
        
        # figuring paths
        self.pub_dir = os.path.realpath(os.path.join(self.path, defs.DIR_PUBLIC))
        if not os.path.isdir(self.pub_dir):
            os.mkdir(self.pub_dir)
            
        if force:
            print("Force parameter passed, so deleting the whole site before\n")
            for root, dirs, files in os.walk(self.pub_dir):
                for f in files: os.unlink(os.path.join(root, f))
                for d in dirs: shutil.rmtree(os.path.join(root, d))

        # setup pages
        pages = []
        for page in self.site['pages']:
            pages.append(self.setup_page(page))
        self.site["pages"] = pages

    def build(self):
        # create theme structure
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
        page_path = os.path.join(self.path, defs.DIR_CONTENT, page_file)
        with open(page_path, 'r') as f:
            page_content = f.read()

        content = page_content.split("---")

        page = yaml.safe_load(content[1])

        page_name = os.path.basename(page_file).split(".")[0]

        if not "menu" in page:
            page["menu"] = page["title"]

        page_content = "---".join(content[2:])
        
        content_path = os.path.abspath(os.path.join(self.path, defs.DIR_CONTENT))
        content_path = util.path_relative_from(
            os.path.dirname(os.path.realpath(page_path)),
            content_path)

        page["name"] = page_name
        page["content_path"] = content_path
        page["url"] = os.path.join(page["content_path"], page["name"] + ".html")
        page["content"] = markdown.markdown(page_content, extensions=['tables'])
        
        return page

    def setup_images(self, page):
        images = []

        if "images" in page:
            if len(page["images"]) == 0 or not isinstance(page["images"][0], str): return

            for img in page["images"]:
                imgs = glob2.glob(os.path.join(self.path, defs.DIR_CONTENT, page["content_path"], img))
                for i in imgs:
                    images.append(self.setup_image(page, i))

        page["images"] = images

    def setup_image(self, page, original_image_path):

        image_name = util.path_relative_from(original_image_path, os.path.join(self.path, defs.DIR_CONTENT)).split(".")[0]
        image_path = os.path.join(self.pub_dir, os.path.dirname(image_name))
        image_file = os.path.join(self.pub_dir, image_name) + ".jpg"
        image_thumb_file = os.path.join(self.pub_dir, image_name) + "_thumb.jpg"
        
        if not os.path.isdir(image_path):
            os.mkdir(image_path)

        with Image.open(original_image_path) as im:
            ratio = im.size[0] / im.size[1]
            
            # image
            if not os.path.isfile(image_file):
                dimensions = (int(self.site["images_max_height"] * ratio), self.site["images_max_height"])
                nim = im.resize(dimensions)
                if "images_border" in self.site:
                    nim = ImageOps.expand(nim, border=self.site["images_border"],fill='white')
                nim.save(image_file, "JPEG", optimize=True, quality=self.site["images_quality"])

            # thumb
            if not os.path.isfile(image_thumb_file):
                dimensions = (self.site["thumbs_max_width"], int(self.site["thumbs_max_width"] / ratio))
                nim = im.resize(dimensions)
                if "thumbs_border" in self.site:
                    nim = ImageOps.expand(nim, border=self.site["thumbs_border"],fill='white')
                nim.save(image_thumb_file, "JPEG", optimize=True, quality=self.site["thumbs_quality"])

        info = {
            "path": image_name + ".jpg",
            "thumb": image_name + "_thumb.jpg"
        }

        return info


    def build_page(self, page):
        print("Building page %s" % page["url"])

        page_path = os.path.join(self.pub_dir, page["content_path"])
        if not os.path.isdir(page_path):
            os.mkdir(page_path)

        # setup images
        self.setup_images(page)

        result = self.site_page_template(site=self.site, page=page)
        
        result_file_path = os.path.join(self.pub_dir, page["url"])
        if os.path.isfile(result_file_path):  os.remove(result_file_path)
        with open(result_file_path, 'x') as f:
            f.write(result)
            


import os
import sys
import shutil
import datetime

import yaml
from chameleon import PageTemplateLoader

from fling import defs

class FlingernWebsite:
    def __init__(self, path):
        self.path = path
        site_conf = os.path.join(self.path, "site.yaml")

        with open(site_conf, 'r') as f:
            self.site = yaml.safe_load(f)

        self.site["year"] = datetime.datetime.today().year

    def build(self):
        # figurate paths
        self.pub_dir = os.path.join(".", self.path, defs.DIR_PUBLIC)

        # setup pages
        pages = []
        for page in self.site['pages']:
            pages.append(self.setup_page(page))
        self.site["pages"] = pages

        # copy theme structure
        if not os.path.isdir(self.pub_dir):
            shutil.copytree(
                os.path.join(".", defs.DIR_THEME),
                self.pub_dir
            )

        # loading templates
        self.site_templates = PageTemplateLoader(os.path.join(".", defs.DIR_THEME))
        self.site_page_template = self.site_templates["page.html"]

        # generate pages
        for page in self.site["pages"]:
            self.build_page(page)
            
    def setup_page(self, page_file):
        page_path = os.path.join('.', self.path, page_file)
        with open(page_path, 'r') as f:
            page_content = f.read()

        content = page_content.split("---")
        
        page = yaml.safe_load(content[0])

        url = os.path.basename(page_file).split(".")[0] + ".html"

        page["url"] = url
        page["content"] = content[1]

        return page

    def build_page(self, page):
        print("Building page %s" % page["title"])

        result = self.site_page_template(site=self.site, page=page)
        
        result_file_path = os.path.join(self.pub_dir, page["url"])
        if os.path.isfile(result_file_path):  os.remove(result_file_path)
        with open(result_file_path, 'x') as f:
            f.write(result)


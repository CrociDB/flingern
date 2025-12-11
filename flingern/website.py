import datetime
import shutil
from pathlib import Path
from typing import Any, Dict

import markdown
import yaml
from chameleon import PageTemplateLoader

from flingern import defs
from flingern.images import ImageProcessor


class FlingernWebsite:
    def __init__(self, path: Path, force: bool) -> None:
        self.path = path
        site_conf = self.path / "site.yaml"

        with site_conf.open("r") as f:
            self.site: Dict[str, Any] = yaml.safe_load(f)

        self.site["year"] = datetime.datetime.today().year

        # figuring paths
        self.pub_dir = (self.path / defs.DIR_PUBLIC).resolve()
        if not self.pub_dir.is_dir():
            self.pub_dir.mkdir()

        if force:
            print("Force parameter passed, so deleting the whole site before\n")
            for item in self.pub_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)

        self.image_processor = ImageProcessor(
            content_root=self.path / defs.DIR_CONTENT, public_dir=self.pub_dir, config=self.site
        )

        # setup pages
        for section in self.site["sections"]:
            for i, page in enumerate(section["pages"]):
                section["pages"][i] = self.setup_page(page)

    def build(self) -> None:
        # create theme structure
        theme_pub = self.pub_dir / "public"
        if theme_pub.is_dir():
            shutil.rmtree(theme_pub)

        shutil.copytree(Path(defs.flingern_directory) / defs.DIR_THEME_PUBLIC, theme_pub)

        # loading templates
        self.site_templates = PageTemplateLoader(str(Path(defs.flingern_directory) / defs.DIR_THEME))
        self.site_page_template = self.site_templates["page.html"]

        # generate pages
        for section in self.site["sections"]:
            for page in section["pages"]:
                self.build_page(page)

    def setup_page(self, page_file: str) -> Dict[str, Any]:
        page_path = self.path / defs.DIR_CONTENT / page_file
        page_content = page_path.read_text()

        content = page_content.split("---")

        page: Dict[str, Any] = yaml.safe_load(content[1])

        page_name = page_path.stem

        if not "menu" in page:
            page["menu"] = page["title"]

        page_content_md = "---".join(content[2:])

        content_path_root = (self.path / defs.DIR_CONTENT).resolve()
        content_path = page_path.parent.resolve().relative_to(content_path_root)

        page["name"] = page_name
        page["content_path"] = str(content_path)
        page["url"] = str(content_path / (page["name"] + ".html"))
        page["content"] = markdown.markdown(page_content_md, extensions=["tables"])

        return page

    def build_page(self, page: Dict[str, Any]) -> None:
        print("Building page %s" % page["url"])

        page_path = self.pub_dir / page["content_path"]
        if not page_path.is_dir():
            page_path.mkdir(parents=True, exist_ok=True)

        # setup images
        self.image_processor.process_page_images(page)

        result = self.site_page_template(site=self.site, page=page)

        result_file_path = self.pub_dir / page["url"]
        if result_file_path.is_file():
            result_file_path.unlink()

        # Write content
        result_file_path.write_text(result)

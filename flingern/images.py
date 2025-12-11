from pathlib import Path
from typing import Dict, Any, List, Optional
from PIL import Image, ImageOps

class ImageProcessor:
    def __init__(self, content_root: Path, public_dir: Path, config: Dict[str, Any]):
        self.content_root = content_root
        self.public_dir = public_dir
        self.config = config

    def process_page_images(self, page: Dict[str, Any]) -> None:
        images: List[Dict[str, str]] = []

        if "images" in page:
            if len(page["images"]) == 0 or not isinstance(page["images"][0], str): return

            for img_pattern in page["images"]:
                base_dir = self.content_root / page["content_path"]
                if base_dir.exists():
                    imgs = list(base_dir.glob(img_pattern))
                    for i in imgs:
                        result = self.process_image(i)
                        if result:
                            images.append(result)

        page["images"] = images

    def process_image(self, original_image_path: Path) -> Optional[Dict[str, str]]:
        try:
            rel_path = original_image_path.relative_to(self.content_root)
        except ValueError:
            return None
        
        image_rel_no_ext = rel_path.with_suffix('')
        
        image_path = self.public_dir / image_rel_no_ext.parent
        image_file = (self.public_dir / image_rel_no_ext).with_suffix(".jpg")
        image_thumb_file = self.public_dir / (str(image_rel_no_ext) + "_thumb.jpg")
        
        if not image_path.is_dir():
            image_path.mkdir(parents=True, exist_ok=True)

        with Image.open(original_image_path) as im:
            ratio = im.size[0] / im.size[1]
            
            # image
            if not image_file.is_file():
                dimensions = (int(self.config.get("images_max_height", 800) * ratio), self.config.get("images_max_height", 800))
                nim = im.resize(dimensions)
                if "images_border" in self.config:
                    nim = ImageOps.expand(nim, border=self.config["images_border"], fill='white')
                nim.save(image_file, "JPEG", optimize=True, quality=self.config.get("images_quality", 85))

            # thumb
            if not image_thumb_file.is_file():
                dimensions = (self.config.get("thumbs_max_width", 300), int(self.config.get("thumbs_max_width", 300) / ratio))
                nim = im.resize(dimensions)
                if "thumbs_border" in self.config:
                    nim = ImageOps.expand(nim, border=self.config["thumbs_border"], fill='white')
                nim.save(image_thumb_file, "JPEG", optimize=True, quality=self.config.get("thumbs_quality", 85))

        info = {
            "path": str(image_file.relative_to(self.public_dir)),
            "thumb": str(image_thumb_file.relative_to(self.public_dir))
        }

        return info

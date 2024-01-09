let setupGallery = function(galleryId, galleryDesktopId, galleryMobileId)
{
    let images = [];
    let gallery = document.getElementById(galleryId);
    let galleryDesktop = document.getElementById(galleryDesktopId);
    let galleryMobile = document.getElementById(galleryMobileId);

    for (const img of gallery.children)
    {
        images.push(img);
    }

    
    let createGallery = function(element, images)
    {
        let columns = element.children[0].children;
        let images_column = Math.ceil(images.length / columns.length);
        console.dir(images_column);
        while (images.length > 0)
        {
            for (let i = 0; i < columns.length; i++)
            {
                let img = images.pop();
                if (img)
                    columns[i].appendChild(img.cloneNode(true));
            }
        }
    }

    let reorder = function()
    {
        if (window.innerWidth >= 1200)
        {
            galleryMobile.classList.add('d-none');
            galleryDesktop.classList.remove('d-none');
        }
        else
        {
            galleryMobile.classList.remove('d-none');
            galleryDesktop.classList.add('d-none');
        }
    }

    createGallery(galleryMobile, images.map((x) => x));
    createGallery(galleryDesktop, images.map((x) => x));
    reorder();
    addEventListener("resize", (event) => reorder());
}
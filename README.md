```
  d888 888 d8b                                             
d88P"  888 Y8P                                             
888    888                                                 
888888 888 888 88888b.   .d88b.   .d88b.  888d888 88888b.  
888    888 888 888 "88b d88P"88b d8P  Y8b 888P"   888 "88b 
888    888 888 888  888 888  888 88888888 888     888  888 
888    888 888 888  888 Y88b 888 Y8b.     888     888  888 
888    888 888 888  888  "Y88888  "Y8888  888     888  888 
                             888                                
                            d88P
                          Y88P"
```

**flingern** is a static art website generator. Example: [Bruno Croci's Art](https://bruno.croci.art/).

# Features

 - [x] Easy to use: write your whole website in Markdown with minimal config in TOML
 - [x] Fire up the monitor and it will serve the website and automatically rebuild it on any change
 - [x] Generates the website with an elegant theme
 - [ ] Theme flexibility: customize the theme as you wish
 - [x] Automatic image conversion: converts photos into thumbnails and lower quality versions to save bandwidth

# Getting Started

Install it through PIP (still not available):

```shell
pip install flingern
```

The build your website with:

```shell
flingern website/
```

## Site Building Monitor

**flingern** has a monitor that will automatically rebuild the site on any change and serve the build website. All you have to do is:

```shell
flingern --watch .
```

# Development

In order to setup the development environment, you might need some system-wide dependencies such as `libjpeg-dev` and `zlib1g-dev`. Example installing it with a Debian-based distro:

```shell
sudo apt install libjpeg-dev zlib1g-dev
```

Then sync dependencies and run with **uv**:

```shell
uv sync
uv run main.py
```
# Why 'flingern'?

Flingern is a nice neighborhood in Düsseldorf where I usually take walks and have coffee.

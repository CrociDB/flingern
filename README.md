<p align="center">
  <img src="img/flingern.png" alt="flingern" />
</p>
<p align="center">flingern is a static art website generator</p>

Example: [Bruno Croci's Art](https://bruno.croci.art/).

# Features

 - [x] Easy to use: write your whole website in Markdown with minimal config in YAML
 - [x] Fire up the monitor and it will serve the website and automatically rebuild it on any change
 - [x] Generates the website with an elegant theme
 - [x] Automatic image conversion: converts photos into thumbnails and lower quality versions to save bandwidth
 - [ ] Theme flexibility: customize the theme as you wish

# Getting Started

Install it through PIP (still not available):

```shell
pip install flingern
```

Create a new site with:

```shell
flingern new my-site
```

The build your:

```shell
flingern build my-site
```

You can also serve it, and enable the watchdog to rebuild on any change:

```shell
flingern serve my-site --watch
```

# Development

*flingern* uses `nix-shell` to build a reliable development shell:

```shell
nix-shell
```

Then sync dependencies and run with **uv**:

```shell
uv sync
uv run main.py
```
# Why 'flingern'?

Flingern is a nice neighborhood in Düsseldorf where I usually take walks and have coffee.

---
title: "Getting Started"
menu: "Getting Started"
---

## Installing

Through **pip**:

```
pip install flingern
```

## Creating a new site

```
flingern new helloworld
```

The structure should be:

```
helloworld:
    | site.yaml
    | content
        | index.md
```

## Building site

Once your within the site root:

```
flingern .
```

## Serving for development

```
flingern -w .
```

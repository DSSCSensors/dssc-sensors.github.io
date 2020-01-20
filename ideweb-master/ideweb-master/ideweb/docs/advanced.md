# Advanced

This section outlines a few advanced options for using ImageDataExtractor.

## Large-scale Extraction

ImageDataExtractor can be used for high-throughput data extraction using two methods:

    >>> ide.extract_images('<path/to/img/dir>')
    >>> ide.extract_documents('<path/to/docs/dir>')  
    
These run the `extract_image` and `extract_document` methods sequentially on every file in the target directory.

ImageDataExtractor also supports `.zip`, `.tar` and `.tar.gz` inputs.

## Output locations

In addition to the output graphs, images are in the following locations for transparency:

- `raw_images` : Contains the images that were downloaded from the article 
- `split_photo_images` : Individual images after the first splitting algorithm (whitespace)
- `spit_grid_images` : Individual images after the second splitting algorithm (integer fractions of the grid)

CSV's containing metadata are also outputted to:

- `_raw` : Contains metadata of the extracted image, including figure caption
- `_csv` : Contains metadata of split images.

    
To specify an output directory add this as the second argument to any function. For example:

    >>> ide.extract_image('<path/to/image/file>', '<path/to/output>')

wll save all outputs to `<path/to/output>`

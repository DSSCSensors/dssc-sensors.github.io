# Installation

This section outlines the steps required to install ImageDataExtractor. 

We **strongly** advise the use of a **virtual environment** when installing ImageDataExtractor (Click [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to learn how.)

## Step 1: Install Tesseract 3

ImageDataExtractor currently uses **Tesseract 3** for text recognition. You can check your existing version by running:

    $ tesseract -v

The source code for the correct installation can be downloaded [here](https://github.com/tesseract-ocr/tesseract/tree/3.05) if required.
Instructions for compiling on your machine can be found [here](https://github.com/tesseract-ocr/tesseract/wiki/Compiling).

## Step 2: Install ImageDataExtractor

Installation with `pip` is the simplest option for getting going with ImageDataExtractor.
 
Simply run:

    pip install ImageDataExtractor
    
Then download the necessary data files to run ChemDataExtractor-IDE by running:

    cde data download

and you're ready to go!

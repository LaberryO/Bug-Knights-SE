import os;

def imageLoader(fileName):
    return os.path.join("Resource", "Image", fileName);

def fontLoader(fontName):
    return os.path.join("Resource", "Font", fontName);
import os;

def ImageLoader(fileName):
    return os.path.join("Resource", "Image", fileName);

def FontLoader(fontName):
    return os.path.join("Resource", "Font", fontName);
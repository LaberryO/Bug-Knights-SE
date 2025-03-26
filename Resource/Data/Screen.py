class Screen:
    _instance = None;

    def __new__(cls, width = 540, height = 960):
        if cls._instance is None:
            cls._instance = super().__new__(cls);
            cls._instance.width = width
            cls._instance.height = height
        return cls._instance;
    def getSize(self):
        return self.getWidth(), self.getHeight();
    def getWidth(self):
        return self.width;
    def getHeight(self):
        return self.height;
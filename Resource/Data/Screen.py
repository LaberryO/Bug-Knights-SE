# Screen 은 싱글톤으로 생성해서 관리
# 어차피 변동될 일이 딱히 없어서 이렇게 함.

class Screen:
    _instance = None;

    def __new__(cls, width = 540, height = 960):
        if cls._instance is None:
            cls._instance = super().__new__(cls);
            cls._instance.width = width
            cls._instance.height = height
        return cls._instance;

    # Getter
    def getWidth(self):
        return self.width;

    def getHeight(self):
        return self.height;

    def getSize(self):
        return self.getWidth(), self.getHeight();

    # Setter
    def setWidth(self, width):
        self.width = width;
    
    def setHeight(self, height):
        self.height = height;

    def setSize(self, width, height):
        self.setWidth(width);
        self.setHeight(height);
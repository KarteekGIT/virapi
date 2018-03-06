class SetDefaults(object):
    def __init__(self):
        self.fileWriter("buttons/next")
        self.fileWriter("buttons/play")
        self.fileWriter("buttons/previous")
        self.fileWriter("buttons/sensor")
        self.fileWriter("buttons/start")
        self.fileWriter("buttons/stop")
        
    def fileReader(self, path):
        fileRead = open(path, "r+")
        content = fileRead.read(5)
        content = content.strip("\n")
        return content
        
    def fileWriter(self, path):
        writeFile = open(path, "w")
        writeFile.seek(0)
        writeFile.write("False")
        writeFile.truncate()
        writeFile.close()

    def fileTrue(self, path):
        writeFile = open(path, "w")
        writeFile.seek(0)
        writeFile.write("True")
        writeFile.truncate()
        writeFile.close()

class SetDefaults(object):
    def __init__(self):
        nextFile = open("buttons/next", "w")
        playFile = open("buttons/play", "w")
        prevFile = open("buttons/previous", "w")
        sensFile = open("buttons/sensor", "w")
        startFile = open("buttons/start", "w")
        stopFile = open("buttons/stop", "w")
        
        nextFile.seek(0)
        nextFile.write("False")
        nextFile.truncate()
        nextFile.close()

        playFile.seek(0)
        playFile.write("False")
        playFile.truncate()
        playFile.close()
        
        prevFile.seek(0)
        prevFile.write("False")
        prevFile.truncate()
        prevFile.close()
        
        sensFile.seek(0)
        sensFile.write("False")
        sensFile.truncate()
        sensFile.close()
        
        startFile.seek(0)
        startFile.write("False")
        startFile.truncate()
        startFile.close()
        
        stopFile.seek(0)
        stopFile.write("False")
        stopFile.truncate()
        stopFile.close()
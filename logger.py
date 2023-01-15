import storage

class Logger:
    def __init__(self, filename):
        self.readonly = True
        try:
            storage.remount("/", False)
            self.f = open("/log.txt", 'a')
            self.readonly = False
        except:
            pass

    def log(self, *s):
        if self.readonly:
            print(*s)
        else:
            s = " ".join([str(x) for x in s])
            self.f.write(s)

    def close(self):
        if not self.readonly:
            self.f.close()
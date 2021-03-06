from modules import BaseModule
import re

class VideoIdConverter(BaseModule):
    videoUrl = "https://www.bilibili.com/video/%s"
    patternAv = r"av[0-9]+"
    patternBv = r"BV[0-9,A-Z,a-z]+"
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = dict(("fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"[i], i) for i in range(58))
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    @classmethod
    def bv2av(cls, x):
        r = 0
        for i in range(6):
            r += cls.tr[x[cls.s[i]]] * 58 ** i
        return (r - cls.add) ^ cls.xor

    @classmethod
    def av2bv(cls, x):
        x = (int(x) ^ cls.xor) + cls.add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[cls.s[i]] = cls.table[x // 58 ** i % 58]
        return ''.join(r)

    @classmethod
    def urlConvert(cls, url):
        if re.search(cls.patternBv, url):
            return cls.videoUrl % ("av%s" % cls.bv2av(re.search(cls.patternBv, url).group()))
        if re.search(cls.patternAv, url):
            return cls.videoUrl % cls.av2bv(int(re.search(cls.patternAv, url).group()[2::]))
        return ""

    def getMethod(self):
        return {"convert":"convert between bv and av"}


    def process(self, args):
        for url in [s for s in args.split(" ")[1:] if s != ""]:
            urla = self.urlConvert(url)
            if urla == "":
                self.info("%s is not a proper video id" % url)
                continue
            self.info("%s -> %s" % (url, urla))


module = VideoIdConverter
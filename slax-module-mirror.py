import re
import logging
import os
import errno
import threading
from bs4 import BeautifulSoup as bs
from urllib2 import urlopen,urlparse,Request

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
   

class FlowException(Exception):
    pass

class ModuleEntry(threading.Thread):

    name = None
    x86 = None
    x86_64 = None
    desc = None
    req = None
    size = None
    path = None

    def __init__(self, parent, tr, primary_url):
        threading.Thread.__init__(self)
        self.tr = tr
        self.primary_url = primary_url
        self.parent = parent

    def run(self):
        tds = self.tr.find_all('td')
        logger.debug('tds: %s' % str(tds))
        if not tds: raise FlowException()
        self.name = tds[0].a.get_text()
        self.x86 = self.primary_url+tds[2].div.a.get('href')
        self.x86_64 = self.primary_url+tds[2].div.a.get('href')
        self.desc = tds[3].get_text()
        self.req = tds[4].get_text()
        self.size = tds[5].get_text()
        self.path = os.path.join(self.parent.name,self.name)
        if not self.parent.parent.make_duplicate_placeholder(self):
            self.download_all()

    def download_all(self):
        self.download(self.x86, arch='x86')
        self.download(self.x86_64, arch='x86_64')

    def download(self, url, arch):
        logger.info('downloading: %s' % url)
        if not url: raise FlowException()
        u = urlopen(url)
        if u.getcode() != 200: raise FlowException()
        arch_path = os.path.join(self.path, arch)
        mkdir_p(arch_path)
        f = open(os.path.join(arch_path, url.split('/')[-1]), 'w')
        f.write(u.read())
        f.close()

    def __dict__(self):
        return {'name':self.name, 'x86':self.x86, 'x86_64':self.x86_64, 'desc':self.desc, 'req':self.req, 'size':self.size}

    def __str__(self):
        return str(self.__dict__)

class CategoryEntry:

    def __init__(self, parent, div, primary_url):
        logger.debug('%s; %s' % (str(primary_url), str(div)))
        self.parent = parent
        self.mods = []
        cat_a = div.find('a', href=re.compile('\?category=.*'))
        logger.debug(('category.cat_a: %s' % cat_a))
        self.name = cat_a.get_text()
        self.url = cat_a.get('href')
        mkdir_p(self.name)
        cat_soup = bs(urlopen(primary_url+self.url))
        for row in cat_soup.find('table').find_all('tr'):
            try:
                urlobj = urlparse.urlsplit(primary_url)
                mod = ModuleEntry(self, row, '%s://%s' % (urlobj.scheme, urlobj.netloc))
                mod.start()
                logger.debug('category.mod: %s' % str(mod))
                self.mods.append(mod)
            except FlowException:
                pass

    def __dict__(self):
        return {'name':self.name, 'url':self.url, 'mods':[str(x) for x in self.mods]}

    def __str__(self):
        return str(self.__dict__)

class Page:

    def __init__(self):
        self.primary_url = 'https://www.slax.org/en/modules.php'
        self.categories = []
        self.mods = {}
        soup = bs(urlopen(self.primary_url))
        for cat_div in soup.find_all('div',class_=re.compile('category')):
            logger.debug('page.div: %s' % str(cat_div))
            if cat_div:
                try:
                    cat = CategoryEntry(self, cat_div, self.primary_url)
                    self.mods.update(dict([(x.name, cat.name) for x in cat.mods if x.name]))
                    logger.debug('page.cat: %s' % str(cat))
                    self.categories.append(cat)
                except FlowException:
                    pass

    def has(self, mod_name):
        if mod_name in self.mods:
            return True
        return False

    def make_duplicate_placeholder(self, mod):
        if not self.has(mod.name): return False
        mkdir_p(mod.path)
        def touch_mod(mod, arch, url):
            mkdir_p(os.path.join(mod.path, arch))
            f = open(os.path.join(mod.path, arch, url.split('/')[-1]), 'w')
            f.write('see: %s' % os.path.join(self.mods[mod.name], arch, url.split('/')[-1]))
            f.close()
        touch_mod(mod, 'x86', mod.x86)
        touch_mod(mod, 'x86_64', mod.x86_64)
        return True



    def __str__(self):
        return str([str(x) for x in self.categories])

p = Page()
print(p)

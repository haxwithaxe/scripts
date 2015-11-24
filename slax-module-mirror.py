import errno
import logging
import os
import re
import threading
from urllib2 import urlopen, urlparse, Request

from bs4 import BeautifulSoup as bs


LOGGER_NAME = 'slax-module-mirror'
ARCH_X86 = 'x86'
ARCH_X86_64 = 'x86_64'
SLAX_MODULES_URL = 'https://www.slax.org/en/modules.php'

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
   

class FlowException(Exception):
    pass


class ModuleEntry(threading.Thread):

    def __init__(self, parent, tr, primary_url):
        super().__init__()
        self.logger = logging.getLogger(LOGGER_NAME)
        self.tr = tr
        self.primary_url = primary_url
        self.parent = parent

    def get_abspath(self, relpath):
        return self.primary_url + relpath

    def run(self):
        self._nodes = self.tr.find_all('td')
        self.logger.debug('tds: %s', tds)
        if not self.nodes:
            raise FlowException()
        if not self.parent.parent.make_duplicate_placeholder(self):
            self.download_all()

    @property
    def name(self):
        return self.nodes[0].a.get_text()

    @property
    def x86(self):
        return self.primary_url + tds[2].div.a.get('href')

    @property
    def x86_64(self):
        return self.primary_url + self.nodes[2].div.a.get('href')

    @property
    def desc(self):
        return self.nodes[3].get_text()
    
    @property
    def req(self):
        return tds[4].get_text()

    @property
    def size(self):
        return self.nodes[5].get_text()

    @property
    def path(self):
        return os.path.join(self.parent.name, self.name)


    def download_all(self):
        self.download(self.x86, arch=ARCH_X86)
        self.download(self.x86_64, arch=ARCH_X86_64)

    def download(self, url, arch):
        self.logger.info('downloading: %s', url)
        if not url:
            raise FlowException()
        u = urlopen(url)
        if u.getcode() != 200:
            raise FlowException()
        arch_path = os.path.join(self.path, arch)
        mkdir_p(arch_path)
        with open(os.path.join(arch_path, url.split('/')[-1]), 'w') as f:
            f.write(u.read())

    def __dict__(self):
        return {'name':self.name, 'x86':self.x86, 'x86_64':self.x86_64, 'desc':self.desc, 'req':self.req, 'size':self.size}

    def __str__(self):
        return str(self.__dict__)


class CategoryEntry:

    def __init__(self, parent, div, primary_url):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.logger.debug('%s; %s', primary_url, div)
        self.parent = parent
        self.mods = []
        cat_a = div.find('a', href=re.compile('\?category=.*'))
        self.logger.debug('category.cat_a: %s', cat_a)
        self.name = cat_a.get_text()
        self.url = cat_a.get('href')
        self.download_modules()

    def download_modules(self):
        mkdir_p(self.name)
        primary_urlobj = urlparse.urlsplit(primary_url)
        full_category_url = primary_url + self.url
        cat_soup = bs(urlopen(full_category_url))
        for row in cat_soup.find('table').find_all('tr'):
            try:
                mod = ModuleEntry(self, row, '%s://%s' % (primary_urlobj.scheme, primary_urlobj.netloc))
                mod.start()
                self.logger.debug('category.mod: %s', mod)
                self.mods.append(mod)
            except FlowException:
                pass

    def __dict__(self):
        return {'name':self.name, 'url':self.url, 'mods':[str(x) for x in self.mods]}

    def __str__(self):
        return str(self.__dict__)


class Page:

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.primary_url = SLAX_MODULES_URL
        self.categories = []
        self.mods = {}
        self.download_categories()

    def download_categories(self):
        soup = bs(urlopen(self.primary_url))
        for cat_div in soup.find_all('div',class_=re.compile('category')):
            self.logger.debug('page.div: %s', cat_div)
            if cat_div:
                try:
                    cat = CategoryEntry(self, cat_div, self.primary_url)
                    self.mods.update(dict([(x.name, cat.name) for x in cat.mods if x.name]))
                    logger.debug('page.cat: %s', cat)
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
        touch_mod(mod, ARCH_X86, mod.x86)
        touch_mod(mod, ARCH_X86_64, mod.x86_64)
        return True

    def __str__(self):
        return str([str(x) for x in self.categories])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(LOGGER_NAME)
    p = Page()
    print(p)

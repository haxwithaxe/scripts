
import string
import subprocess

domain_chars = string.ascii_lowercase+string.digits+'_-'

tlds = ['com','co','xxx','asia','biz','mobi','tv','tel','org','net','info','us','ca','cc','bz','me','ch','de','hn']
tlds_short = ['co','tv','us','ca','cc','bz','me','ch','de','hn']

class Domain:

    def __init__(self, domain, tld):
        self.domain = domain
        self.tld = tld

    def __eq__(self, other):
        return self.domain == other.domain and self.tld == other.tld


class TLD:

    def __init__(self, value, domain_length=0):
        self.value = value
        self.domain_length = domain_length
        self.domains = []

    def __contains__(self, domain):
        return domain in self.domains

    def free(self, domain):
        print('whois %(domain)s.%(tld)s' % {'domain':domain,'tld':self.value})
        whois = subprocess.check_output('whois %(domain)s.%(tld)s' % {'domain':domain,'tld':self.value}, shell=True)
        if whois and 'Not found: ' in whois.decode():
            return Domain(domain, self.value)
        return whois


class Run:

    def __init__(self, tlds, max_length):
        self.tlds = tuple(TLD(tld) for tld in tlds)
        self.max_length = max_length
        self.domains = []
        self.domains_gen = self.get_domains('', 0)
        self._current_tld = None
    
    def get_domains(self, parent, depth):
        if depth < self.max_length:
            for char in domain_chars:
                if depth == 0 and char in ('_', '-'):
                    continue
                yield parent+char
                for child in self.get_domains(parent+char, depth+1):
                    yield child

    def found_free(self, domain):
        if isinstance(domain, Domain):
            if domain not in self.domains:
                self.domains.append(domain)

    def __iter__(self):
        return self

    def __next__(self):
        domain = self.domains_gen.__next__()
        for tld in self.tlds:
            fulldomain = tld.free(domain)
            self.found_free(fulldomain)
            if isinstance(fulldomain, Domain):
                return fulldomain

if __name__ == '__main__':
    r = Run(['us'], 1)
    print([d for d in r])

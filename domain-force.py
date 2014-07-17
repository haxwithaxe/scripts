import subprocess

domain_chars = [chr(x) for x in [45] + range(48,57) + range(65,90)]

tlds = ['com','co','xxx','asia','biz','mobi','tv','tel','org','net','info','us','ca','cc','bz','me','ch','de','hn']
tlds_short = ['co','tv','us','ca','cc','bz','me','ch','de','hn']

class Domain:
    def __init__(self, domain, tld):
        self.domain = domain
        self.tld = tld

    def free(self):
        output = subprocess.check_output(['whois', '%(domain)s.%(tld)s' % {'domain':self.domain,'tld':self.tld}], shell=True)
        if output and 'Not found: ' in output:
            return True
        return False

def for_tlds():
    for tld in TLDS:
        print('TLD: %s' % tld)
	for_domains()

def get_domain(state={'domain':[],'depth':0,'max':0}):
    for pos in range(len(domain_chars)):
        state['domain'].append(domain_chars[pos])
        state['depth'] += 1
        if state.get('depth') == state.get('max'):
            d = state.get('domain')
            d.append(domain_chars[pos])
            dom = Domain(join(state.get('domain').append()), tld)
            if dom.free():
                print(dom.domain)
        else:
            get_domain(state)


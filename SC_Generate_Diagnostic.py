from tenable.sc import TenableSC

sc = TenableSC('ip of device')
sc.login('username','password')

def diagnostics(self, task=None, options=None, fobj=None):
    task="diagnosticsfile"
    options=all
    fobj=fobj

    with open('diagnostics.tar.gz', 'wb') as fobj:
            sc.system.diagnostics(fobj=fobj)

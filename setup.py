#!/usr/bin/env python

"""utils - small shared utilities for other diffpy packages

Packages:   diffpy.utils
"""

import os
from setuptools import setup, find_packages

# Use this version when git data are not available, like in git zip archive.
# Update when tagging a new release.
FALLBACK_VERSION = '1.1-x'

# versioncfgfile holds version data for git commit hash and date.
# It must reside in the same directory as version.py.
MYDIR = os.path.dirname(os.path.abspath(__file__))
versioncfgfile = os.path.join(MYDIR, 'diffpy/utils/version.cfg')
gitarchivecfgfile = versioncfgfile.replace('version.cfg', 'gitarchive.cfg')

def gitinfo():
    from subprocess import Popen, PIPE
    kw = dict(stdout=PIPE, cwd=MYDIR)
    proc = Popen(['git', 'describe', '--match=v[[:digit:]]*'], **kw)
    desc = proc.stdout.read()
    proc = Popen(['git', 'log', '-1', '--format=%H %at %ai'], **kw)
    glog = proc.stdout.read()
    rv = {}
    rv['version'] = '-'.join(desc.strip().split('-')[:2]).lstrip('v')
    rv['commit'], rv['timestamp'], rv['date'] = glog.strip().split(None, 2)
    return rv


def getversioncfg():
    from ConfigParser import RawConfigParser
    cp = RawConfigParser(dict(version=FALLBACK_VERSION))
    cp.read(versioncfgfile) or cp.read(gitarchivecfgfile)
    gitdir = os.path.join(MYDIR, '.git')
    if not os.path.isdir(gitdir):  return cp
    try:
        g = gitinfo()
    except OSError:
        return cp
    d = cp.defaults()
    if g['version'] != d.get('version') or g['commit'] != d.get('commit'):
        cp.set('DEFAULT', 'version', g['version'])
        cp.set('DEFAULT', 'commit', g['commit'])
        cp.set('DEFAULT', 'date', g['date'])
        cp.set('DEFAULT', 'timestamp', g['timestamp'])
        cp.write(open(versioncfgfile, 'w'))
    return cp

versiondata = getversioncfg()

# define distribution
setup_args = dict(
        name = "diffpy.utils",
        version = versiondata.get('DEFAULT', 'version'),
        namespace_packages = ['diffpy'],
        packages = find_packages(),
        test_suite = 'diffpy.utils.tests',
        include_package_data = True,
        zip_safe = False,
        author = 'Simon J.L. Billinge group',
        author_email = 'sb2896@columbia.edu',
        maintainer = 'Pavol Juhas',
        maintainer_email = 'pavol.juhas@gmail.com',
        description = "Shared utilities for diffpy packages.",
        license = 'BSD-style license',
        url = "https://github.com/diffpy/diffpy.utils/",
        keywords = "text data parsers wx grid",
        classifiers = [
            # List of possible values at
            # http://pypi.python.org/pypi?:action=list_classifiers
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics',
        ],
)

if __name__ == '__main__':
    setup(**setup_args)

# End of file

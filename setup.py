from distutils.core import setup

def get_long_description():
    f = open('README.md')
    data = f.read()
    f.close()
    return data

setup(name = 'eaglepy',
      packages = ['eaglepy'],
      version = '1.0.3',
      description = 'Read, modify, and create Cadsoft EAGLE files',
      long_description = get_long_description(),
      author = 'Richard Clark',
      author_email = 'pydev@richard-h-clark.com',
      url = 'http://richard-h-clark.com/eaglepy',
      keywords = ['cadsoft', 'eagle'],
      classifiers = ['Programming Language :: Python',
                     'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                     'Operating System :: OS Independent',
                     'Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Manufacturing',
                     'Intended Audience :: Science/Research',
                     'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
                     ]
      )
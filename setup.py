from distutils.core import setup
setup(
  name = 'ieee754',
  packages = ['ieee754'],
  version = '0.2',
  license='MIT',
  description = 'A Python library which converts floating points numbers into IEEE-754 representation.',
  author = 'Bora Canbula',
  author_email = 'bora.canbula@cbu.edu.tr',
  url = 'https://github.com/canbula/ieee754',
  download_url = 'https://github.com/canbula/ieee754/archive/refs/tags/v_01.tar.gz',
  keywords = ['IEEE-754', 'binary', 'floating-points', 'binary-representation'],
  install_requires=[
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Mathematics',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
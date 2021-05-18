from setuptools import setup

setup(name='gpcrmining',
      version='0.1.1',
      description='Functions to scrape GPCR data from the web.',
      url='http://github.com/drorlab/GPCR-mining',
      author='Martin Voegele',
      author_email='mvoegele@stanford.edu',
      license='MIT',
      packages=['gpcrmining'],
      zip_safe=False,
      install_requires=[
        'numpy',
        'pandas',
        'click',
        'requests',
      ],
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        # license (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Supported Python versions
        'Programming Language :: Python :: 3',
      ],)


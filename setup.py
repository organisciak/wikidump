from setuptools import setup

setup(name='pywikidump',
      version='0.1',
      description='Library for efficiently parsing Wikipedia export files',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: University of Illinois/NCSA Open Source License',
          'Programming Language :: Python :: 2.7',
          'Natural Language :: English',
          'Topic :: Text Processing :: General'
      ],
      keywords='wikipedia backup',
      url='https://github.com/organisciak/wikidump',
      author='Peter Organisciak',
      author_email='organisciak@gmail.com',
      license='NCSA',
      packages=['pywikidump'],
      install_requires=[
          'nltk',
          'pylibmc',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)

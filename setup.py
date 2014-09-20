from setuptools import setup, find_packages
import os

version = '0.0.4'

requires = [
    'pyramid',
    'dogpile.cache',
    ]

tests_require = [
    'mock',
    ]

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='pyramid_dogpile_cache',
      version=version,
      description="dogpile.cache factory for Pyramid",
      long_description=long_description,
      classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Pyramid",
        ],
      keywords='web wsgi pylons pyramid dogpile cache',
      author='Moriyoshi Koizumi',
      author_email='mozo@mozo.jp',
      url='https://github.com/moriyoshi/pyramid_dogpile_cache',
      license='mit',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require=requires + tests_require,
      extras_require={
        'testing': tests_require,
        },
      install_requires=requires,
      test_suite='pyramid_dogpile_cache',
      entry_points="""
      # -*- Entry points: -*-
      [dogpile.cache]
      file = dogpile.cache.backends.file:DBMBackend
      memcached = dogpile.cache.backends.memcached:MemcachedBackend
      memcached.pylibmc = dogpile.cache.backends.memcached:PylibmcMemcachedBackend
      bmemcached = dogpile.cache.backends.memcached:BMemcachedBackend
      memory = dogpile.cache.backends.memory:MemoryBackend
      redis = dogpile.cache.backends.redis:RedisBackend
      """,
      )

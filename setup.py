# -*- coding: utf8 -*-
import sys
from setuptools import setup, find_packages
install_requires = []

if sys.version_info < (2, 7):
    install_requires.append('argparse')
    install_requires.append('virtualenv')
    install_requires.append('PyYAML==3.12')

setup(name='lae',
      version='0.1_Alpha',
      url='http://gitlab.linkedsee.com/platform/lae',
      license='MIT',
      author='platform@Linkedsee',
      author_email='quxiaolong@yun-ji.cn',
      description='linkedsee app engine',
      install_requires=install_requires,
      classifiers=[
          'Development Status :: 0.1 - Alpha',
          'Intended Audience :: xiaolong',
          'Programming Language :: Python :: 2.7',
      ],
      package_data={"": ["*.tmpl"]},
      include_package_data=True,
      packages=find_packages(exclude=['tests', 'lae.egg-info']),
      long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=['nose>=1.0'],
      test_suite='nose.collector',
      entry_points="""
            [console_scripts]
            lae = lae.lae:main
            """
      )

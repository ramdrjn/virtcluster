
from distutils.core import setup

setup(name='commisioning',
      version='1.0',
      author='vc',
      author_email='vc',
      url='vc',
      packages=['commision'],
      scripts=['vc_com.py'],
      data_files=[('conf', ['rpm.install'])]
      )

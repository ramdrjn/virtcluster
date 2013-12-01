
from distutils.core import setup
setup(name='provisioning',
      version='1.0',
      author='vc',
      author_email='vc',
      url='vc',
      packages=['provision'],
      scripts=['vc_prov.py'],
      package_data={'': ['bootstrap_com.sh']}
      )

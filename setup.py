from setuptools import setup

setup(name='captionbot',
      version='0.1',
      description='Simple API wrapper for https://captionbot.ai',
      url='http://github.com/lucky-user/captionbot',
      author='Tatiana Krikun',
      author_email='krikunts@gmail.com',
      license='MIT',
      packages=['captionbot'],
      install_requires=[
        'requests',
      ],
      zip_safe=False)
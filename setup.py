from distutils.core import setup

setup(
    name='volctl2',
    version='2.0.0',
    author='Hugo Osvaldo Barrera',
    author_email='hugo@osvaldobarrera.com.ar',
    packages=['volctl2'],
    url='https://github.com/hobarrera/volctl2',
    license='LICENSE',
    description='A simple Volume Control application, especially tailored for my Logitech MX Performance.',
    #long_description=open('README.md').read(),
    requires=[
        "pyalsaaudio (>= 0.7)",
        "pynotify (== 0.1.1)",
    ],
    data_files=[('bin', ['volctld'])]
)

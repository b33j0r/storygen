from setuptools import setup

setup(
    name='storygen',
    version='0.1',
    packages=['', 'storygen', 'storygen.names', 'storygen.world', 'storygen.events', 'storygen.people',
              'storygen.culture', 'storygen.utility', 'storygen.languages', 'storygen.languages.tests'],
    package_dir={'': 'src'},
    url='',
    license='Proprietary',
    author='Brian Jorgensen',
    author_email='brian.jorgensen@gmail.com',
    description='',
    install_requires=['numpy'],
    entry_points={
        'console_scripts': []
    },
)

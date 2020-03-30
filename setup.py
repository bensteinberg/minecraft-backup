from setuptools import setup

setup(
    name='minecraft-backup',
    version='0.1',
    py_modules=['backup'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        mcbackup=backup:cli
    ''',
)

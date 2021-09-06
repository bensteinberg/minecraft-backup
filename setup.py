from setuptools import setup

setup(
    name='minecraft-backup',
    version='0.3',
    py_modules=['backup'],
    install_requires=[
        'Click',
        'python-dotenv',
        'mcrcon'
    ],
    entry_points='''
        [console_scripts]
        mcbackup=backup:cli
    ''',
)

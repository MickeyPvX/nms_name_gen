from setuptools import setup

with open('requirements.txt', 'r') as req_file:
    reqs = req_file.read().splitlines()

setup(
    name='nms_name_gen',
    version='1.0.0',
    py_modules=['nms_name_gen'],
    install_requires=reqs,
    entry_points='''
        [console_scripts]
        nms-name-gen=nms_name_gen:main
    ''',
)

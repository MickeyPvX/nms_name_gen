from setuptools import setup

with open('requirements.txt', 'r') as req_file:
    reqs = req_file.read().splitlines()

setup(
    name='nms_name_gen',
    version='0.1.0',
    py_modules=['nms_name_gen'],
    install_requires=reqs,
    entry_points='''
        [console_scripts]
        nms_name_gen=nms_name_gen:entrypoint
    ''',
)

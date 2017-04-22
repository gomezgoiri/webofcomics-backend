from setuptools import setup

setup(
    name='webofcomics',
    packages=['webofcomics'],
    include_package_data=True,
    install_requires=[
        'flask',
        'pymongo',
	'flask-cors',
	'flask_jwt'
    ],
)

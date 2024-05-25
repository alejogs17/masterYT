from setuptools import setup, find_packages

setup(
    name='flask-login-mysql',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-Login',
        'Flask-MySQLdb',
        'Flask-WTF',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'mysqlclient',
        'Werkzeug',
        'WTForms',
        'click',
        'colorama',
        'autopep8',
        'pycodestyle',
        'toml',
    ],
)

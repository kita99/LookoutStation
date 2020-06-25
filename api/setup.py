from setuptools import setup, find_packages

setup(
    name='lookoutstation-api',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'certifi==2020.4.5.1',
        'chardet==3.0.4',
        'click==7.1.1',
        'Flask==1.1.2',
        'Flask-Cors==3.0.8',
        'Flask-SQLAlchemy==2.4.1',
        'idna==2.9',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.2',
        'MarkupSafe==1.1.1',
        'passlib==1.7.2',
        'psycopg2==2.8.5',
        'PyJWT==1.7.1',
        'python-dateutil==2.8.1',
        'requests==2.23.0',
        'six==1.14.0',
        'SQLAlchemy==1.3.17',
        'urllib3==1.25.9',
        'Werkzeug==1.0.1'
    ]
)

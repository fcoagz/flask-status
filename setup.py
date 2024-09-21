import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

setup(
    name='flask-server-status',
    version='0.0.3',
    url='https://github.com/fcoagz/flask-status/',
    license='MIT',
    author='Francisco Griman',
    author_email='grihardware@gmail.com',
    description='It is a Flask extension to view incidents caused by the server',
    long_description=(HERE / "README.md").read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    package_data={
        '': ['flask_server_status/statsig/templates/*.html', 'flask_server_status/statsig/static/*'],
    },
    install_requires=[
        'setuptools==75.1.0'
        'flask>=3.0.0',
        'cachetools>=5.5.0',
        'apscheduler==3.10.4',
        'sqlalchemy==2.0.35',
        'marshmallow==3.22.0',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
    ],
)
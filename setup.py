from os.path import splitext, basename

from glob import glob
from setuptools import setup, find_packages

setup(
    install_requires=[
        "certifi==2020.12.5",
        "chardet==3.0.4",
        "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "google-api-python-client==1.6.2",
        "httplib2==0.19.1",
        "idna==2.7",
        "oauth2client==4.1.3",
        "pyasn1==0.4.8",
        "pyasn1-modules==0.2.8",
        "pyjwt==2.1.0",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "python-dotenv==0.6.4",
        "requests==2.20.0",
        "rsa==4.7.2; python_version >= '3.5' and python_version < '4'",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "uritemplate==3.0.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.24.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3' and python_version < '4'",
    ],
    name="zoom2youtube",
    version="0.0.1",
    description="Transfer video recordings from the Zoom to YouTube",
    url="https://github.com/Welltory/Zoom2Youtube/",
    author="Welltory",
    author_email="github@welltory.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    entry_points={"console_scripts": ["zoom2youtube=zoom2youtube.main:main",],},
    zip_safe=False,
)

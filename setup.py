from setuptools import setup, find_packages

setup(
    name='techfun-uploader',
    version='1.0.0',
    description='Upload files to TechFun\'s server from the command line',
    author='TechFun',
    author_email='david@techfun.me',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tqdm',
        'requests-toolbelt'
    ],
    entry_points={
        'console_scripts': [
            'upload=techfun_upload.cli:main',
        ],
    },
    python_requires='>=3.6',
)

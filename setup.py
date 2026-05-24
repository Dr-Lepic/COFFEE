from setuptools import setup, find_packages
import os
import json

# Read kernel.json to get kernel info
kernel_json_path = os.path.join('java_kernel', 'kernel.json')
with open(kernel_json_path) as f:
    kernel_json = json.load(f)

setup(
    name='java_kernel',
    version='0.1.0',
    description='A Jupyter kernel wrapper for Java',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/java-kernel',
    packages=find_packages(),
    install_requires=[
        'ipykernel>=6.0.0',
        'jupyter_client>=7.0.0',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Framework :: Jupyter',
    ],
    package_data={
        'java_kernel': ['kernel.json'],
    },
    include_package_data=True,
)

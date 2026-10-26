from setuptools import setup, find_packages

setup(
    name='jobtitletransformer',  # Must be unique on PyPI
    version='0.3.0',
    packages=find_packages(exclude=['tests', 'tests.*']), # include=["jobtitletransformer"]
    package_data={"JobTitleTransformer": ["job_scripts/*.py"]},
    install_requires=[
        'pandas',
        'numpy',
        'termcolor',
        'unidecode',
        'tabulate',
        "sentence-transformers",
        "faiss-cpu"
    ],
    author='Prasanna UTHAMARAJ',
    author_email='prasannadatabuss@gmail.com',  # Optional but nice
    description='A healthcare-focused job title transformation pipeline.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PrasannaDataBus/JobTitleTransformer',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing :: Linguistic',
        'Intended Audience :: Healthcare Industry'
    ],
    python_requires='>=3.9'
)
from setuptools import setup, find_packages

setup(
    name='lector_gdrive',
    version='0.1.0',
    description='Librería para leer contenidos de un directorio en Google Drive',
    author='Tu Nombre',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'google-auth',
        'google-auth-oauthlib',
    ],
    python_requires='>=3.7',
)

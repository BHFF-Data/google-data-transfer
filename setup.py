import setuptools

with open("requirements.txt") as f:
    reqs = f.read().splitlines()

setuptools.setup(name='google-data-transfer',
                 version='0.1',
                 description='Automating data transfer between Google Forms and Google Sheets',
                 author='Nejra Smajlovic',
                 install_requires=reqs,
                 author_email='data@bhfuturesfoundation.org',
                 packages=setuptools.find_packages(),
                 zip_safe=False)

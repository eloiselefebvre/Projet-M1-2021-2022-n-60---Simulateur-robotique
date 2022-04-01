from setuptools import find_packages, setup

setup(
    # ...
    name="discoverysimulator",
    version="1.0",
    description="Description",
    keywords="robotic python students simulator",
    long_description="This is the long description",
    packages=find_packages(),
    install_requires=["PyQt5"],

    author="...",
    author_email="...",
    package_data={
         "ressources": ["icons/*"]
     },
    include_package_data=True
    # license="", # search MIT, BSD ?
    # ...
)

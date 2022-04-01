from setuptools import find_packages, setup

setup(
    # ...
    name="discoverysimulator",
    version="1.0",
    description="Description",
    packages=find_packages(),
    install_requires=["PyQt5"],
    keywords="robotic python students simulator",
    author="...",
    author_email="...",
    package_data={
         "ressources": ["icons/*"]
     },
    include_package_data=True,
    license="", # search MIT, BSD ?
    zip_safe=False
    # ...
)

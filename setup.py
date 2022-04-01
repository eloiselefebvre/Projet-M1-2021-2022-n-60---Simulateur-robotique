from setuptools import find_packages, setup

setup(
    # ...
    name="monpackage",
    version="1.0",
    description="Description",
    long_description="This is the long description",
    packages=find_packages(),
    install_requires=[
        "PyQt5"
    ],
    keywords="robotic python",
    author="...",
    author_email="...",
    package_data={
         "ressources": ["icons/*"]
    },
    include_package_data=True,
    # license="", # search MIT, BSD ?
    zip_safe=False
    # ...
)
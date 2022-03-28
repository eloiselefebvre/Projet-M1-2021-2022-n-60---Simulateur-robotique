from setuptools import find_packages, setup

setup(
    # ...
    name="discoverysimulator",
    version="0.1",
    description="Description",
    packages=find_packages(
        where='discoverySimulator',
        include=['*']
    ),
    package_dir={"": "discoverySimulator"},
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
    license="", # search MIT, BSD ?
    zip_safe=False
    # ...
)
from setuptools import find_packages, setup

setup(
    # ...
    name="discovery_simulator",
    version="0.1",
    description="Description",
    packages=find_packages(
        where='discoverySimulator',
        include=['*'],
        exclude=['additional'],
    ),
    package_dir={"": "discoverySimulator"},
    install_requires=[
        "PyQt5"
    ],
    keywords="robotic python",
    author="...",
    author_email="...",
    include_package_data=True,
    license="", # search MIT, BSD ?
    zip_safe=False
    # ...
)
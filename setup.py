from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="discoverySimulator",
    version="1.0",
    description="Description",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="robot robotic python students simulator education teaching",

    packages=find_packages(),
    install_requires=["PyQt5"],

    author="Leo Planquette & Eloise Lefebvre",
    author_email="discoverysimulator@gmail.com",
    url="...",
    package_data={
        '': ['*.svg']
    },
    include_package_data=True,
    license="MIT",
    zip_safe=False
)

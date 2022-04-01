from setuptools import find_packages, setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    # ...
    name="discoverySimulator",
    version="1.0",
    description="Description",
    keywords="robotic python students simulator",
    long_description=readme(),
    long_description_content_type = "text/markdown",
    packages=find_packages(),
    install_requires=["PyQt5"],

    author="Leo Planquette , Eloise LEFEBVRE",
    author_email="leo.planquette@gmail.com , eloise.lefebvre1@gmail.com",
    url = "",
    package_data={
         "ressources": ["icons/footer/*.svg , icons/infos/*.svg, icons/objects/*.svg, icons/states/*.svg, icons/toolbar/*.svg"]
     },
    include_package_data=True
    # license="", # search MIT, BSD ?
    # ...
)

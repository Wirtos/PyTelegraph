import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyTelegraph",
    version="0.3",
    author="Wirtos",
    author_email="Wirtos.new@gmail.com",
    description="Telegra.ph wrapper",
    long_descriptin=long_description,
    long_description_content_type="text/markdown",
    url="t.me/wirtos_new",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.19.1',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

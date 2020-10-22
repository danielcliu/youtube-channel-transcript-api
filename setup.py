import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtube-channel-transcript-api", # Replace with your own username
    version="0.0.1",
    author="Daniel Liu",
    author_email="dcliu@ucdavis.edu",
    description="A python package the utilizes the Youtube Data V3 API to get all transcripts from a given channel/playlist.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielcliu/youtube-channel-transcript-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'google-api-python-client',
        'youtube-transcript-api',
    ],
    )

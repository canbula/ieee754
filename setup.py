from distutils.core import setup

setup(
    name="ieee754",
    packages=["ieee754"],
    version="0.3",
    license="MIT",
    description="A Python module which converts floating points numbers into IEEE-754 representation.",
    author="Bora Canbula",
    author_email="bora.canbula@cbu.edu.tr",
    url="https://github.com/canbula/ieee754",
    download_url="https://github.com/canbula/ieee754/archive/refs/tags/v_03.tar.gz",
    keywords=[
        "IEEE-754",
        "precisions",
        "double-precision",
        "binary",
        "floating-points",
        "binary-representation",
    ],
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)

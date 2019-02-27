# -*- coding: utf-8 -*-

import os
import sys
import platform
import glob

from setuptools import setup, find_packages, Command


if sys.version_info < (3, 6):
    print("Python 3.6 or higher required, please upgrade.")
    sys.exit(1)

version = "0.1"
name = "scholar_bot"
description = ("Post updates on Slack about citations "
               "for the Computational Phyisoligy department at Simula")
scripts = glob.glob("bin/*")
requirements = ['slackclient', 'scholarly', 'pyyaml']

if platform.system() == "Windows" or "bdist_wininst" in sys.argv:
    # In the Windows command prompt we can't execute Python scripts
    # without a .py extension. A solution is to create batch files
    # that runs the different scripts.
    batch_files = []
    for script in scripts:
        batch_file = script + ".bat"
        f = open(batch_file, "w")
        f.write(r'python "%%~dp0\%s" %%*\n' % os.path.split(script)[1])
        f.close()
        batch_files.append(batch_file)
    scripts.extend(batch_files)



def run_install():
    "Run installation"

    # Call distutils to perform installation
    setup(
        name=name,
        description=description,
        version=version,
        author='Henrik Finsberg',
        license="MIT",
        author_email="henrikn@simula.no",
        platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
        packages=["scholar_bot"],
        package_dir={"scholar_bot": "scholar_bot"},
        # install_requires=requirements,
        scripts=scripts,
        zip_safe=False,
    )


if __name__ == "__main__":
    run_install()

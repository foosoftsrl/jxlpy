from setuptools import Extension, setup
from Cython.Build import cythonize
from distutils.command import build as build_module
import os
import subprocess
import platform

# This is the way, if I get it right, in which CIBUILDWHEEL tells us what the architecture is on MACOS
archflags = os.environ.get("ARCHFLAGS", None)
print(f"archflags=\(archflags)")
machine=platform.machine()
buildscript=os.getcwd() + "/build_prerequisites.sh"
builddir=os.getcwd() + f"/build/{machine}"
class build(build_module.build):
  def run(self):
    os.makedirs(builddir,exist_ok=True)
    p = subprocess.Popen(["bash", buildscript, machine], cwd=builddir)
    p.wait()
#    os.system(f'./build_prerequisites.sh \(machine)> build.log 2>&1')
    build_module.build.run(self)

with open("README.md", 'r') as f:
    long_description = f.read()

jxlpy_ext = Extension(
    name="_jxlpy",
    sources=["_jxlpy/_jxl.pyx"],
    include_dirs=[f"{builddir}/sysroot/include"],
    extra_compile_args=['-O2'],
    extra_link_args=[
        f"-L{builddir}/sysroot/lib",
        f"-L{builddir}/sysroot/lib64",
        "-ljxl","-ljxl_threads","-lbrotlidec-static","-lbrotlienc-static","-lbrotlicommon-static","-lhwy"],
    language='c++',
)


setup(name='jxlpy',
      version='0.9.4',
      description='JPEG XL integration in Python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT License',
      author='oloke',
      author_email='olokelo@gmail.com',
      url='http://github.com/olokelo/jxlpy',
      packages=['jxlpy'],
      package_data={
          'jxlpy': ['*.pyx', '*.py'],
          '': ['README.md']
      },
      include_package_data=True,
      install_requires=['cython'],
      extras_require={'pillow': ['Pillow']},
      python_requires='>=3.4',
      ext_modules=cythonize([jxlpy_ext]),
      cmdclass = {
        'build': build,
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: System :: Archiving :: Compression',
          'Topic :: Multimedia :: Graphics',
          'Topic :: Multimedia :: Graphics :: Graphics Conversion',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Cython',
          'Programming Language :: Python :: 3'
      ]
)

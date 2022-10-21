BUILDDIR=$(readlink -f $PWD)
ARCHITECTURE=$1

echo builddir=$BUILDDIR


if [[ "$(uname)" == 'Darwin' ]]; then
  alias nproc="sysctl -n hw.logicalcpu" # As opposed to `hw.physicalcpu`
fi

function checkout_jpeg() {
  pushd $BUILDDIR
  if [ ! -d "libjpeg-turbo" ] ; then
    git clone https://github.com/libjpeg-turbo/libjpeg-turbo.git
  fi
  popd
}

function checkout_libjxl() {
  pushd $BUILDDIR
  if [ ! -d "libjxl" ] ; then
    git clone https://github.com/libjxl/libjxl.git --recursive --shallow-submodules
  fi
  cd libjxl
  git checkout v0.7.0
  popd
}

function build_jpeg() {
  pushd $BUILDDIR/libjpeg-turbo
  mkdir -p build
  cd build
  cmake -DCMAKE_OSX_ARCHITECTURES=$ARCHITECTURE -DCMAKE_INSTALL_PREFIX=$BUILDDIR/sysroot ..
  make -j$(nproc) install
  popd
}

function build_libjxl() {
  pushd $BUILDDIR/libjxl
  git checkout v0.7.0
  mkdir -p build
  cd build
  cmake -DCMAKE_MACOSX_RPATH=0 -DCMAKE_OSX_ARCHITECTURES=$ARCHITECTURE -DJPEGXL_ENABLE_TOOLS=OFF -DBUILD_TESTING=OFF -DJPEGXL_BUNDLE_LIBPNG=ON -DCMAKE_INSTALL_PREFIX=$BUILDDIR/sysroot ..
  make -j$(nproc) install
  #We want a static build, let's remove all dylibs
  rm $BUILDDIR/sysroot/lib/*dylib
  popd
}

checkout_jpeg
checkout_libjxl
build_jpeg
build_libjxl


# Maintainer: Alex Dewar <alex.dewar@gmx.co.uk>
# Contributor: Ray Rashif <schiv@archlinux.org>
# Contributor: Tobias Powalowski <tpowa@archlinux.org>

pkgname=opencv-git
pkgver=4.2.0
pkgrel=2
provides=(opencv opencv-samples)
conflicts=(opencv opencv-samples)
pkgdesc="Open Source Computer Vision Library"
arch=(x86_64)
license=(BSD)
url="http://opencv.org/"
options=(staticlibs)
depends=(intel-tbb openexr gst-plugins-base libdc1394 cblas lapack libgphoto2 jasper)
makedepends=(cmake python-numpy python2-numpy mesa eigen hdf5 lapacke gtk3)
optdepends=('opencv-samples: samples'
            'gtk3: for the HighGUI module'
            'hdf5: support for HDF5 format'
            'opencl-icd-loader: For coding with OpenCL'
            'python-numpy: Python 3 interface'
            'python2-numpy: Python 2 interface')
source=("opencv-$pkgver.tar.gz::https://github.com/opencv/opencv/archive/$pkgver.zip"
        "opencv_contrib-$pkgver.tar.gz::https://github.com/opencv/opencv_contrib/archive/$pkgver.tar.gz")
sha256sums=('55bd939079d141a50fca74bde5b61b339dd0f0ece6320ec76859aaff03c90d9f'
            '8a6b5661611d89baa59a26eb7ccf4abb3e55d73f99bb52d8f7c32265c8a43020')

prepare() {
  mkdir -p build
}

build() {
  cd build
  # cmake's FindLAPACK doesn't add cblas to LAPACK_LIBRARIES, so we need to specify them manually
  _pythonpath=`python -c "from sysconfig import get_path; print(get_path('platlib'))"`
  cmake ../opencv-$pkgver \
    -DOPENCV_ENABLE_NONFREE=ON \
    -DWITH_OPENCL=ON \
    -DWITH_OPENGL=ON \
    -DWITH_TBB=ON \
    -DOpenGL_GL_PREFERENCE=GLVND \
    -DBUILD_WITH_DEBUG_INFO=OFF \
    -DBUILD_TESTS=OFF \
    -DBUILD_PERF_TESTS=OFF \
    -DBUILD_EXAMPLES=ON \
    -DINSTALL_C_EXAMPLES=ON \
    -DINSTALL_PYTHON_EXAMPLES=ON \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCPU_BASELINE_DISABLE=SSE3 \
    -DCPU_BASELINE_REQUIRE=SSE2 \
    -DWITH_CUBLAS=ON \
    -DOPENCV_EXTRA_MODULES_PATH="$srcdir/opencv_contrib-$pkgver/modules" \
    -DCMAKE_BUILD_TYPE=Release \
    -DOPENCV_SKIP_PYTHON_LOADER=ON \
    -DEIGEN_INCLUDE_PATH=/usr/include/eigen3 \
    -DOPENCV_PYTHON3_INSTALL_PATH=$_pythonpath \
    -DLAPACK_LIBRARIES="/usr/lib/liblapack.so;/usr/lib/libblas.so;/usr/lib/libcblas.so" \
    -DLAPACK_CBLAS_H="/usr/include/cblas.h" \
    -DLAPACK_LAPACKE_H="/usr/include/lapacke.h" \
    -DOPENCV_GENERATE_PKGCONFIG=ON
  make
}

package() {
  cd build
  make DESTDIR="$pkgdir" install

  # install license file
  install -Dm644 "$srcdir"/opencv-$pkgver/LICENSE -t "$pkgdir"/usr/share/licenses/$pkgname

  cd "$pkgdir"/usr/share

  # separate samples package; also be -R friendly
  if [[ -d opencv4/samples ]]; then
    mv opencv4 $pkgname # otherwise folder naming is inconsistent
  elif [[ ! -d opencv4 ]]; then
    warning "Directory naming issue; samples package may not be built!"
  fi
}

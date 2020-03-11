from conans import ConanFile, tools
import os


class TensorflowsalusConan(ConanFile):
    name = "tensorflow-devel"
    # we remove compiler from settings so that we can use the package from different compilers
    settings = "os", "arch"
    description = "Development package for tensorflow. This is a total hack exposing all internals of TensorFlow"
    url = "https://github.com/SymbioticLab/tensorflow-salus"
    license = "Apache-2.0"
    author = "Peifeng Yu"

    default_user = "symbioticlab"
    default_channel = "testing"

    export_sources = "TensorFlowConfig.cmake"

    # comma-separated list of requirements
    requires = "zeromq/4.3.2@symbioticlab/stable", "cppzmq/4.6.0@symbioticlab/stable"
    default_options = {
        "zeromq:shared": True,
        "libsodium:shared": True,
    }

    def imports(self):
        # import dependency packages to a central localtion for bazel to consume
        self.copy("*.*", "include", "include")
        self.copy("*.so*", "lib", "lib")

    def package(self):
        # Package header files
        self.copy(
            "*.h", "include", "bazel-tensorflow",
            excludes=(
                "_bin/*", "bazel-out/*",
                # eigen will be copied in whole
                "third_party/eigen3/*",
                "external/eigen_archive/*"
            )
        )
        self.copy("*.h", "include", "bazel-genfiles")

        # Package proto files
        self.copy(
            "*.proto", "include", "bazel-tensorflow",
            excludes=(
                "_bin/*", "bazel-out/*",
            )
        )
        self.copy("*.proto", "include", "bazel-genfiles")

        # Package whole Eigen library, which can't be cover in header files
        self.copy("*", "include/third_party/eigen3", "bazel-tensorflow/third_party/eigen3")
        self.copy("*", "include/external/eigen_archive", "bazel-tensorflow/external/eigen_archive")

        # Package so files
        for libname in ["tensorflow_kernels"]:
            ver = self.version.split('-')[0]
            sover = ver.split('.')[0]
            # fix soname
            with tools.chdir(os.path.join(self.build_folder, "bazel-bin/tensorflow")):
                self.run("ln -s lib{libname}.so.{ver} lib{libname}.so".format(libname=libname, ver=ver))
                self.run("ln -s lib{libname}.so.{ver} lib{libname}.so.{sover}".format(libname=libname, sover=sover))
                self.run("mv lib{libname}.so.{ver}-2.params lib{libname}.so-2.params".format(libname=libname, ver=ver))
            self.copy("lib{}.so*".format(libname), "lib", "bazel-bin/tensorflow", keep_path=False, symlinks=True)
            self.copy("lib{}.so-2.params".format(libname), "lib", "bazel-bin/tensorflow", keep_path=False)

        # Ship a cmake module, conan can automatically find this
        self.copy("TensorFlowConfig.cmake", "lib/cmake/tensorflow", keep_path=False)


    def package_info(self):
        self.cpp_info.name = self.name

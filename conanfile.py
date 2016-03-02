from conans import ConanFile
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake, ConfigureEnvironment


class ZlibNgConan(ConanFile):
    name = "giflib"
    version = "5.1.2"
    ZIP_FOLDER_NAME = "giflib-%s" % version 
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url="http://github.com/lasote/conan-zlib-ng"
    license="https://sourceforge.net/p/giflib/code/ci/master/tree/COPYING"
    exports = ["FindGIF.cmake"]
    
    def config(self):
        try: # Try catch can be removed when conan 0.8 is released
            del self.settings.compiler.libcxx
            del self.settings.os.windows 
        except: 
            pass

    def source(self):
        zip_name = "%s.tar.gz" % self.ZIP_FOLDER_NAME
        download("http://downloads.sourceforge.net/project/giflib/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/autogen.sh" % self.ZIP_FOLDER_NAME)
            

    def build(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
            self.run("cd %s && %s ./autogen.sh" % (self.ZIP_FOLDER_NAME, env.command_line))
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)
            if self.settings.os == "Macos":
                old_str = '-install_name \$rpath/\$soname'
                new_str = '-install_name \$soname'
                replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)

            
            self.run("cd %s && %s ./configure" % (self.ZIP_FOLDER_NAME, env.command_line))
            self.run("cd %s && %s make" % (self.ZIP_FOLDER_NAME, env.command_line))
 
    def package(self):
        # Copy FindGIF.cmake to package
        self.copy("FindGIF.cmake", ".", ".")
        
        # Copying zlib.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % (self.ZIP_FOLDER_NAME), keep_path=False)
        self.copy("*.h", "include", "%s" % ("_build"), keep_path=False)

        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
                self.copy(pattern="*getarg*.a*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src="%s/_build" % self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['gif', 'getarg']

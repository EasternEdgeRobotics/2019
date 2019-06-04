## About


BenethicSpecies.py is a script which counts simulated shapes of benethic species.

The scripts first isolates the shapes by masking only black colors on the camera feed. Each contour is selected using using the moments of polygons on the screen. Checking which shape the contour is, is done in steps.

- To identify rectangles, the ratio of the width to the height is calculated. If the ratio is very small or very large (not close to the value of 1.0), the contour is a rectangle.

- If the contour is not a rectangle, contour approximation is performed on the contour to get a list of vertices. If there are only 3 vertices, the shape is considered a triange.

- Contour approximation doesn't work well when there are no corners of the contour. To identify if the contour is a circle. The bounding ellipse of the contour is found. If the area of the bounding ellipse is equal to or is close to the area of the contour, it is considered a circle.

-Contours that don't fit the above criteria are considered squares.

## How To Use


BenethicSpecies is an external script that is ran outside the control software. To run it, type into a terminal (in the working directory of the script):

```
python3 benethicSpecies.py
```

This will open up a opencv instance of the camera feed. The script will overlay the count of each species and highlight any species found.

To exit the script press the escape (`esc`) key


## Installing Python

### Windows

Python has an installer for windows versions.

Navigate to [python.org](https://www.python.org) and go to the downloads page by clicking `Downloads`.

Download the latest version by clicking the download button below the latest release label. As of May 22nd 2019 this button is labelled `Download Python 3.7.3`. This should start downloading the windows installer for Python. Follow the instructions to install python.

In order for the Python package installer to be access in any directory on the systerm, the scripts folder of the python install must be added to the system's PATH environment variable.


###Linux (Ubuntu)

Python can be installed using the Advanced Package Tool (apt). Open up a terminal windown and type the following command.

To install python2:
```
sudo apt-get install python
```

To install python3:
```
sudo apt-get install python3
```

## How To Build OpenCV4 From Source On Linux

This uses some of the methods as presented by the openCV team. However, I skip some unnecessary steps for our use of OpenCV (aka installing it for C++ and Java). If for some reason the method doesn't setup properly come to me (Troake).

The original tutorial is available [here](https://docs.opencv.org/3.4/d2/de6/tutorial_py_setup_in_ubuntu.html)
  
***

First step is to ensure that we can build the source. Therefore some dependencies are required.
```
sudo apt-get install cmake
sudo apt-get install python-devel numpy
sudo apt-get install gcc gcc-c++
```

Cmake is used for building C applications. OpenCV is a C/C++ based library. It just also has Python support. In order to use extra features such as gstreamer, these dependencies must also be downloaded and installed:
```
sudo apt-get install gtk2-devel
sudo apt-get install libv4l-devel
sudo apt-get install ffmpeg-devel
sudo apt-get install gstreamer-plugins-base-devel
```
The source for OpenCV is on github so you have to clone the repository. Run this command in a location to hold the source.
```
git clone https://github.com/opencv/opencv.git
```

When you run the git clone, it will put it all in a folder called `opencv` in that directory. The next step is to make a directory for the built version of OpenCV. Go into the opencv folder and create a build folder.
```
cd opencv
mkdir build
```

Go into the build directory and run cmake on the parent directory.
```
cd build
cmake ../

(or you can just run cmake from the opencv folder)

cmake
```
You should get something like this close to the end of the cmake log. This confirms that OpenCV recognises  Python 3 on the machine (There may also be some info about Python2. That's all good as long as you see the Python3 info).
```
--   Python 3:
--     Interpreter:                 /usr/bin/python3.4 (ver 3.4.3)
--     Libraries:                   /usr/lib/x86_64-linux-gnu/libpython3.4m.so (ver 3.4.3)
--     numpy:                       /usr/lib/python3/dist-packages/numpy/core/include (ver 1.8.2)
--     packages path:               lib/python3.4/dist-packages
```

After cmake is finished go into the `/build/python_loader` folder and run setup.py.
```
python3 setup.py install
```

## How to install OpenCV4 on Windows

Windows is a little complicated for things like this but if you want to give it a try, check out [this tutorial](https://www.learnopencv.com/install-opencv-4-on-windows/) or follow the instructions below.

### Get dependencies

Download and install Visual Studio Build Tools from [here](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017). When installing select Desktop development with C++.

Download and install CMake from [here](https://cmake.org/download/). When installing add it to your system path.

Download and install Python 3 form [here](https://www.python.org/downloads/).

Download and install git for Windows from [here](https://gitforwindows.org/).

### Install OpenCV4

Download the latest Win pack from [https://opencv.org/releases.html](https://opencv.org/releases.html)

Run the downloaded executable and extract the contents to where you want the program to be installed.

As administrator then run:

```
$ setx -m OPENCV_DIR C:\OPENCVDIR\Build\x64\vc14
```

Where OPENCVDIR is the directory you extracted it to.

Then open the program Edit the system environmental variables, Environmental Variables... and add a new entry to the PATH being `%OPENCV_DIR%\bin`

To add python support go to the python directory opencv\build\python and run the following:

```
$ python setup.py install
```

Everything should now be installed and to check that things are working run:

```
$ python
>>> import cv2
>>> cv2.__version__
```

If it prints out `'4.0.0'` everything is good to go.

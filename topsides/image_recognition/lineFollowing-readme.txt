## About

The TranscectLineAPI is used to interact and analyze the transcent line on the dam. Captures of the camera feed are constantly captured by the script.
Red colors in the frame are masked and used as a giant contour. To determine the orientation of the line, the width is compared to the height.
If the width is greatly larger than the height, the line is horizontal. If the width is greatly smaller, the line is vertical. If the width is about the same length of the height,
it is a corner. When the bot reaches a corner, the border of the frame is scanned for red pixels. If that side has red pixels and is not the side the bot came from, the bot will travel in that direction.

For determining the grid location of the bot, the black lines are masked. When a black line is detected on one side of the frame, it is temperarily saved in memory.
Once the line reaches the opposite side of the frame, the grid location is adjested in respect to which sides were detected.


## How To Use

#### Integrating with Control Software

To use the TranscentLineAPI the script must be imported in the file.

```
import TranscentLineAPI
```

Once the bot is positioned at the start of the line, run the start function in the TranscentLineAPI file.

```
TranscentLineAPI.start()
```

When this is ran, the script will begin to analyze the camera feed and operate the bot.
The script will automatically end when the bot reaches the end of the line.

If the script must be killed before the bot finishes the task. The stop function can be ran.

```
TranscentLineAPI.end()
```

#### Running as Standalone Script

The TranscentLineAPI can be ran as a standalone script. Simply running the following script will begin the script.

```
python TranscentLineAPI.py
```

When the TranscentLineAPI is ran as a standalone script, it will not be able to control the bot.


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
https://www.facebook.com/messages/t/100008529706843
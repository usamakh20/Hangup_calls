1. Install requirements.txt

2. set up ffmpeg or libav for playing audio

    Mac (using homebrew):
    brew install ffmpeg --with-libvorbis --with-sdl2 --with-theora

    Linux (using aptitude):
    apt-get install ffmpeg libavcodec-extra

    Windows:

    Download and extract libav from Windows binaries provided here. http://builds.libav.org/windows/
    Add the libav /bin folder to your PATH envvar
    pip install pydub

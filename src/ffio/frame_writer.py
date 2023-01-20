import numpy as np
import ffmpeg
import sys, os, time
if sys.platform != 'win32':
    import fcntl
from typing import Tuple

class FrameWriter:
    '''Video frame writer to the output video file using ffmpeg.
    
    Args:
        output_file_name (str): output video file name
        size (Tuple[int, int]): frame size (width, height)
        fps (int): frames per second
        bitrate (str): bit rate
        audio (ffmpeg.nodes.FilterableStream): audio stream which is generated by ffmpeg.input
        stdout (bool): if true, writer object outputs the ffmpeg messages to stdout
    
    Attributes:
        video_file_name (str): output video file name
        frame (np.ndarray): Array of frame buffer which shape is (size[1], size[0], 3) and dtype is np.uint8
    '''
    
    video_file_name: str
    frame: np.ndarray
    
    def __init__(self, output_file_name: str, 
                 size: Tuple[int, int] = (1280, 720), 
                 fps: int = 30, bitrate = '10240k', 
                 audio: ffmpeg.nodes.FilterableStream = None, 
                 stdout: bool = False):
        self.video_file_name = output_file_name
        self.fps = fps
        self.stdout = stdout
        video_width, video_height = size
        self.frame = np.zeros((video_height, video_width, 3), dtype=np.uint8)
        output_args = [self.video_file_name]
        if audio:
            output_args.insert(0, audio)
        self.process = (
            ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', r=fps, s=f'{video_width}x{video_height}')
            .output(*output_args, pix_fmt='yuv420p', video_bitrate=bitrate)
            .overwrite_output()
            .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
        )
        if self.stdout:
            if sys.platform != 'win32':
                fl =  fcntl.fcntl(self.process.stderr, fcntl.F_GETFL)
                fcntl.fcntl(self.process.stderr, fcntl.F_SETFL, fl|os.O_NONBLOCK)
            else:
                self.stdout = False

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close(self):
        '''Close writer object.
        '''
        try:
            self.process.stdin.close()
            self.process.stdout.close()
            self.process.stderr.close()
            self.process.wait()
            self.__print_ffmpeg_messages()
            if self.stdout:
                print()
        except:
            pass

    def write_frame(self):
        '''Add a frame in the buffer of the writer object to the output video file.
        '''
        self.write(self.frame)

    def write(self, frame):
        '''Add a frame of the external buffer to the output video file.

        Args:
            frame (np.ndarray): an external buffer which shape is (size[1], size[0], 3) and dtype is np.uint8
        '''
        if frame.shape != self.frame.shape:
            raise ValueError(f'Shape of frame parameter should be {self.frame.shape}, but {frame.shape}')
        self.process.stdin.write(frame.tobytes())
        self.__print_ffmpeg_messages()
    
    def __print_ffmpeg_messages(self):
        if self.stdout and self.process.stderr.readable():
            data = self.process.stderr.read()
            if data:
                print(data.decode('utf-8'), end='')
            sys.stdout.flush()

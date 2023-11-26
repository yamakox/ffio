import numpy as np
import ffmpeg
from dataclasses import dataclass
from typing import Union

@dataclass
class Probe:
    '''Probing first video stream from the input video file.

    Args:
        input_file_name (str): input video file name

    Attributes:
        video_file_name (str): input video file name
        width (int): width of video frame
        height (int): height of video frame
        sample_aspect_ratio (str): sample aspect ratio
        display_aspect_ratio (str): display aspect ratio
        duration (float): duration of video in seconds
        fps (float): frames per seconds
        n_frames (int): number of frames
    '''

    video_file_name: str
    width: int
    height: int
    sample_aspect_ratio: str
    display_aspect_ratio: str
    duration: float
    fps: float
    n_frames: int

    def __init__(self, input_file_name: str):
        self.video_file_name = input_file_name
        probe = ffmpeg.probe(input_file_name)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        self.width = int(video_info['width'])
        self.height = int(video_info['height'])
        self.sample_aspect_ratio = video_info['sample_aspect_ratio'] if 'sample_aspect_ratio' in video_info else None
        self.display_aspect_ratio = video_info['display_aspect_ratio'] if 'display_aspect_ratio' in video_info else None
        self.duration = float(video_info['duration'])
        self.fps = eval(video_info['r_frame_rate'])
        self.n_frames = int(eval('{0}*{1}'.format(video_info['duration'], video_info['r_frame_rate'])))


class FrameReader:
    '''Video frame reader from the input video file using ffmpeg.
    
    Args:
        input_file_name (str): input video file name
        ss (float): start time in seconds
        to (float): stop time in seconds, or end time if None is specified
        n_frames (int): number of frames
        filter_complex (dict[str, Union[dict, list, tuple]]): definition of a complex filtergraph

    Attributes:
        video_file_name (str): input video file name
    '''

    video_file_name: str

    def __init__(self, input_file_name: str, ss: float = 0, to: float = None, n_frames: int = None, filter_complex: dict[str, Union[dict, list, tuple]] = None):
        self.video_file_name = input_file_name
        self.probe = Probe(input_file_name)
        if to is None:
            to = self.probe.duration
        process = ffmpeg.input(input_file_name, ss=ss, to=to)
        if n_frames is not None:
            process = process.filter('fps', n_frames / (to - ss))
        if filter_complex:
            for k, v in filter_complex.items():
                if type(v) == dict:
                    process = process.filter_(k, **v)
                elif type(v) == list or type(v) == tuple:
                    process = process.filter_(k, *v)
                else:
                    process = process.filter_(k, v)
        self.process = (
            process
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run_async(pipe_stdout=True, pipe_stderr=True)
        )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def close(self):
        '''Close reader object.
        '''
        try:
            self.process.stdout.close()
            self.process.stderr.close()
            self.process.wait()
        except:
            pass

    def read_frame(self):
        '''Read a frame from the input video file.
        
        Returns:
            np.ndarray: Array of frame buffer which shape is (height, width, 3) and dtype is np.uint8
        '''
        in_bytes = self.process.stdout.read(self.probe.width * self.probe.height * 3)
        if not in_bytes:
            return None
        return np.frombuffer(in_bytes, np.uint8).reshape([self.probe.height, self.probe.width, 3])

    def frames(self):
        '''Get a generator of input video frames.

        Returns:
            Generator[np.ndarray]: a generator of input video frames
        '''
        while (frame := self.read_frame()) is not None:
            yield frame

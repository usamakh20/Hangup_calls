from pydub import AudioSegment
import matplotlib.pyplot as plt
from pydub.playback import play
import audioop
import numpy as np
from os import listdir

StoMS = 1000  # seconds to milli seconds.
secondsToProcess = 2
data_folder = 'data/'
noise_threshold = 0.1
noise_significant_figures = 3
silence_threshold = 0.3  # Silence ratio less than this in secondsToProcess classifies call as abrupt.


def detectAbruptHangup(recording_filename):
    recording = AudioSegment.from_mp3(data_folder + recording_filename)
    maxAmplitude = recording.max
    noise_amplitude = round(
        (maxAmplitude * noise_threshold) / 10 ** noise_significant_figures) * 10 ** noise_significant_figures

    lastSecondsRecording = recording[-secondsToProcess * StoMS:]

    no_of_samples = recording.duration_seconds * recording.frame_rate
    silence_start_index = no_of_samples - 1
    for sample in lastSecondsRecording.reverse().get_array_of_samples():
        if sample.__abs__() < noise_amplitude:
            silence_start_index -= 1
        else:
            break

    def displayAudio(audio):
        samples = audio.get_array_of_samples()

        x = np.arange(len(samples)) / audio.frame_rate
        y = samples.tolist()

        plt.figure()
        plt.title(recording_filename)
        plt.xlabel('Seconds')
        plt.ylabel('Amplitude')
        plt.plot(x, y)
        plt.ylim(-maxAmplitude, maxAmplitude)
        plt.show()

    silence_ratio = (no_of_samples - silence_start_index - 1) / (secondsToProcess * recording.frame_rate)

    displayAudio(recording)
    displayAudio(lastSecondsRecording)
    print(recording_filename)
    print("Silence Start: %s" % (silence_start_index / recording.frame_rate))
    print("Noise Amplitude: %s" % noise_amplitude)
    print("Silence Ratio: %s" % silence_ratio)
    print("\tOriginal \t|\t Last ")
    print("Rms: %s \t|\t %s" % (recording.rms, lastSecondsRecording.rms))
    print("Max Amplitude: %s \t|\t %s" % (recording.max, lastSecondsRecording.max))
    print("Max DBFS: %s \t|\t %s" % (recording.max_dBFS, lastSecondsRecording.max_dBFS))
    print("Average Amplitude: %s \t|\t %s" % (audioop.avg(recording.raw_data, recording.sample_width),
                                              audioop.avg(lastSecondsRecording.raw_data,
                                                          lastSecondsRecording.sample_width)))
    try:
        play(lastSecondsRecording)
    except:
        print("Recording not Played. Install ffmpeg or libav. See Readme.txt")

    return silence_ratio < silence_threshold, silence_start_index, no_of_samples - 1


if __name__ == '__main__':
    for file_name in listdir(data_folder):
        if detectAbruptHangup(file_name)[0]:
            print("Abrupt Hangup", end='\n\n\n\n')
        else:
            print("Normal", end='\n\n\n\n')

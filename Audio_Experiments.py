from pydub import AudioSegment
from pydub.playback import play

mill_to_sec = 1000

recording = AudioSegment.from_mp3("data/03105199533 Ayesha sadiq Hang up.mp3")

first_10_seconds = recording[:10 * mill_to_sec]
last_5_seconds = recording[-10 * mill_to_sec:]

# boost volume by 6dB
beginning = first_10_seconds + 6

# reduce volume by 3dB
end = last_5_seconds - 3

# 1.5 second crossfade
with_style = beginning.append(end, crossfade=1500)

do_it_over = with_style * 2

# 2 sec fade in, 3 sec fade out
awesome = do_it_over.fade_in(2000).fade_out(3000)

play(awesome)

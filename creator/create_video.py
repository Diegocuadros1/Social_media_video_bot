from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.audio.AudioClip import CompositeAudioClip, concatenate_audioclips 

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI/magick.exe"})


def clip_audio(path):
    try:
        return AudioFileClip(path)
    except:
        print("There has been an error in the path", path)

def clip_video(path):
    try:
        return VideoFileClip(path)
    except:
        print("There has been an error with path", path)

def find_answer(item):
    print(item)
    for i in item:
        if i == item[5]:
            answer = item.index(i)
            print(answer)

    #[letter that was correct, the horizontal position, and the index number of trivia_questions (A: 1, B: 2, C: 3, D: 4)] 
    if answer == 1:
        return ['A', -100, answer]
    if answer == 2:
        return ['B', 0, answer]
    if answer == 3:
        return ['C', 100, answer]
    if answer == 4:
        return ['D', 200, answer]          

def compose_audio(length):
    print("Number of trivia questions: ", length)

    print("Composing Audio...")
    #audio clips
    bell_ding_clip = clip_audio("./creator/tts_output/bell-ding.mp3")
    clock_tick_clip = clip_audio("./creator/tts_output/clock-tick.mp3")

    #cutting clock ticking time and tracking duration for each
    clock_tick_clip_time = 3.5
    clock_tick_clip = clock_tick_clip.subclip(0, clock_tick_clip_time)

    bell_time = bell_ding_clip.duration
    audio_questions = []

    when_show_text = []
    time = 0

    for i in range(length):
        print(i + 1)
        question = clip_audio(f"./creator/tts_output/question{i + 1}.mp3")

        #working with the timer
        show_question = time
        question_duration = question.duration + clock_tick_clip_time
        show_answer = time + question_duration
        duration = question_duration + bell_time

        when_show_text.append([show_question, question_duration, show_answer, duration, bell_time])

        time += duration

        if question:
            #combining the audio sequence
            combination = concatenate_audioclips([question, clock_tick_clip, bell_ding_clip])

            #adding it to the rest of the questions
            audio_questions.append(combination)

    final_audio = concatenate_audioclips(audio_questions)

    # Set the fps for the final audio if it's not set
    if not hasattr(final_audio, 'fps'):
        final_audio.fps = 44100  # Typical audio sample rate

    #final_audio.write_audiofile("./creator/vid_output/audio_output.mp3")

    return final_audio, when_show_text


def loop_video(video, audio_time):

    #find video length
    video_duration = video.duration

    loop_count = int( audio_time // video_duration) + 1

    clips = [video] * loop_count

    #concatinate video clips
    final_clip = concatenate_videoclips(clips)

    #setting final duration to the exact target location
    final_clip = final_clip.set_duration(audio_time)

    return final_clip

def text_to_video(video, trivia_questions, text_times):

    video_width = video.size[0]
    video_height = video.size[1]
    print("WIDTH: ", video_width, "HEIGHT: ", video_height)

    for item in range(len(trivia_questions)):

        answer_found = find_answer(trivia_questions[item])

        start = text_times[item][0]

        whole_duration = text_times[item][3]

        show_green = text_times[item][2]

        rgb_green = 'rgb(98,249,37)'

        answer_duration = text_times[item][4]

        #working with the question text_times = [when question starts, the duration of the question before answer, when to show the answer, duration, duration of the answer]
        text_question = TextClip(trivia_questions[item][0], fontsize=50, color='white', font='Arial', size=video.size)
        text_question = text_question.set_pos(('left', -200)).set_duration(whole_duration)

        text_a = TextClip("A) " + trivia_questions[item][1], fontsize=50, color='white', font='Arial', size=video.size)
        text_a = text_a.set_pos(('left', -100)).set_duration(text_times[item][1])

        text_b = TextClip("B) " + trivia_questions[item][2], fontsize=50, color='white', font='Arial', size=video.size)
        text_b = text_b.set_pos(('left', 0)).set_duration(text_times[item][1])

        text_c = TextClip("C) " + trivia_questions[item][3], fontsize=50, color='white', font='Arial', size=video.size)
        text_c = text_c.set_pos(('left', 100)).set_duration(text_times[item][1])

        text_d = TextClip("D) " + trivia_questions[item][4], fontsize=50, color='white', font='Arial', size=video.size)
        text_d = text_d.set_pos(('left', 200)).set_duration(text_times[item][1])

        #answer_found = [letter that was correct, the horizontal position, and the index number of trivia_questions (A: 1, B: 2, C: 3, D: 4)] 
        answer = TextClip(answer_found[0] + ") " + trivia_questions[item][answer_found[2]], fontsize=50, color=rgb_green, font='Arial', size=video.size)
        answer = answer.set_pos(('left', answer_found[1])).set_duration(answer_duration)

        video = CompositeVideoClip([video, text_question.set_start(start), text_a.set_start(start), text_b.set_start(start), text_c.set_start(start), text_d.set_start(start), answer.set_start(show_green)])

        #writing video to the file
    return video
        



def create_video(trivia_questions, vid_title):

    #background clip
    clip_path = f"./background_videos/{vid_title}.mp4"
    background = clip_video(clip_path)

    audio, text_times = compose_audio(len(trivia_questions))
    print("TEXT TIMES:", text_times)

    audio_time = audio.duration

    #creating the background video long enough to support the audio
    video = loop_video(background, audio_time)

    video = video.set_audio(audio)

    final_video = text_to_video(video, trivia_questions, text_times)

    final_video.write_videofile("final_video.mp4", codec="libx264")









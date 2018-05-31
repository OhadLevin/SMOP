import pygame


freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)

def play_music(music_file):
    try:
        # use the midi file you just saved
        """
            stream music with mixer.music module in blocking manner
            this will stream the sound from disk while playing
            """
        clock = pygame.time.Clock()
        try:
            pygame.mixer.music.load(music_file)
            print("Music file %s loaded!" % music_file)
        except pygame.error:
            print("File %s not found! (%s)" % (music_file, pygame.get_error()))
            return
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(30)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
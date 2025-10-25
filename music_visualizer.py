import pygame
import numpy as np
from scipy.io import wavfile
import sys

# ---------- CONFIG ----------
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 500
BAR_COUNT = 60
FPS = 30
BG_COLOR = (0, 0, 0)
LEFT_COLOR = (0, 200, 255)   # blue-ish for left channel
RIGHT_COLOR = (255, 100, 0)  # orange-ish for right channel

# ---------- LOAD WAV FILE ----------
if len(sys.argv) < 2:
    print("Usage: python3 music_visualizer.py <your_audio_file.wav>")
    sys.exit(1)

wav_file = sys.argv[1]

try:
    sample_rate, data = wavfile.read(wav_file)
except Exception as e:
    print("Error reading WAV file:", e)
    sys.exit(1)

# Handle stereo vs mono
if len(data.shape) == 1:  # mono
    left_channel = data
    right_channel = data
else:  # stereo
    left_channel = data[:, 0]
    right_channel = data[:, 1]

# Normalize
left_channel = left_channel / np.max(np.abs(left_channel))
right_channel = right_channel / np.max(np.abs(right_channel))

# ---------- INIT PYGAME ----------
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Stereo Music Visualizer")
clock = pygame.time.Clock()

print("Stereo Music Visualizer Started")

# ---------- DRAW FUNCTION ----------
def draw_bars(left_frame, right_frame):
    screen.fill(BG_COLOR)
    bar_width = WINDOW_WIDTH // BAR_COUNT
    step = max(len(left_frame) // BAR_COUNT, 1)

    for i in range(BAR_COUNT):
        left_amp = np.abs(left_frame[i * step : (i + 1) * step]).mean()
        right_amp = np.abs(right_frame[i * step : (i + 1) * step]).mean()

        left_height = int(left_amp * WINDOW_HEIGHT)
        right_height = int(right_amp * WINDOW_HEIGHT)

        # Left channel bars (top half)
        pygame.draw.rect(screen, LEFT_COLOR,
                         (i * bar_width, WINDOW_HEIGHT // 2 - left_height, bar_width - 2, left_height))
        # Right channel bars (bottom half)
        pygame.draw.rect(screen, RIGHT_COLOR,
                         (i * bar_width, WINDOW_HEIGHT // 2, bar_width - 2, right_height))

    pygame.display.flip()

# ---------- MAIN LOOP ----------
frame_size = 1024
index = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    left_frame = left_channel[index:index+frame_size]
    right_frame = right_channel[index:index+frame_size]

    if len(left_frame) == 0 or len(right_frame) == 0:
        index = 0  # loop audio
        continue

    draw_bars(left_frame, right_frame)
    index += frame_size
    clock.tick(FPS)

pygame.quit()

'''
game resource
'''
# sound
sound_path = './sound/'
jump_wav = sound_path+'jump.wav'
die_wav = sound_path+'die.wav'
checkpoint_wav = sound_path+'checkPoint.wav'

# sprite
sprite_path = './sprites'
ground = 'ground.png'
replay = 'replay_button.png'
game_over = 'game_over.png'
numbers = 'numbers.png'
dinoJump = 'dino.png'
dinoDuck = 'dino_ducking.png'
cloud = 'cloud.png'
cactusS = 'cacti-small.png'
cactusB = 'cacti-big.png'
ptera = 'ptera.png'

'''
game config
'''
play_sound = True
human = False            # is human playing?
speedup = 5

'''
training ai config
'''
# weights
weight_path = './ai/weights/'
weight = 'weight'

epoch = 1
training = False       # to save weights or not
fresh_pop = False       # to load weights or not

population = 100
best_candidates = 2

mutation_rate = 0.5
mutation_range = (0.5, 1.5)
crossing_points = 2

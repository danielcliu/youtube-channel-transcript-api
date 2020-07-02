with open("test.txt", 'r') as f:
    x = f.read().splitlines()

print(x)

chan_name = 'Esport'
vid_names = ['Big Wiggly Style', 'Biggest plays']

import os
for vid in vid_names:
    filepath=f'test/{chan_name}/{vid.replace(" ", "_")}'
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(f'{vid} is created!')

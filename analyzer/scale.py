NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']

MAJOR_PATTERN = [2, 2, 1, 2, 2, 2, 1]


def build_major_scale(root):
    scale = [root]
    idx = NOTE_NAMES.index(root)

    for step in MAJOR_PATTERN:
        idx = (idx + step) % 12
        scale.append(NOTE_NAMES[idx])

    return scale[:-1]
from mido import MidiFile

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']


def midi_to_note(note_number):
    return NOTE_NAMES[note_number % 12]


def extract_chords_with_bass(midi_file):
    mid = mido.MidiFile(midi_file)

    current_notes = {}
    chords = []
    current_time = 0

    for msg in mid:
        current_time += msg.time

        if msg.type == 'note_on' and msg.velocity > 0:
            current_notes[msg.note] = midi_to_note(msg.note)

        elif msg.type in ['note_off'] or (msg.type == 'note_on' and msg.velocity == 0):
            current_notes.pop(msg.note, None)

        if current_notes:
            bass_note_number = min(current_notes.keys())
            bass_note = current_notes[bass_note_number]

            note_names = list(set(current_notes.values()))

            chords.append({
                "notes": note_names,
                "bass": bass_note,
                "start": current_time
            })

    return chords
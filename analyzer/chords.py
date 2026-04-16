CHORDS = {
    'C': ['C', 'E', 'G'],
    'Dm': ['D', 'F', 'A'],
    'Em': ['E', 'G', 'B'],
    'F': ['F', 'A', 'C'],
    'G': ['G', 'B', 'D'],
    'Am': ['A', 'C', 'E']
}




def detect_chord_with_inversion(notes, bass):
    note_set = set(notes)

    best_match = "Unknown"
    best_score = 0

    for name, chord_notes in CHORDS.items():
        chord_set = set(chord_notes)
        score = len(note_set & chord_set)

        if score > best_score:
            best_score = score
            best_match = name

    if best_match != "Unknown":
        root = best_match.replace('m', '')
        if bass != root:
            return f"{best_match}/{bass}"

    return best_match
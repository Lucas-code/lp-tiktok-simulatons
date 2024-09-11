import mido

def process_sound(path):
    midi_file = mido.MidiFile(path)
    midi_notes =[]

    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                midi_notes.append((msg.note, msg.velocity))
    
    return midi_notes
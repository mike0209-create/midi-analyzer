from flask import Flask, render_template, request
from analyzer.midi import extract_chords_with_bass
from analyzer.chords import detect_chord_with_inversion
from analyzer.scale import build_major_scale

app = Flask(__name__)


def format_time(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m}:{s:02d}"

def analyze(midi_file, key):
    frames = extract_chords_with_bass(midi_file)
    scale = build_major_scale(key)

    results = []

    for frame in frames:
        notes = frame["notes"]
        bass = frame["bass"]
        

        if len(notes) < 3:
            continue

        chord = detect_chord_with_inversion(notes, bass)
        out_of_scale = list(set(notes) - set(scale))

        results.append({
            "notes": notes,
            "bass": bass,
            "chord": chord,
            "out": out_of_scale,
            "start": frame["start"]
        })

    return results


def compress_results(results):
    compressed = []
    prev = None

    for r in results:
        if prev is None or r["chord"] != prev["chord"]:
            compressed.append(r)
            prev = r

    return compressed


@app.route("/", methods=["GET", "POST"])
def index():
    chords = []

    if request.method == "POST":
        file = request.files["file"]
        
        key = request.form.get("key", "C")

        filepath = "temp.mid"
        file.save(filepath)

        results = analyze(filepath, key)
        results = compress_results(results)

        chords = [
            f"{format_time(r['start'])} {r['chord']}/{r['bass']}" for r in results
            ]

    return render_template("index.html", chords=chords)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
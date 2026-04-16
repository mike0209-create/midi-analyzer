import argparse

from analyzer.midi import extract_chords_with_bass
from analyzer.chords import detect_chord_with_inversion
from analyzer.scale import build_major_scale


def analyze(midi_file, key):
    frames = extract_chords_with_bass(midi_file)
    
    
    
    scale = build_major_scale(key)
    
    results = []

    for frame in frames:
        notes = frame["notes"]
        bass = frame["bass"]

        # ノイズ除去（2音以下は無視）
        if len(notes) < 3:
            continue

        chord = detect_chord_with_inversion(notes, bass)

        out_of_scale = list(set(notes) - set(scale))

        results.append({
            "notes": notes,
            "bass": bass,
            "chord": chord,
            "out": out_of_scale
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

def print_result(results, key):
    print(f"\nKey: {key} major")
    print("\n--- Time-based Chord Analysis ---")

    for i, r in enumerate(results):
        notes = ", ".join(r["notes"])
        out = ", ".join(r["out"]) if r["out"] else "none"

        print(f"[{i}] Notes: {notes} | Bass: {r['bass']} -> {r['chord']}")
        print(f"    Out of scale: {out}")


def main():
    parser = argparse.ArgumentParser(description="MIDI Analyzer")
    parser.add_argument("file", help="MIDI file path")
    parser.add_argument("--key", default="C", help="Key (default: C)")

    args = parser.parse_args()

    results = analyze(args.file, args.key)

    results = compress_results(results)
    print_result(results, args.key)


if __name__ == "__main__":
    main()
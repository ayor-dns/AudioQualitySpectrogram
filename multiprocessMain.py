from pathlib import Path
import librosa
import librosa.display
import numpy as np
import soundfile as sf
import time
import matplotlib.pyplot as plt
import matplotlib
import argparse
import multiprocessing


matplotlib.use('agg')
plt.rcParams.update({"font.size": 8})
audio_file_ext = ['.mp3', '.flac', '.wav']
SAVE_PARAMS = {"dpi": 150, "bbox_inches": "tight", "transparent": False}
TICKS = np.array([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000, 22000, 24000])
TICK_LABELS = np.array(["0", "2k", "4k", "6k", "8k", "10k", "12k", "14k", "16k", "18k", "20k", "22k", "24k"])


def is_audio_file(filepath: Path):
    return filepath.suffix in audio_file_ext


def get_destination_path(current_file_path: Path, root_source_path: Path, root_output_path: Path):
    return (root_output_path / current_file_path.relative_to(root_source_path)).parent


def plot_spectrogram_and_save(
        signal, fs, output_path: Path, fft_size=2048, hop_size=None, window_size=None, title=""):
    # default values taken from the librosa documentation
    if not window_size:
        window_size = fft_size

    if not hop_size:
        hop_size = window_size // 4

    stft = librosa.stft(
        signal,
        n_fft=fft_size,
        hop_length=hop_size,
        win_length=window_size,
        center=False,
    )
    spectrogram = np.abs(stft)
    spectrogram_db = librosa.amplitude_to_db(spectrogram, ref=np.max)

    fig, ax = plt.subplots(num=1, figsize=(10, 4), clear=True)
    img = librosa.display.specshow(
        spectrogram_db,
        y_axis="linear",
        x_axis="time",
        sr=fs,
        hop_length=hop_size,
        cmap="inferno",
        ax=ax,
    )
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.ylim(0, 24000)
    plt.gca().set_facecolor('black')
    plt.yticks(TICKS, TICK_LABELS)
    plt.colorbar(img, format="%+2.f dBFS")
    plt.title(title)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        output_path.with_stem(
            f"{output_path.stem}"
        ),
        **SAVE_PARAMS,
    )

    plt.close(fig)


def process_file(data):
    file, source_path, dest_path = data
    process_name = multiprocessing.current_process().name
    start = time.time()
    log = ""
    try:
        title = file.name
        img_output_path = get_destination_path(file, source_path, dest_path)
        output_path = img_output_path / f"{title}.png"

        # check if file already processed
        if not output_path.exists():
            print(f"[{process_name}]\tFILE:\t{file}")
            signal, sample_rate = sf.read(file)
            log += f"[{process_name}]\n"
            log += f"\t{file.name}\n"
            log += f"\t\tSignal's sample rate: {sample_rate}\n"
            log += f"\t\tSignal's shape: {signal.shape}\n"
            plot_spectrogram_and_save(signal[:, 0], sample_rate, output_path=output_path, title=title)
            log += f"\t\tProcess duration: {round(time.time() - start)} seconds\n"
        else:
            log += f"[ALREADY PROCESSED]\t{file.name}\t({output_path})"

        print(f"{log}")

    except Exception as err:
        print(f"ERROR with file={file}")
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser()
    # Adding optional argument
    parser.add_argument("source", help="Folder containing audio files")
    parser.add_argument("-d", "--destination",
                        help="Path where result will be written. If not specified, results are put next to source folder.")
    parser.add_argument("-w", "--workers", type=int, default=1,
                        help="Number of worker processes to use. Set to 0 for max cpu count. Default is 1 and value is clamped to (1, cpu count).")
    args = parser.parse_args()
    source_path = Path(args.source)
    if args.destination is not None:
        dest_path = Path(args.destination)
    else:
        # put result next to source folder in a result folder
        dest_path = Path(source_path.parent) / "Spectrogrambox_result"
    dest_path.mkdir(parents=True, exist_ok=True)

    print("\nSTART\n")
    start_time = time.time()

    # print(f"source : {source_path}")
    # print(f"destination : {dest_path}")

    files = [f for f in source_path.rglob("*") if is_audio_file(f)]
    print(f"Nombre de fichiers audio : {len(files)}")

    if args.workers == 0:
        num_processes = multiprocessing.cpu_count()
    else:
        num_processes = max(1, min(args.workers, multiprocessing.cpu_count()))
    print(f"Utilisation de {num_processes} processus\n")

    tasks = [(f, source_path, dest_path) for f in files]
    with multiprocessing.Pool(num_processes) as pool:
        # Utilisation de pool.map pour paralléliser les traitements
        pool.map(process_file, tasks)

    print(f"[TOTAL TIME] {round(time.time() - start_time)} seconds for {len(files)} audio files")
    print("\n\nEND")

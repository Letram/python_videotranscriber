import os
import sys
import getopt
import time
from splitter import split
from transcriber import transcribe

# https://setuptools.readthedocs.io/en/latest/setuptools.html#developer-s-guide
AUDIO_PATH = "./audios"
AUDIO_EXT = "wav"
EXTRACT_VIDEO_COMMAND = "ffmpeg -hide_banner -loglevel warning -i {from_video_path} -f {audio_ext} -vn {to_audio_path}"
DATETIME = time.strftime("%Y%m%d%H%M%S", time.localtime())

def cronista_transcribe(audio_source_path: str, destination_folder: str, block_of_transcription: int, lang: str, on_transcription_progress = None, to_file: bool = True):
    audio_segments = split(
        audio_source_path, destination_folder, block_of_transcription, to_file)
    transcribe(audio_segments, lang, on_transcription_progress)


def cronista_transcribe_GUI(source_file_path: str, lang: str, block_of_transcription: int, on_transcription_progress):
    DATETIME = time.strftime("%Y%m%d%H%M%S", time.localtime())
    if not os.path.isfile(source_file_path):
        on_transcription_progress("La ruta introducida no es válida")
        exit(-1)

    filename, ext = os.path.splitext(os.path.basename(source_file_path))

    audio_source_path = AUDIO_PATH + "/" + filename + \
        "_{}".format(DATETIME) + "." + AUDIO_EXT

    if not lang in ('es', 'en'):
        on_transcription_progress("Se ha seleccionado un idioma no válido")
        exit(-1)

    command = EXTRACT_VIDEO_COMMAND.format(
        from_video_path=source_file_path, audio_ext=AUDIO_EXT, to_audio_path=audio_source_path)
    os.system(command)

    if not isinstance(block_of_transcription, int):
        on_transcription_progress("La cantidad introducida no está soportada, tiene que ser un número entero.")
        exit(-1)

    destination_folder = AUDIO_PATH + "/" + filename + "_{}".format(DATETIME)
    if not os.path.isdir(destination_folder):
        try:
            os.mkdir(destination_folder)
        except OSError:
            on_transcription_progress("Creation of the directory %s failed" % destination_folder)
            exit(-1)

    cronista_transcribe(audio_source_path, destination_folder,
                        block_of_transcription, lang, on_transcription_progress, True)

def main(argv):
    source_file_path = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv:", ["video="])

    except getopt.GetoptError:
        print('cronista.py -v <videosource>')
        sys.exit(-1)

    # Este for recorre cada una de las opciones que le pasamos al script como clave-valor (option, argument)
    for opt, arg in opts:
        if opt == "-h":
            print('cronista.py -s <videosource>')
        elif opt in ("-v", "--videofile"):
            source_file_path = arg

    if not os.path.isfile(source_file_path):
        print("La ruta introducida no es válida")
        exit(-1)

    filename, ext = os.path.splitext(os.path.basename(source_file_path))

    audio_source_path = AUDIO_PATH + "/" + filename + \
        "_{}".format(DATETIME) + "." + AUDIO_EXT

    lang = input(
        "Seleccione el idioma del audio que hay que transcribir (idiomas soportados: 'es' y 'en'. Por defecto: es): ") or "es"
    if not lang in ('es', 'en'):
        print("Se ha seleccionado un idioma no válido")
        exit(-1)

    command = EXTRACT_VIDEO_COMMAND.format(
        from_video_path=source_file_path, audio_ext=AUDIO_EXT, to_audio_path=audio_source_path)
    os.system(command)
    """
    if not ext == ".wav":
        print("El formato del fichero no está soportado")
        exit(-1)
    """
    block_of_transcription = int(input(
        "Seleccione la cantidad de segundos en los que se dividirá el audio (cantidad recomendada: entre 15 y 20. Por defecto: 20): ") or "20")
    if not isinstance(block_of_transcription, int):
        print("La cantidad introducida no está soportada, tiene que ser un número entero.")
        exit(-1)

    destination_folder = AUDIO_PATH + "/" + filename + "_{}".format(DATETIME)
    if not os.path.isdir(destination_folder):
        try:
            os.mkdir(destination_folder)
        except OSError:
            print("Creation of the directory %s failed" % destination_folder)
            exit(-1)

    cronista_transcribe(audio_source_path, destination_folder,
                        block_of_transcription, lang, True)

if __name__ == "__main__":
    main(sys.argv[1:])

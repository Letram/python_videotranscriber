import speech_recognition as sr
import sys
import getopt
import json
import os
import math

# https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst


def main(argv):
    sound = ""
    sound_folder = ""
    langs = {'es': "es-ES", 'en': "en-US"}
    selected_lang = "es-ES"

    try:
        opts = getopt.getopt(argv, "hl:s:f:", ["lang=, src=, folder="])

    except getopt.GetoptError:
        print('script.py -l <"es", "en">')
        sys.exit(2)

    # Este for recorre cada una de las opciones que le pasamos al script como clave-valor (option, argument)
    for opt, arg in opts:
        if opt == "-h":
            print('script.py -l <"es", "en"> -s <soundfile> -f <soundfolder>')
        elif opt in ("-l", "--lang"):
            selected_lang = langs[arg]
        elif opt in ("-s", "--soundfile"):
            sound = arg
        elif opt in ("-f", "--folder"):
            sound_folder = arg

    r = sr.Recognizer()

    if(sound_folder != ""):
        print("Transcribiendo audio, la lengua seleccionada es: {0}".format(
            selected_lang))
        audio_files = [f for f in sorted(os.listdir(sound_folder))]
        print(audio_files)
        for audio_file in audio_files:
            print("\tReconociendo {0}".format(sound_folder + audio_file))
            with sr.WavFile(sound_folder + audio_file) as source:
                # r.adjust_for_ambient_noise(source, )
                audio = r.record(source)
                try:
                    transcript = r.recognize_google(
                        audio, language=selected_lang)
                    # transcript = r.recognize_sphinx(audio, language=selected_lang, )
                    print("La transcripción del audio es: \n" + transcript)
                except Exception as e:
                    print("Error {} : ".format(e))
    else:
        if sound == "":
            print("No se ha añadido ningún fichero de audio")
            sys.exit(0)
        with sr.AudioFile(sound) as source:
            r.adjust_for_ambient_noise(source)

            print("Transcribiendo audio, la lengua seleccionada es: {0}".format(
                selected_lang))

            audio = r.record(source)

        try:
            print("La transcripción del audio es: \n" +
                  r.recognize_google(audio, language=selected_lang))

        except Exception as e:
            print("Error {} : ".format(e))


def transcribe(audio_segments: list, lang: str, on_transcription_progress):
    r = sr.Recognizer()
    folder = os.path.dirname(audio_segments[0]["audio_path"])
    transcript_list = []
    on_transcription_progress("Transcribiendo audio, la lengua seleccionada es: {0}".format(
        lang))
    for audio_index, audio_file in enumerate(audio_segments):
        print(audio_file)
        on_transcription_progress("\tReconociendo {0} ({1} de {2})".format(
            audio_file["audio_path"], audio_index + 1, len(audio_segments)))
        with sr.WavFile(audio_file["audio_path"]) as source:
            audio = r.record(source, duration = math.ceil(audio_file["duration"]))
            try:
                transcript = r.recognize_google(
                    audio, language=lang)
                transcript_list.append({
                    "from": audio_file["from_time"],
                    "to": audio_file["to_time"],
                    "filename": os.path.basename(audio_file["audio_path"]),
                    "transcription": transcript
                })
                #print("La transcripción del audio es: \n" + transcript)
            except Exception:
                on_transcription_progress("\t\tPista demasiado corta como para transcribir")
                transcript_list.append(
                    {"filename": audio_file, "transcription": ""})
    with open(folder+"/transcript.json", "w", encoding="utf8") as outfile:
        json.dump(transcript_list, outfile, ensure_ascii=False)
        on_transcription_progress("Proceso completado!")


if __name__ == "__main__":
    main(sys.argv[1:])

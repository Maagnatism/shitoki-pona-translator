import pickle
import PySimpleGUI as sg

sg.theme('DarkBlack')   # Add a touch of color

layout = [
    [sg.Titlebar("toki pona Translator!!!!")],
    [sg.Text("Welcome to the (very simple) toki pona translator! Enter a sentence or a single word below:")],
    [sg.InputText(), sg.Button("Enter")],
    [sg.Text("[Your sentence will appear here.]", k = "translation")],
    [sg.Text("")],
    [sg.Checkbox("Debug mode", default = False, enable_events = True, k = '-DEBUG MODE-')]
]

window = sg.Window("", layout, grab_anywhere=True, scaling=2)

toki_pona_file = open('toki_pona', 'rb')
toki_pona_words = pickle.load(toki_pona_file)
toki_pona_file.close()
# print(toki_pona_words)

SPECIAL_WORDS = ["anu", "e", "en", "li", "o", "ala"]


def format_word_def(word):
    return_string = ""
    try:
        for key in toki_pona_words.get(word):
            return_string += (key + ": " + toki_pona_words.get(word).get(key) + "\n")
        return return_string
    except TypeError:
        return "Word not found."


def word_part_def_getter(word, speech):
    ending = ""
    if word.endswith(","):
        ending = ","
        word = word.replace(",", "")
    elif word.endswith("."):
        ending = "."
        word = word.replace(".", "")
    elif word.endswith(":"):
        ending = ":"
        word = word.replace(":", "")
    elif word.endswith("?"):
        # ending = "?"
        word = word.replace("?", "")
    if word in toki_pona_words:
        try:
            # print(toki_pona_words.get(word).get(speech) + " -- speech found")
            if toki_pona_words.get(word).get(speech) is not None:
                return toki_pona_words.get(word).get(speech) + ending
            elif speech == "verbDO" and toki_pona_words.get(word).get("verb") is not None:
                return toki_pona_words.get(word).get("verb") + ending
            else:
                return toki_pona_words.get(word).get("noun") + ending
        except:
            # print(toki_pona_words.get(word).get("noun") + " -- speech not found")
            if debug:
                print(toki_pona_words.get(word).get("noun"), " 61")
            return toki_pona_words.get(word).get("noun") + ending
    else:
        if debug:
            print(word + " -- word not found", " 65")
        return word + ending

# make it check for DO, then use verbDO . if verbDO not found, use verb


def sentence_sorter(word_speech_list):
    sentence_parts = []
    latest_split = 0

    for i in range(len(word_speech_list)):
        if word_speech_list[i][1] != "adj" and word_speech_list[i][1] != "noun" and word_speech_list[i][1] != "DO":
            sentence_parts.append(word_speech_list[latest_split:i])
            sentence_parts.append([word_speech_list[i]])
            latest_split = i + 1

    sentence_parts.append(word_speech_list[latest_split:])
    if debug:
        print(sentence_parts, " 83")
    sorted_sentence = []
    for sentence_part in sentence_parts:
        sorted_sentence.extend(word_speech_sorter(sentence_part))

    return sorted_sentence


# add different definitions for verbs w/ & w/o DO and tawa

def word_speech_sorter(word_speech_list): # assign number priority to each word/speech pair and then sort (noun: 3, adj: 2, personal adj: 1)
    list1 = []
    list2 = []
    list3 = []

    for word_speech in word_speech_list:
        if word_speech[1] == "noun" or word_speech[1] == "DO":
            list3.append(word_speech)
        elif word_speech[1] == "adj" and word_speech[0] in ["ona", "mi", "sina", "o"]:
            list1.append(word_speech)
        elif word_speech[0] not in toki_pona_words:
            list1.append(word_speech)
        else:
            list2.append(word_speech)

    # print(list1)
    # print(list2)
    # print(list3)

    list1.extend(list2)

    list1.extend(list3)
    if debug:
        pass
        # print(list1, " 80")
    # return sorted_word_speeches
    return list1


def translate_phrase(words):
    speech_parts = []

    if debug:
        print("translate_phrase called!!  126")

    verb_found = False
    DO = False

    if "e" in words:
        DO = True

    speech_parts.append("noun")

    i = 1
    while i < len(words):
        if i == 1 and (words[0] == "mi" or words[0] == "sina") and (words[1] not in SPECIAL_WORDS):  # verb is 2nd word (UNLESS NOT):
            verb_found = True
            if DO:
                speech_parts.append("verbDO")
            else:
                if words[1] == "lon":
                    speech_parts.append("verb")
                    speech_parts.append("noun")
                    i += 1
                elif toki_pona_words.get(words[1]).get("verb") is None:
                    if debug:
                        print("Inserting li  149")
                    words.insert(1, "li")
                    speech_parts.append("verbHELP")
                    speech_parts.append("noun")
                    i += 1
                else:
                    speech_parts.append("verb")

        elif words[i] == "li" and verb_found == False:
            # speech_parts[i] = "verb indicator"
            if debug:
                print("li found.  160")
            if DO:
                speech_parts.append("verbDO")
                speech_parts.append("verbDO")
            else:
                if toki_pona_words.get(words[i + 1]).get("verb") is None:
                    speech_parts.append("verbHELP")
                    speech_parts.append("noun")  # maybe change to noun idk
                else:
                    speech_parts.append("verb")
                    speech_parts.append("verb")
            verb_found = True
            i += 1

        # remember to deal with o!! (done)
        # also deal with tan(done) & taso(done) & tawa (done)
        # deal with la (done) and lon (done)
        # fix li translate (done)
        # make so that li translates to "am/is" if no DO and verb has no verb def  (done)

        elif words[i] == "e":
            speech_parts.append("DO indicator")
            speech_parts.append("DO")
            i += 1

        # anu = or, en = and

        elif words[i] == "anu" or words[i] == "en" or words[i] == "taso":
            speech_parts.append("article")
            speech_parts.append("noun")
            i += 1

        elif words[i] == "pi":
            speech_parts.append("regrouper")
            speech_parts.append("noun")
            i += 1

        elif words[i] == "la" or words[i] == "lon" or words[i] == "tan":
            speech_parts.append("context")
            speech_parts.append("noun")
            i += 1

        elif words[i] == "tawa" or words[i] == "kepeken":
            speech_parts.append("other")
            speech_parts.append("noun")
            i += 1

        else:  # adj last resort
            speech_parts.append("adj")

        i += 1

    # print(speech_parts)

    return_sentence = ""
    if debug:
        print("Words:", words, "Speeches:", speech_parts, " 216")
    words_speech_paired = list(zip(words, speech_parts))
    if debug:
        print(words_speech_paired, " 219")

    sorted_sentence = sentence_sorter(words_speech_paired)

    if debug:
        print(sorted_sentence, " 224")

    for i in range(len(words)):
        if debug:
            try:
                print(sorted_sentence[i][0], sorted_sentence[i][1], " 229")
                print(word_part_def_getter(sorted_sentence[i][0], sorted_sentence[i][1]), " 230")
            except IndexError:
                print("index error oops 232")
        try:
            return_sentence += word_part_def_getter(sorted_sentence[i][0], sorted_sentence[i][1])
            return_sentence += " "
        except TypeError:
            pass

    if debug:
        print("Return sentence (phrase):", return_sentence, " 240")
    return return_sentence


def main():
    global debug
    debug = False

    global question
    question = False

    fully_translated = ""

    # put everything in if event == "enter"
    while True:
        event, values = window.read()

        # print(values)

        if event == sg.WIN_CLOSED:
            break

        if event == "Enter":
            
            question = False
            fully_translated = ""

            input_sentence = values[0].strip()

            if "?" in input_sentence:
                question = True

            words = input_sentence.split(" ")

            DO = False
            if "e" in words:
                DO = True

            i = 0
            if question:
                if debug:
                    print("Question detected.")
                while i < len(words):  # if question
                    if words[i] == "ala":
                        if debug:
                            print("Detects ala")
                        try:
                            if words[i - 1] == words[i + 1].replace("?",""):
                                words.pop(i + 1)
                                words.pop(i)
                                if debug:
                                    print("Question: removed ala and verb. Words:" + words + " 291")
                                break
                        except IndexError:
                            if debug:
                                print("Question: tried to remove ala & extra verb but couldn't")
                    i += 1

            if len(words) == 1 and input_sentence.lower() != "debug":
                # print(toki_pona_words.get(words[0]))
                # print(words[0])
                fully_translated = format_word_def(words[0])

            elif input_sentence.lower() != "debug":
                sentence_phrases = []
                latest_comma_split = 0

                for i in range(len(words)):
                    if words[i].endswith(",") or words[i].endswith(".") or words[i].endswith(":") or words[i] == "la":
                        if debug:
                            print("comma/period/ found words[" + str(i) + "]  310")
                        sentence_phrases.append(words[latest_comma_split:i + 1])  # figure out how to translate without comma but put the comma back in the sentence (fixed)
                        latest_comma_split = i + 1
                sentence_phrases.append(words[latest_comma_split:])

                if debug:
                    print(sentence_phrases, " 316")

                # else:

                if debug:
                    print("Number of phrases:", len(sentence_phrases), " 321")
                try:
                    for phrase in sentence_phrases:
                        translated_phrase = translate_phrase(phrase)
                        if debug:
                            print("Phrase: ", phrase, " 326")
                            print("Translated phrase: ", translated_phrase, " 327")
                        fully_translated += translated_phrase

                    if question:
                        fully_translated += "?"
                except:
                    fully_translated = "[Not valid]"

                fully_translated = fully_translated.replace("  ", " ")  # fixes spacing issues

            window["translation"].update(value=fully_translated)
        if event == "-DEBUG MODE-":
            debug = not debug
            # print(debug)
    window.close()


if __name__ == "__main__":
    main()






import random

from truthometer.langchain.wrong_phrase_updater_manager import WrongPhraseUpdaterManager

html_header = """<html> 
<head></head>
<body>
"""

html_footer = """ 
</body>
</html>"""


def replace_upper_lower_case(sentence:str, old_phrase:str, new_phrase:str)->str:
    sentence_lower = sentence.lower()
    pos_start = sentence_lower.find(old_phrase.lower())
    if pos_start>-1:
        pos_end = pos_start + len(old_phrase)
        return sentence[0:pos_start] + new_phrase + sentence[pos_end:len(sentence)]
    else:
        return sentence

class VerificationPageBuilder():
    def __init__(self, use_llm = False):
        self.verif_page_content = ""
        self.content_with_bookmarks = ""
        self.suggested_rewrites = []
        if use_llm:
            self.chatgpt_corrector = WrongPhraseUpdaterManager()
        else:
            self.chatgpt_corrector = None

    def write_html_page(self, text, content):
        suffix = text[0:15].replace(' ', '_')
        filename = f"verification_page_{suffix}.html"
        my_html_file = open(filename, "w", encoding='utf-8')

        #if error found
        if self.verif_page_content.find("<s>")>-1:
            my_html_file.write(html_header + '<h2>Text with suspicious facts</h2>\n' +
                           self.verif_page_content + '\n<h2>Text with <i>suggested rewrites</i></h2>' +
                           ' '.join(self.suggested_rewrites) +'\n'+content + '\n' + html_footer, )
        else:
            my_html_file.write(html_header + '<h2>No suspicious facts are found in text</h2>\n' +
                               self.verif_page_content  + content + '\n' + html_footer, )
        my_html_file.close()
        return filename

    def insert_bookmarks_in_sentence(self, orig_sentence, suspicious_phrases, web_pages, map_seed_hit, map_snip_seed, map_phrase_score):
        if self.chatgpt_corrector is not None:
            suspicious_phrases, map_seed_hit, map_snip_seed = self.chatgpt_corrector.update_based_on_llm_similarity(suspicious_phrases, map_seed_hit, map_snip_seed)

        tag_map = {}
        sentence_with_marked_errors = orig_sentence + ''
        verif_sentence = orig_sentence + ''
        proposed_change_sentence = orig_sentence + ''
        sentence_for_chatgpt = orig_sentence + ''
        orig_sentence_for_chatgpt = orig_sentence + ''
        for phrase in suspicious_phrases:
            tag = phrase.replace(' ', '_')[0:10] + str(random.randint(1, 999))
            if phrase in map_seed_hit:
                hit_num = map_seed_hit[phrase]
                tag_map[hit_num] = tag
            else:
                print("missed phrase (not in substitution map)'"+phrase+"'")
            #orig_sentence = orig_sentence.replace(phrase, f"<a href=\"#{tag}\">{phrase}</a>")
            orig_sentence = replace_upper_lower_case(orig_sentence, phrase, f"<a href=\"#{tag}\">{phrase}</a>")
            sentence_with_marked_errors = replace_upper_lower_case(sentence_with_marked_errors, phrase, f"<s>{phrase}<s>")
            sentence_for_chatgpt = replace_upper_lower_case(sentence_for_chatgpt , phrase, " # ")

        for phrase in suspicious_phrases:
            if verif_sentence.find(phrase)<0:
                pos_start = verif_sentence.lower().find(phrase)
                if pos_start>-1:
                    if phrase in map_snip_seed and phrase in map_phrase_score and map_phrase_score[phrase] < 0.88:
                        verif_sentence = verif_sentence[0:pos_start] + f"<s>{phrase}</s>" + verif_sentence[pos_start+len(phrase):10000000]
            else:
                verif_sentence = replace_upper_lower_case(verif_sentence, phrase, f"<s>{phrase}</s>")
        self.verif_page_content += verif_sentence + '\n <br>'

        for phrase in suspicious_phrases:
            if phrase in map_snip_seed:
                new_phrase = map_snip_seed[phrase]
                score = str (map_phrase_score[phrase])
                #last resort to avoid substitution when it is not needed
                if map_phrase_score[phrase] < 0.88:
                    proposed_change_sentence = replace_upper_lower_case(proposed_change_sentence, phrase, f"<i>{new_phrase}</i>")
                    #+' '+score}</i>")
        self.suggested_rewrites.append(proposed_change_sentence+ '\n <br>')

        background_text_for_sentence = f"<h3>Verification</h3>"
        count = 0
        if web_pages:
            for w in web_pages:
                if not w:
                    break
                title = w.get('name')
                snippet = w.get('snippet')
                url = w.get('url')
                line = f"<p><a href=\"{url}\"> {title}</a></p>"
                if count in tag_map:
                    tag_candidate = tag_map[count]
                    line += f"<br id=\"{tag_candidate}\">" + snippet
                else:
                    line += '<br>' + snippet

                background_text_for_sentence += line + '<br>\n'
                count += 1
                if count > 7:
                    break
        #if in llm mode and error is identified
        if self.chatgpt_corrector is not None and sentence_for_chatgpt.find(' # ')>-1 :
            sentence_for_chatgpt_substituted = self.chatgpt_corrector.perform_substitution(sentence_for_chatgpt, orig_sentence_for_chatgpt)
        else:
            sentence_for_chatgpt_substituted = ""
        if len(sentence_for_chatgpt_substituted )>5 and sentence_for_chatgpt_substituted.find(' # ')<0:
            # replace the last element by sentence improved by llm
            self.suggested_rewrites.pop()
            self.suggested_rewrites.append(sentence_for_chatgpt_substituted+"<br>")

        return '<h2>Sentence and its Verification</h2>' + orig_sentence + '\n' + background_text_for_sentence + '<br>\n',  \
               sentence_with_marked_errors

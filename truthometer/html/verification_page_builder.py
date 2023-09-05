import random

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
    pos_end = pos_start + len(old_phrase)
    return sentence[0:pos_start] + new_phrase + sentence[pos_end:len(sentence)]


class VerificationPageBuilder():
    def __init__(self):
        self.verif_page_content = ""
        self.content_with_bookmarks = ""
        self.suggested_rewrite = ""

    def write_html_page(self, text, content):
        suffix = text[0:15].replace(' ', '_')
        filename = f"verification_page_{suffix}.html"
        my_html_file = open(filename, "w", encoding='utf-8')

        my_html_file.write(html_header + '<h2>Text with suspicious facts</h2>\n' +
                           self.verif_page_content + '\n<h2>Text with <i>suggested rewrites</i></h2>' +
                           self.suggested_rewrite +'\n'+content + '\n' + html_footer, )
        my_html_file.close()
        return filename

    def insert_bookmarks_in_sentence(self, orig_sentence, suspicious_phrases, web_pages, map_seed_hit, map_snip_seed):
        tag_map = {}
        sentence_with_marked_errors = orig_sentence + ''
        verif_sentence = orig_sentence + ''
        proposed_change_sentence = orig_sentence + ''
        for phrase in suspicious_phrases:
            tag = phrase.replace(' ', '_')[0:10] + str(random.randint(1, 999))
            if phrase in map_seed_hit:
                hit_num = map_seed_hit[phrase]
                tag_map[hit_num] = tag
            else:
                print("missed phrase "+phrase)
            #orig_sentence = orig_sentence.replace(phrase, f"<a href=\"#{tag}\">{phrase}</a>")
            orig_sentence = replace_upper_lower_case(orig_sentence, phrase, f"<a href=\"#{tag}\">{phrase}</a>")
            sentence_with_marked_errors = replace_upper_lower_case(sentence_with_marked_errors, phrase, f"<s>{phrase}<s>")

        for phrase in suspicious_phrases:
            if verif_sentence.find(phrase)<0:
                pos_start = verif_sentence.lower().find(phrase)
                verif_sentence = verif_sentence[0:pos_start] + f"<s>{phrase}</s>" + verif_sentence[pos_start+len(phrase):10000000]
            else:
                verif_sentence = replace_upper_lower_case(verif_sentence, phrase, f"<s>{phrase}</s>")
        self.verif_page_content += verif_sentence + '\n <br>'


        for phrase in suspicious_phrases:
            if phrase in map_snip_seed:
                new_phrase = map_snip_seed[phrase]
                proposed_change_sentence = replace_upper_lower_case(proposed_change_sentence, phrase, f"<i>{new_phrase}</i>")
        self.suggested_rewrite += proposed_change_sentence+ '\n <br>'

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

        return '<h2>Sentence and its Verification</h2>' + orig_sentence + '\n' + background_text_for_sentence + '<br>\n',  \
               sentence_with_marked_errors

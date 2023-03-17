import random

html_header = """<html> 
<head></head>
<body>
"""

html_footer = """ 
</body>
</html>"""


class VerificationPageBuilder():
    def __init__(self):
        self.verif_page_content = ""
        self.content_with_bookmarks = ""
        self.suggested_rewrite = ""

    def write_html_page(self, text, content):
        suffix = text[0:15].replace(' ', '_')
        filename = f"verification_page_{suffix}.html"
        my_html_file = open(filename, "w")

        my_html_file.write(html_header + '<h2>Text with suspicious facts</h2>\n' +
                           self.verif_page_content + '\n<h2>Text with <i>suggested rewrites</i></h2>' +
                           self.suggested_rewrite +'\n'+content + '\n' + html_footer)
        my_html_file.close()
        return filename

    def insert_bookmarks_in_sentence(self, orig_sentence, suspicious_phrases, web_pages, map_seed_hit, map_snip_seed):
        tag_map = {}
        verif_sentence = orig_sentence + ''
        proposed_change_sentence = orig_sentence + ''
        for phrase in suspicious_phrases:
            tag = phrase.replace(' ', '_')[0:10] + str(random.randint(1, 999))
            hit_num = map_seed_hit[phrase]
            tag_map[hit_num] = tag
            orig_sentence = orig_sentence.replace(phrase, f"<a href=\"#{tag}\">{phrase}</a>")

        for phrase in suspicious_phrases:
            verif_sentence = verif_sentence.replace(phrase, f"<s>{phrase}</s>")
        self.verif_page_content += verif_sentence + '\n <br>'


        for phrase in suspicious_phrases:
            if phrase in map_snip_seed:
                new_phrase = map_snip_seed[phrase]
                proposed_change_sentence = proposed_change_sentence.replace(phrase, f"<i>{new_phrase}</i>")
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

        return '<h2>Sentence and its Verification</h2>' + orig_sentence + '\n' + background_text_for_sentence + '<br>\n'

import unicodedata
import json

with open("all_unicode_characters.js", "w", encoding="utf-8") as f:
    f.write("[\n")

    for code in range(0x110000): 
        try:
            char = chr(code)
            name = unicodedata.name(char)
            entry = {
                "symbol": char,
                "name": name.title()
            }
            f.write(json.dumps(entry, ensure_ascii=False) + ",\n")
        except ValueError:
            continue 

    f.write("]\n")

print("File 'all_unicode_characters.js' is generated with all Unicode characters!")

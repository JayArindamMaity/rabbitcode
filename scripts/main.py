# this is the main script for handing the data input and output in a convenient manner T_T

import os
import re


print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⡴⢧⣀⠀⠀⣀⣠⠤⠤⠤⠤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⠏⢀⡴⠊⠁⠀⠀⠀⠀⠀⠀⠈⠙⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢶⣶⣒⣶⠦⣤⣀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣟⠲⡌⠙⢦⠈⢧⠀
⠀⠀⠀⣠⢴⡾⢟⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡴⢃⡠⠋⣠⠋⠀
⠐⠀⠞⣱⠋⢰⠁⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠤⢖⣋⡥⢖⣫⠔⠋⠀⠀⠀
⠈⠠⡀⠹⢤⣈⣙⠚⠶⠤⠤⠤⠴⠶⣒⣒⣚⣩⠭⢵⣒⣻⠭⢖⠏⠁⢀⣀⠀⠀⠀⠀
⠠⠀⠈⠓⠒⠦⠭⠭⠭⣭⠭⠭⠭⠭⠿⠓⠒⠛⠉⠉⠀⠀⣠⠏⠀⠀⠘⠞⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢤⣀⠀⠀⠀⠀⠀⠀⣀⡤⠞⠁⠀⣰⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⠿⠀⠀⠀⠀⠀⠈⠉⠙⠒⠒⠛⠉⠁⠀⠀⠀⠉⢳⡞⠉⠀⠀⠀⠀⠀
""")
print("""Welcome to Codesolve!!!
This is the cli for managing the web data XD
""")
import os
import re
import inflect

def get_input(prompt, lowercase=False, case_sensitive=False):
    value = input(prompt)
    if lowercase:
        return value.lower()
    if not case_sensitive:
        return value.strip().lower()
    return value.strip()

def get_multiline_input(end_marker="endloop"):
    print(f"Enter your code (end with '{end_marker}'):")    
    lines = []
    while True:
        line = input()
        if line.strip() == end_marker:
            break
        lines.append(line)
    return '\n'.join(lines)

def build_output_path(platform, category):
    base_path = os.path.join(".", "frontend", "public", "data", platform)
    os.makedirs(base_path, exist_ok=True)
    return os.path.join(base_path, f"{category}.ts")

def parse_existing_file(filepath):
    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'\[\s*(.*?)\s*\];', content, re.DOTALL)
    if not match:
        return []

    array_content = match.group(1).strip()
    if not array_content:
        return []

    entries = []
    pattern = re.compile(
        r'\{\s*quesname:\s*"([^"]+)",\s*'
        r'queslink:\s*"([^"]+)",\s*'
        r'soljava:\s*`([^`]*)`,\s*'
        r'solcpp:\s*`([^`]*)`,\s*'
        r'solpyth:\s*`([^`]*)`\s*\}', re.DOTALL
    )

    for match in pattern.finditer(array_content):
        entries.append({
            "quesname": match.group(1),
            "queslink": match.group(2),
            "soljava": match.group(3),
            "solcpp": match.group(4),
            "solpyth": match.group(5),
        })

    return entries

def number_to_words(num):
    p = inflect.engine()
    return p.number_to_words(num).replace("-", "_").replace(" ", "_")

def format_ts_export(export_name, data_list, platform, category):
    lines = [f"// This file contains {platform} {category} questions", "", f"export const {export_name} = ["]
    for entry in data_list:
        lines.append("    {")
        lines.append(f'        quesname: "{entry["quesname"]}",')
        lines.append(f'        queslink: "{entry["queslink"]}",')
        lines.append(f'        soljava: `{entry["soljava"]}`,' if entry["soljava"] else '        soljava: ``,')
        lines.append(f'        solcpp: `{entry["solcpp"]}`,' if entry["solcpp"] else '        solcpp: ``,')
        lines.append(f'        solpyth: `{entry["solpyth"]}`' if entry["solpyth"] else '        solpyth: ``')
        lines.append("    },")
    lines.append("];")
    return '\n'.join(lines)

def main():
    platform = get_input("Enter platform (leetcode/codeforces/codechef): ", lowercase=True)
    quesname = get_input("Enter question name (case sensitive): ", case_sensitive=True)
    queslink = get_input("Enter question link (case sensitive): ", case_sensitive=True)

    if platform == "leetcode":
        rating = get_input("Enter rating (easy/medium/hard): ", lowercase=True)
        category = rating
        export_name = f"leetcode_{rating}"
    elif platform in ["codeforces", "codechef"]:
        rating = get_input("Enter numeric rating (e.g., 800, 1200): ")
        try:
            rating_num = int(rating)
            lower_bound = (rating_num // 100) * 100
            category = str(lower_bound)
            export_name = number_to_words(lower_bound)
        except ValueError:
            print("Invalid rating.")
            return
    else:
        print("Unsupported platform.")
        return

    language = get_input("Enter language (cpp/java/python): ", lowercase=True)
    code = get_multiline_input()

    filepath = build_output_path(platform, category)
    existing_entries = parse_existing_file(filepath)

    lang_key = {"java": "soljava", "cpp": "solcpp", "python": "solpyth"}[language]

    updated = False
    for entry in existing_entries:
        if entry["quesname"] == quesname and entry["queslink"] == queslink:
            entry[lang_key] = code
            updated = True
            break

    if not updated:
        new_entry = {
            "quesname": quesname,
            "queslink": queslink,
            "soljava": "",
            "solcpp": "",
            "solpyth": ""
        }
        new_entry[lang_key] = code
        existing_entries.append(new_entry)

    ts_content = format_ts_export(export_name, existing_entries, platform, category)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(ts_content)

    print(f"\n✅ Solution saved successfully in: {filepath}")

if __name__ == "__main__":
    main()
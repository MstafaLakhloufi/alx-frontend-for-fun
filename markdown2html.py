#!/usr/bin/python3
import sys
import os
import re
import hashlib

def parse_markdown_line(line):
    # Headings
    heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
    if heading_match:
        level = len(heading_match.group(1))
        content = heading_match.group(2)
        return f"<h{level}>{content}</h{level}>"

    # Unordered List
    if line.startswith("- "):
        return f"<li>{line[2:].strip()}</li>", "ul"

    # Ordered List
    if line.startswith("* "):
        return f"<li>{line[2:].strip()}</li>", "ol"

    # Bold and Emphasis
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)

    # MD5 Hash
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)

    # Remove 'c' characters
    line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)

    return f"<p>{line.strip()}</p>"

def markdown_to_html(input_file, output_file):
    try:
        with open(input_file, 'r') as md_file, open(output_file, 'w') as html_file:
            list_type = None

            for line in md_file:
                line = line.rstrip()

                # Parse line for HTML
                parsed_line = parse_markdown_line(line)

                # Handle list start/end tags
                if isinstance(parsed_line, tuple):
                    parsed_line, new_list_type = parsed_line
                    if new_list_type != list_type:
                        if list_type:
                            html_file.write(f"</{list_type}>\n")
                        list_type = new_list_type
                        html_file.write(f"<{list_type}>\n")
                else:
                    if list_type:
                        html_file.write(f"</{list_type}>\n")
                        list_type = None

                # Write parsed line
                html_file.write(parsed_line + "\n")

            if list_type:
                html_file.write(f"</{list_type}>\n")

    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file, output_file = sys.argv[1], sys.argv[2]
    markdown_to_html(input_file, output_file)
    sys.exit(0)

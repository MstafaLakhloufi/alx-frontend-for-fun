#!/usr/bin/python3
""" 
Write a script markdown2html.py that takes an argument 2 strings:
First argument is the name of the Markdown file
Second argument is the output file name 
"""


if __name__ == '__main__':
    """
    Write a script markdown2html.py that takes an argument 2 strings:
    First argument is the name of the Markdown file
    Second argument is the output file name
    """

    import sys
    import os.path
    import hashlib

    def parse():
        """ dashBool at 0 represents that no ul list is open"""
        dashBool = 0
        odashBool = 0
        pdashBool = 0

        f = open(sys.argv[1], "r")
        for line in f:
            line = midlineparse(line)
            """ 
            if a list has been opened, dash bool is 1
            if the next line isnt a list item, dashbool remains at 2
            if it is it gets set to 1 again
            """
            if (dashBool == 1):
                dashBool = 2
            if (odashBool == 1):
                odashBool = 2
            if (pdashBool == 1):
                pdashBool = 2

            """ line that will be returned """
            finalLine = line

            if line[0] == "#":
                finalLine = mark2header(line)
            elif line[0] == "-":
                finalLine = mark2list(line, dashBool)
                dashBool = 1
            elif line[0] == "*":
                finalLine = mark2olist(line, odashBool)
                odashBool = 1
            elif line[0] != "" and line[0] != " " and line[0] != "\n":
                finalLine = mark2par(line, pdashBool)
                pdashBool = 1

            if os.path.isfile(sys.argv[2]) == False:
                x = open(sys.argv[2], "x")
                x.close

            w = open(sys.argv[2], "a")

            if (dashBool == 2):
                w.write("</ul>\n")
                dashBool = 0
            if (odashBool == 2):
                w.write("</ol>\n")
                odashBool = 0
            if (pdashBool == 2):
                w.write("</p>\n")
                pdashBool = 0
            w.write("{}\n".format(finalLine))
            w.close()

        w = open(sys.argv[2], "a")
        if (dashBool == 1):
            w.write("</ul>\n")
            dashBool = 0
        if (odashBool == 1):
            w.write("</ol>\n")
            odashBool = 0
        if (pdashBool == 1):
            w.write("</p>\n")
            pdashBool = 0
        w.close()
        f.close()

    def mark2header(line):
        """ translates # to <h1> """
        count = 0
        for char in line:
            if char == "#":
                count += 1
                continue
            elif char == " ":
                head = "<h{}>".format(count)
                tail = "</h{}>".format(count)
                finalLine = "{}{}{}".format(head, line[(count+1):].rstrip(), tail)
                return (finalLine)
                break
            else:
                break

    def mark2list(line, dashbool):
        """ translates - to <ul> """
        if (dashbool == 0):
            head = "<ul>\n"
        else:
            head = ""
        body = "<li>{}</li>".format(line[2:].rstrip())
        return "{}{}".format(head, body)

    def mark2olist(line, dashbool):
        """ translates * to <ol> """
        if (dashbool == 0):
            head = "<ol>\n"
        else:
            head = ""
        body = "<li>{}</li>".format(line[2:].rstrip())
        return "{}{}".format(head, body)

    def mark2par(line, dashbool):
        """ translates regular text to <p> and <br/> """
        templine = []
        if (dashbool == 0):
            head = "<p>\n"
        elif (dashbool == 2):
            head = "<br />\n"
        else:
            head = ""
        body = "{}".format(line.rstrip())
        return "{}{}".format(head, body)

    def midlineparse(line):
        """ parses bold and other thing mid line """

        """ bold """
        tokens = line.split('**')
        for i in range(len(tokens)):
            if (i % 2 != 0 and tokens[i+1] != ''):
                tokens[i] = "<b>{}</b>".format(tokens[i])
        nuline = "{}".format(''.join(tokens))

        """ em """
        _tokens = nuline.split('__')
        for j in range(len(_tokens)):
            if (j % 2 != 0 and _tokens[j+1] != ''):
                _tokens[j] = "<em>{}</em>".format(_tokens[j])
        nuline = "{}".format(''.join(_tokens))

        """ md5 """
        square_substring = []
        square_tokens_temp = []
        square_tokens = nuline.split('[[')

        for sub in square_tokens:
            square_tokens_temp.extend(sub.split("]]"))
        for ki in square_tokens[1:]:
            square_tokens_s = ki.split(']]')
            if len(square_tokens_s) > 1:
                square_substring.append(square_tokens_s[0])

        for kj in square_substring:
            pos = square_tokens_temp.index(kj)
            encoded = hashlib.md5(square_tokens_temp[pos].encode())
            square_tokens_temp[pos] = "{}".format(encoded.hexdigest())
        nuline = "{}".format(''.join(square_tokens_temp))

        """ lowercase """
        bracket_substring = []
        bracket_tokens_temp = []
        bracket_tokens = nuline.split('((')

        for sub in bracket_tokens:
            bracket_tokens_temp.extend(sub.split("))"))
        for li in bracket_tokens[1:]:
            bracket_tokens_s = li.split('))')
            if len(bracket_tokens_s) > 1:
                bracket_substring.append(bracket_tokens_s[0])

        for lj in bracket_substring:
            pos = bracket_tokens_temp.index(lj)
            ret = lj.replace('c', '').replace('C', '')
            bracket_tokens_temp[pos] = "{}".format(ret)

        nuline = "{}".format(''.join(bracket_tokens_temp))
        return nuline


    """ function that converts markdown to html """
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)

    if os.path.isfile(sys.argv[1]) == False:
        print("Missing {}".format(sys.argv[1]), file=sys.stderr)
        exit(1)

    parse()
    exit(0)
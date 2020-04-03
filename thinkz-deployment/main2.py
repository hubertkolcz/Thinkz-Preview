from flask import Flask, render_template, request, jsonify, session, Markup
from sympy.abc import x,y
from sympy.parsing.sympy_parser import parse_expr
from processing import symplify_bool
from sympy.parsing.latex import parse_latex
from sympy import simplify, Eq, solveset, init_printing
from sympy.solvers import solve
from sympy import *
import re, sys, subprocess, json
from subprocess import check_output

init_printing()

score = 0
new_eva = ""

escape_dict={'\a':r'\a',
             '\b':r'\b',
             '\c':r'\c',
             '\f':r'\f',
             '\n':r'\n',
             '\r':r'\r',
             '\t':r'\t',
             '\v':r'\v',
             '\'':r'\'',
             '\"':r'\"'}

def raw(text):
    new_string=''
    for char in text:
        try:
            new_string += escape_dict[char]
        except KeyError:
            new_string += char
    return new_string

left_raw = r'\left'
right_raw = r'\right'
plus_raw = r'\;'
frac_raw = raw("\frac")

def fracy(phrase):
    if r'\frac' in phrase:
        print('frac problem')
        phrase = phrase.replace('\frac', frac_raw)

        if phrase[phrase.find('c') + 1] != '{':
           print('frac problem with single number - 1digit/1digit')
           phrase = phrase[:phrase.find('c') + 1] + '{' + phrase[phrase.find('c') + 1:]
           phrase = phrase[:phrase.find('c') + 3] + '}' + phrase[phrase.find('c') + 3:]

        if phrase[phrase.find('}') + 1] != '{':
           print('frac problem with single number')
           phrase = phrase[:phrase.find('}') + 1] + '{' + phrase[phrase.find('}') + 1:]
           phrase = phrase[:phrase.find('}') + 3] + '}' + phrase[phrase.find('}') + 3:]

    return raw(phrase)

def bracelet(phrase):
    if left_raw in phrase:
       print('left brace done')
       phrase = phrase.replace(left_raw, "")

    if right_raw in phrase:
       print('right brace done')
       phrase = phrase.replace(right_raw, "")

    return raw(phrase)


def plus(phrase):
    if plus_raw in phrase:
       print('plus done')
       phrase = phrase.replace(plus_raw, "+")

    return raw(phrase)

def expr(eva):
    eva = raw(eva)
    try:
        eva = plus(eva)
        eva = bracelet(eva)
        parse_latex(raw(eva))
    except:
        print('An error occurred.')
        eva = plus(eva)
        eva = bracelet(eva)
        try:
            parse_latex(raw(eva))
        except:
            print("still error")

    return parse_latex(raw(eva))

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "lkmaslkdsldsamdlsdmasdldsmkdd"


@app.route("/", methods=["GET", "POST"])
def main():
    result = None
    result2 = None

    eq_first = ""
    eq_first_pure = ""
    eq_last = ""
    eq_last_pure = ""

    if "inputs" not in session:
        session["inputs"] = []

    if len(session["inputs"]) > 1:
        if session["inputs"][-1] == session["inputs"][-2]:
            session["inputs"].clear()
            session.modified = True

    errors = ""
    if request.method == "POST":

        # LaTeX

        eq_first = raw(request.form["eq_first"])
        eq_first_pure = raw(request.form["eq_first"])

        eq_last_pure = raw(request.form["eq_last"])
        eq_last = raw(request.form["eq_last"])

        eq_final_1 = raw(request.form["eq_final_1"])
        eq_final_2 = raw(request.form["eq_final_2"])

        score = "null"
        if (eq_first == "" or eq_first == "/" or eq_first == 0) and eq_last == "":
            result2 = "You haven't written any equations to solve or compare."

        elif (eq_first != "" and eq_first != "/") and eq_last == "" and eq_final_1 == "" and eq_final_2 == "":
            result2 = Markup("<p> Write an equation, that will be a next step to finish your task. </p> <p> Then, click on 'Next step to finish' button.</p> <br> <p> Otherwise, try to write the solution: <br> <p> Choose how many solutions has your task, <br> Write on the whitebard a number (value of variable), <br> Click 'First solution' or 'Second solution'. <br> At the end, click 'Check!'.</p>")
        
        elif (eq_first != "" and eq_first != "/") and eq_last == "" and (eq_final_1 != "" or eq_final_2 != ""):
            if eq_first.find('=') != -1:
                try:
                    eq_first_1 = expr(raw(eq_first))
                    eq_first = raw(eq_first).split('=')
                    number31 = expr(raw(eq_first[0]))
                    number32 = expr(raw(eq_first[1]))
                    snumber3 = Eq(number31-number32,0)

                    tester = solveset(snumber3, x)
                    result2 = str(solveset(snumber3, x))

                    if len(solve(snumber3,x)) == 2:
                        if((solve(snumber3,x)[0] == float(expr(raw(eq_final_1)) )and solve(snumber3,x)[1] == float(expr(raw(eq_final_2)))) or (solve(snumber3,x)[1] == float(expr(raw(eq_final_1))) and solve(snumber3,x)[0] == float(expr(raw(eq_final_2))))):
                            try:
                                result2 = "The result is {}. Well done!".format(str(solveset(snumber3, x)))
                                score = "Success. Click 'Start new task!'"
                            except:
                                score = "Error - initial equation has 2 solutions"
                        else: 
                            try:
                                result2 = "Wrong! Try to make another step or write your guess again"
                                score = "You made a mistake. {} is not valid answer".format(float(expr(raw(eq_final_1)) ))
                            except:
                                score = "Error - initial equation has 2 solutions"
                    else:
                        if(solve(snumber3,x)[0] == float(expr(raw(eq_final_1)))):
                            try:
                                score = "Success. You have finished your task. Start once again!"
                                result2 = "The result is {}. Well done!".format(str(solveset(snumber3, x)))
                            except:
                                score = "Error - 1 solution"
                        else: 
                            try:
                                result2 = "Wrong! Try to make another step or write your guess again"
                                score = "You made a mistake."
                            except:
                                score = "Error - initial equation has 2 solutions"

                    session["inputs"].append(score)
                    session.modified = True

                except:
                    result2 = "Something went wrong"

        elif eq_first.find('=') != -1 and eq_last.find('=') != -1:
            try:
                eq_first_1 = expr(raw(eq_first))
                eq_first = raw(eq_first).split('=')
                number31 = expr(raw(eq_first[0]))
                number32 = expr(raw(eq_first[1]))
                snumber3 = Eq(number31-number32,0)

                eq_last_1 = expr(raw(eq_last))
                eq_last = raw(eq_last).split('=')
                number41 = expr(raw(eq_last[0]))
                number42 = expr(raw(eq_last[1]))
                snumber4 = Eq(number41-number42,0)


                if (solveset(snumber3, x) == solveset(snumber4, x)) == True:
                    result2 = "Nice! {} and {} are equivalent. Do the next step or try to write the solution!".format(eq_first_pure, eq_last_pure)
                    rrr = "{} and {} are equivalent".format(eq_first_1,eq_last_1)
                else:
                     result2 = "You made a mistake! {} and {} are not equivalent. Try again!".format(eq_first_pure, eq_last_pure)
                     rrr = "{} and {} are not equivalent".format(eq_first_1,eq_last_1)

                session["inputs"].append(rrr)
                session.modified = True
            except:
                result2 = "Error!"

        elif (eq_first.find('=') != -1 and eq_last.find('=') == -1) or (eq_first.find('=') == -1 and eq_last.find('=') != -1):
                rrr = "If you want to find an equality, you need to write an expressions of the same type"


                session["inputs"].append(rrr)
                session.modified = True

                result2 = "Try to write an expression once again"

        else:
            try:
                eq_first = expr(raw(eq_first))
                eq_last = expr(raw(eq_last))

                result2_bool = symplify_bool(eq_first, eq_last)
                tester = str(result2_bool)

                if result2_bool:
                    result2 = "Nice! {} and {} are equivalent!".format(eq_first_pure, eq_last_pure)
                    rrr = "{} and {} are equvilalent.".format(eq_first,eq_last)
                else:
                    result2 = "You made a mistake! {} and {} are not equivalent. Try again!".format(eq_first_pure, eq_last_pure)
                    rrr = "{} and {} are not equvilalent.".format(eq_first,eq_last)

                session["inputs"].append(rrr)
                session.modified = True
            except:
                result2 = "Error"

        if len(session["inputs"]) == 0:
            numbers_so_far = []
        else:
            numbers_so_far = []
            for el in session["inputs"]:
                numbers_so_far.insert(0, el)



        if request.form.get("action") == "Start again!":
            session["inputs"].clear()
            eq_first_pure = ""
            session.modified = True
            result2 = Markup("<p> Write an equation, that will be the one that you want to solve. </p> <br> <p>Then, click on 'Your task to solve' button.</p>")
            return render_template("index.html", eq_first_pure=eq_first_pure, result2=result2)
        print("eq_first_pure")
        return render_template("index.html", result2=result2, numbers_so_far=numbers_so_far, eq_first_pure=eq_first_pure)
    print("eq_first_pure")
    return render_template("index.html", eq_first_pure=eq_first_pure)

@app.route('/background_process_test', methods=["GET", "POST"])
def background_process_test():
    with open("/home/lyon106/web/seshat/SampleMathExps/exp.scgink","w") as fo:
        fo.write(request.json)
    res = subprocess.run(["/home/lyon106/web/seshat/seshat", "-c", "/home/lyon106/web/seshat/Config/CONFIG", "-i", "/home/lyon106/web/seshat/SampleMathExps/exp.scgink"], stdout=subprocess.PIPE, universal_newlines=True)
    output = str(res)
    output = output.split('\\n')
    for x in range(len(output)):
        print (output[x])
    return json.dumps(output[-2])
from flask import Flask, render_template, request, jsonify, session, Markup
from sympy.abc import x,y
from sympy.parsing.sympy_parser import parse_expr
from processing import symplify_bool
from sympy.parsing.latex import parse_latex
from sympy import simplify, Eq, solveset, init_printing
from sympy.solvers import solve
from sympy.solvers.solveset import solvify, solveset
from sympy import *
import re, sys, subprocess, json
from subprocess import check_output

init_printing()

score = 0
new_eva = ""
new_eq = ""
next_eq = ""
result_eq = ""
final_result = ""

def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`,
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True

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
    eva = eva.replace
    eva = raw(eva)
    try:
        eva = plus(raw(eva))
        eva = bracelet(raw(eva))
        eva = fracy(raw(eva))
        return parse_latex(raw(eva))
    except:
        print('An error occurred.')
        eva = plus(eva)
        eva = bracelet(eva)
        try:
            parse_latex(raw(eva))
        except:
            print("still error")

    return parse_latex(raw(eva))

def strokes_to_latex(request):
    with open("/home/lyon106/web/seshat/SampleMathExps/exp.scgink","w") as fo:
        fo.write(request.json)
    res = subprocess.run(["/home/lyon106/web/seshat/seshat", "-c", "/home/lyon106/web/seshat/Config/CONFIG", "-i", "/home/lyon106/web/seshat/SampleMathExps/exp.scgink"], stdout=subprocess.PIPE, universal_newlines=True)
    output = str(res)
    output = output.split('\\n')

    return output[-2]

def comparison_equality(eq_first,eq_last):
    eq_first_1 = eq_first.replace('\\\\', '\\')
    eq_last_1 = eq_last.replace('\\\\', '\\')

    if eq_first.find('=') != -1 and eq_last.find('=') != -1:
        try:
            eq_first_1 = str(eq_first_1)
            eq_first_1 = eq_first_1.split('=')
            number31 = parse_latex(eq_first_1[0])
            number32 = parse_latex(eq_first_1[1])

            snumber3 = Eq(number31-number32,0)

            eq_last_1 = str(eq_last_1)
            eq_last_1 = eq_last_1.split('=')
            number41 = parse_latex(eq_last_1[0])
            number42 = parse_latex(eq_last_1[1])

            snumber4 = Eq(number41-number42,0)

            return solveset(snumber3, x) == solveset(snumber4, x)
        
        except:
            return "Parsing error"

    elif (eq_first.find('=') != -1 and eq_last.find('=') == -1) or (eq_first.find('=') == -1 and eq_last.find('=') != -1):
        return "False"

    else:
        try:
            eq_first_1 = eq_first.replace('\\\\', '\\')
            eq_last_1 = eq_last.replace('\\\\', '\\')


            eq_first_1 = parse_latex(eq_first_1)
            eq_last_1 = parse_latex(eq_last_1)

            return symplify_bool(eq_first_1, eq_last_1)
        except:
            return "Parsing error"

def check_result(eq_first,eq_result):
    if eq_first.find('=') != -1:
        eq_first_1 = str(eq_first)
        eq_first_1 = eq_first_1.split('=')
        number31 = parse_latex(eq_first_1[0])
        number32 = parse_latex(eq_first_1[1])
        snumber3 = Eq(number31-number32,0) # Tutaj otrzymuję przekształcone równanie, może mieć 1 lub 2 rozwiązania
        sol_number = len(solvify(snumber3,x,S.Reals))
        
        #1 rozwiazanie
        eq_result_1 = str(eq_result)
        if eq_result_1.find('v') == -1:
            if sol_number == 1:
                eq_result_1 = eq_result_1.split('=')
                number41 = parse_latex(eq_result_1[0])
                number42 = parse_latex(eq_result_1[1])
                snumber4 = Eq(number41-number42,0)

                return solveset(snumber3, x) == solveset(snumber4, x)
            else:
                return "This equation has more than 1 solution"

        #2 rozwiazania
        else:
            if sol_number == 2:
                eq_result_1 = eq_result_1.split('v')

                eq_result_11 = eq_result_1[0].split('=')
                number11 = parse_latex(eq_result_11[0])
                number12 = parse_latex(eq_result_11[1])
                snumber1 = Eq(number11-number12,0)

                eq_result_12 = eq_result_1[1].split('=')
                number21 = parse_latex(eq_result_12[0])
                number22 = parse_latex(eq_result_12[1])
                snumber2 = Eq(number21-number22,0)

                cond1 = solvify(snumber3,x,S.Reals)[0] == solvify(snumber1,x,S.Reals)[0]
                cond2 = solvify(snumber3,x,S.Reals)[1] == solvify(snumber2,x,S.Reals)[0]
                cond3 = solvify(snumber3,x,S.Reals)[1] == solvify(snumber1,x,S.Reals)[0]
                cond4 = solvify(snumber3,x,S.Reals)[0] == solvify(snumber2,x,S.Reals)[0]

                # print(cond1,cond2,cond3,cond4)
                # print(solvify(snumber3,x,S.Reals)[0], solvify(snumber3,x,S.Reals)[1])
                # print(solvify(snumber1,x,S.Reals),solvify(snumber2,x,S.Reals))

                return (cond1 and cond2) or (cond3 and cond4)

            else:
                return "This equation has 1 solution"

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
    if request.method == "POST":

        eq_first_pure = raw(request.form["eq_first"])
        eq_first = raw(request.form["eq_first"])

        eq_last_pure = raw(request.form["eq_last"])
        eq_last = raw(request.form["eq_last"])

        eq_final_1 = raw(request.form["eq_final_1"])
        eq_final_2 = raw(request.form["eq_final_2"])


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
                        if((solve(snumber3,x)[0] == float(expr(raw(eq_final_1))) and solve(snumber3,x)[1] == float(expr(raw(eq_final_2)))) or (solve(snumber3,x)[1] == float(expr(raw(eq_final_1))) and solve(snumber3,x)[0] == float(expr(raw(eq_final_2))))):
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
                session["equations"].append(eq_last_pure)
                session.modified = True
            except:
                result2 = "Error!"

        elif (eq_first.find('=') != -1 and eq_last.find('=') == -1) or (eq_first.find('=') == -1 and eq_last.find('=') != -1):
                rrr = "If you want to find an equality, you need to write an expressions of the same type"


                session["inputs"].append(rrr)
                session["equations"].append(eq_last_pure)
                session.modified = True

                result2 = "Try to write an expression once again"

        else:
            try:
                eq_first = expr(request.form["eq_first"])
                #eq_first_1 = expr(raw(eq_first))

                eq_last = expr(request.form["eq_last"])
                #eq_last_1 = expr(raw(eq_last))

                result2 = [eq_first,eq_last,symplify_bool(eq_first, eq_last)]
                result2_bool = symplify_bool(eq_first, eq_last)
                tester = str(result2_bool)

                if result2_bool:
                    result2 = "Nice! {} and {} are equivalent!".format(eq_first_pure, eq_last_pure)
                    rrr = "{} and {} are equvilalent.".format(eq_first,eq_last)
                else:
                    result2 = "You made a mistake! {} and {} are not equivalent. Try again!".format(eq_first_pure, eq_last_pure)
                    rrr = "{} and {} are not equvilalent.".format(eq_first,eq_last)

                session["inputs"].append(rrr)
                session["equations"].append(eq_last_pure)
                session.modified = True
            except:
                result2 = "Error"

        if len(session["inputs"]) == 0:
            numbers_so_far = []
            equations_so_far = []
            numbers_so_far.append("Wprowadz wyrazenia, ktore chcesz porownac")
        else:
            numbers_so_far = []
            equations_so_far = []
            numbers_so_far.append("Rezultaty:")
            for el in session["inputs"]:
                numbers_so_far.insert(0, el)

            for el in session["equations"]:
                equations_so_far.append(el)

        return render_template("index.html", result2=result2, equations_so_far=equations_so_far, numbers_so_far=numbers_so_far, eq_first_pure=eq_first_pure)
    
    return render_template("index.html", eq_first_pure=eq_first_pure)

@app.route('/new_task', methods=["GET", "POST"])
def new_task():
    global new_eq
    new_eq = strokes_to_latex(request)

    return json.dumps(new_eq)

@app.route('/comparison', methods=["GET", "POST"])
def comparison():
    global new_eq
    global next_eq
    next_eq = strokes_to_latex(request)
    
    info = {"eq_start": new_eq, "eq_middle": next_eq, "comparison_result": comparison_equality(new_eq, next_eq)}

    return json.dumps(info)

@app.route('/result', methods=["GET", "POST"])
def result():
    global new_eq
    global result_eq
    result_eq = strokes_to_latex(request)
    final_result = check_result(new_eq,result_eq)
    info = {"eq_start": new_eq, "eq_end": result_eq, "comparison_result": final_result }

    return json.dumps(info)
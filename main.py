#-*- encoding: utf8 -*-
from flask import Flask, render_template, request, abort
from checktools import check_text, is_py_extension, pep8parser, template_results

app = Flask(__name__)

@app.route("/")
def paste_page():
    return render_template("paste_page.html")

@app.route("/checkresult", methods=['POST', ])
def check_result():
    back_url = str(request.referrer).replace(request.host_url, '')
    context = {
        'result': '',
        'code_text': '',
        'error': '',
        'back_url': back_url,
    }
    if request.method == "POST":
        try:
            context['code_text'] = request.form["code"]
        except KeyError:
            abort(404)
        if not context['code_text']:
            context['error'] = u"코드를 입력해 주세요."
            return render_template("check_result.html", **context)
        else:
            context['result'] = check_text(
                context['code_text'],
                '/tmp/'
            )
    return render_template("check_result.html", **context)

if __name__ == '__main__':
    app.run(debug=True)
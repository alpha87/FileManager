#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import secrets
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField
from flask import (Flask, flash, request, redirect, render_template,
                   url_for, send_from_directory, make_response)

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe()
UPLOAD_FOLDER = "./static/upload"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


class FileForm(FlaskForm):
    file = FileField()
    submit = SubmitField("上传")


@app.route("/download/<file_name>", methods=["GET"])
def download(file_name):
    download_file = make_response(
        send_from_directory(UPLOAD_FOLDER, file_name, as_attachment=True))
    download_file.headers["Content-Disposition"] = (
        f"attachment; filename={file_name.encode().decode('latin-1')}")
    return download_file


@app.route("/delete/<file_name>", methods=["GET"])
def delete_file(file_name):
    os.remove(os.path.join(app.config["UPLOAD_FOLDER"], file_name))
    return redirect(url_for("upload"))


@app.route("/", methods=["GET", "POST"])
def upload():
    form = FileForm()
    try:
        all_file = os.listdir(UPLOAD_FOLDER)
    except FileNotFoundError:
        all_file = []

    if request.method == "POST" and form.validate_on_submit():
        # 判断文件夹是否存在
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        # 处理空文件
        if "file" not in request.files:
            flash("上传文件为空")
            return redirect(request.url)

        file = form.file.data
        if file.filename == "":
            flash("文件名无效")
            return redirect(request.url)

        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
        return redirect(url_for("upload"))

    return render_template("index.html", form=form, all_file=all_file)

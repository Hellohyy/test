from flask import Flask, redirect, url_for, request, session
from flask import render_template

from flask_sqlalchemy import SQLAlchemy
from models import CC, LoginForm, Student, Admin
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Graph
import hashlib
import config
from decorators import login_required
import math

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


# md5加密密码
def encrypt_md5(s):
    # 创建md5对象
    new_md5 = hashlib.md5()
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()


@app.route('/', methods=['GET', 'POST'])
def hello_world():

    # result = CC.query.filter(CC.name =='abc').all()
    # cc2 = result[0]
    # print(cc2)
    # # cc2.password = '456'
    # db.session.delete(cc2)
    # db.session.commit()
    return 'Hello World!'


# 首页
@app.route('/index')
@login_required
def index():
    return render_template("index.html")


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    print('11111')
    myForm = LoginForm(request.form)
    if request.method == "GET":
        return render_template('login.html')
    else:
        name = request.form.get('username')
        password = request.form.get('password')
        print(password)
        #pwd = encrypt_md5(str(password))
        user = Admin.query.filter(Admin.name == name, Admin.password == password).first()
        if user:
            session['user_id'] = user.id
            # 31天内不需要登陆
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', ticks='账户密码错误！', form=myForm)


# 用户表单页
@app.route('/form', methods=['GET', 'POST'])
@app.route('/form/<int:page>', methods=['GET', 'POST'])
@login_required
def form(page=None):
    if request.method == 'GET':
        # sql = "select * from cc"
        # stus = db.session.execute(sql)
        stus = CC.query.order_by(CC.id).paginate(page=page, per_page=10, error_out=False)
        # conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='demo', charset='utf8')
        return render_template('form.html', page_data=stus)
    else:
        id = request.form.get('search_id')
        if id:
            cc = CC.query.filter(CC.id == id).order_by(CC.id).paginate(page=page, per_page=10, error_out=False)
            print(cc)
            return render_template("form.html", page_data=cc)
        else:
            cc = CC.query.order_by(CC.id).paginate(page=page, per_page=10, error_out=False)
            return render_template('form.html', page_data=cc)


# 用户表单删除功能
@app.route('/delete/', methods=['GET'])
def form_del():
    # recv_data = request.get_data()
    # print(recv_data)
    uid = request.args.get('id')
    del_cc = CC.query.filter(CC.id == uid).first()
    print(del_cc)
    from exts import db
    db.session.delete(del_cc)
    db.session.commit()
    return redirect(url_for('form'))


# 用户表单修改页面
@app.route("/update/", methods=['GET', 'POST'])
def update():
    uid = request.args.get('id')
    cc = CC.query.filter(CC.id == uid).first()
    username = cc.name
    password = cc.password
    return render_template("update.html", id=uid, username=username, password=password)


# 用户表单修改功能
@app.route('/updateaction/', methods=['GET', 'POST'])
def form_update():
    uid = request.form.get('id')
    print(uid)
    update_cc = CC.query.filter(CC.id == uid).first()
    print(update_cc.password)
    new_name = request.form.get('username')
    new_password = request.form.get('password')
    update_cc.name = new_name
    update_cc.password = encrypt_md5(new_password)
    from exts import db
    db.session.commit()
    return redirect(url_for('form'))


# 用户表单添加页面
@app.route("/add/")
def add():
    return render_template("add.html")


# 用户表单添加功能
@app.route("/addaction/", methods=['GET', 'POST'])
def add_action():
    username = request.form.get('username').all()
    password = request.form.get('password').all()
    pwd = encrypt_md5(password)
    cc = CC(name=username, password=pwd)
    print(username)
    print(password)
    print(cc)
    from exts import db
    db.session.add(cc)
    db.session.commit()
    return redirect(url_for('form'))


# 男女比例图表
@app.route("/charts/pie")
def pie():
    num1 = Student.query.filter(Student.bf_sex == '男').count()
    num2 = Student.query.filter(Student.bf_sex == '女').count()
    attr = {'男生', '女生'}
    v1 = [num1, num2]
    c = (
        Pie()
            .add("", [list(z) for z in zip(attr, v1)])
            .set_global_opts(title_opts=opts.TitleOpts(title="男女比例图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    c.render("templates/pie.html")
    return render_template("pie.html")


# 年龄分布图表
@app.route("/charts/agePie")
def agepie():
    i = 12
    attr =[]
    vl = []
    while(i<35):
        age = 2019 - i
        num = Student.query.filter(Student.bf_BornDate == str(age)).count()
        if num != 0:
            attr.append(str(i)+"岁")
            vl.append(num)
        i = i+1
    c = (
        Pie()
            .add("", [list(z) for z in zip(attr, vl)])
            .set_global_opts(title_opts=opts.TitleOpts(title="年龄分布图"),
                             legend_opts=opts.LegendOpts(type_="scroll", orient="vertical", pos_top="15%", pos_left="2%"),)
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    c.render("templates/agePie.html")
    return render_template("agePie.html")


# 民族柱状图
@app.route('/charts/nation')
def nation():
    attr = ['汉族', '土家族', '朝鲜族', '回族']
    vl = []
    for nations in attr:
        num = Student.query.filter(Student.bf_nation == nations).count()
        vl.append(num)
    c = (
        Bar()
            .add_xaxis(attr)
            .add_yaxis("人数", vl, is_selected=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="民族人数分布图"))
    )
    c.render("templates/nation.html")
    return render_template("nation.html")


# 关系图
@app.route('/charts/relation')
def relation():
    nodes = [
        opts.GraphNode(name="结点1", symbol_size=10),
        opts.GraphNode(name="结点2", symbol_size=20),
        opts.GraphNode(name="结点3", symbol_size=30),
        opts.GraphNode(name="结点4", symbol_size=40),
        opts.GraphNode(name="结点5", symbol_size=50),
    ]
    links = [
        opts.GraphLink(source="结点1", target="结点2"),
        opts.GraphLink(source="结点2", target="结点3"),
        opts.GraphLink(source="结点3", target="结点4"),
        opts.GraphLink(source="结点4", target="结点5"),
        opts.GraphLink(source="结点5", target="结点1"),
    ]
    c = (
        Graph()
            .add("", nodes, links, repulsion=4000)
            .set_global_opts(title_opts=opts.TitleOpts(title="学生关系图"))
    )
    c.render("templates/relation.html")
    return render_template("relation.html")



@app.route("/graph")
def p():
    import json
    import os

    # student = Student.query.first()
    # #j = json.dumps(student)
    # print(student)

    # with open(os.path.join("fixtures", "npmdepgraph.json"), "r", encoding="utf-8") as f:
    #     j = json.load(f)
    # nodes = [
    #     {
    #         "x": node["x"],
    #         "y": node["y"],
    #         "id": node["id"],
    #         "name": node["label"],
    #         "symbolSize": node["size"],
    #         "itemStyle": {"normal": {"color": node["color"]}},
    #     }
    #     for node in j["nodes"]
    # ]
    #
    # edges = [
    #     {"source": edge["sourceID"], "target": edge["targetID"]} for edge in j["edges"]
    # ]
    #
    # c = (
    #     Graph(init_opts=opts.InitOpts(width="1000px", height="600px"))
    #         .add(
    #         "",
    #         nodes=nodes,
    #         links=edges,
    #         layout="none",
    #         label_opts=opts.LabelOpts(is_show=False),
    #         linestyle_opts=opts.LineStyleOpts(width=0.5, curve=0.3, opacity=0.7),
    #     )
    #         .set_global_opts(title_opts=opts.TitleOpts(title="Graph-NPM Dependencies"))
    # )
    # c.render("graph.html")
    return render_template("AAAA.html")


# 学生信息表单页面
@app.route("/student/", methods=['GET', 'POST'])
@app.route("/student/<int:page>", methods=['GET', 'POST'])
@login_required
def student(page=None):
    if page is None:
        page = 1
    if request.method == 'GET':
        u = Student.query.order_by(Student.bf_StudentID).paginate(page=page, per_page=10, error_out=False)
        return render_template("student.html", page_data=u)
    else:
        id = request.form.get("search_id")
        if id:
            u = Student.query.filter(Student.bf_StudentID==id).order_by(Student.bf_StudentID).paginate(page=page, per_page=10, error_out=False)
            return render_template("student.html", page_data=u)
        else:
            u = Student.query.order_by(Student.bf_StudentID).paginate(page=page, per_page=10, error_out=False)
            return render_template("student.html", page_data=u)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



from pyecharts.charts import Bar
from pyecharts.charts import Pie
import pyecharts_snapshot
from pyecharts import options as opts
from models import Student
import random
#num1 = Student.query.filter(Student.bf_sex == '男')
#num2 = Student.query.filter(Student.bf_sex == '女')

# zip = {
#     '男': num1,
#     '女': num2
# }

# bar = Bar()
# bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
# bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# # 也可以传入路径参数，如 bar.render("mycharts.html")



# def pie() ->Pie:
#     c = (
#         pie()
#         .add("", [list(z) for z in zip()])
#         .set_global_opts(title_opts=opts.TitleOpts(title="男女比例图"))
#         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
#     )
#     return c

attr = {'男生', '女生'}
v1 = [48, 50]
# pie = Pie()
# pie.add("男女比例", [list(z) for z in zip(attr.choose(),attr.values())])
# pie.show_config()
# pie.render('templates/pie.html')


from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Page, Pie
c = (
        Pie()
        .add("", [list(z) for z in zip(attr, v1)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
c.render("templates/pie.html")



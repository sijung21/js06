from pyecharts import Line

attr = ["0.22", "1.60", "3.00", "6.00", "20.00"]
v1 = [5, 20, 36, 10, 100]
v2 = [55, 60, 16, 20, 80]
line = Line("Extinction coefficient")
line.add("red", attr, v1, is_stack=True, is_label_show=True)
line.add("blue", attr, v2, is_stack=True, is_label_show=True)
line.show_config()
line.render()
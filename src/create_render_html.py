from pyecharts import Bar

bar = Bar("My first bar chart", "For our fashion shop client")
bar.use_theme('dark')
bar.add("Clothes", ["T-shirt", "Sweater", "Georgette", "Trousers", "High-heels", "Socks"], [5, 20, 36, 10, 75, 90])
bar.render()
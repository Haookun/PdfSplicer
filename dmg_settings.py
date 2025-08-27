
# dmgbuild 配置文件
application = 'PdfSplicer'
icon = 'app_icon.icns'  # 如有图标请替换路径，无则可去掉此行
filename = 'PdfSplicer.dmg'
volume_name = 'PdfSplicer'
files = [
    'dist/PdfSplicer',
    'dist/PdfSplicer.app'
]
symlinks = {
    'Applications': '/Applications'
}
icon_locations = {
    'PdfSplicer': (140, 120),
    'PdfSplicer.app': (140, 120),
    'Applications': (500, 120)
}
app_symlink = {
    'PdfSplicer': 'dist/PdfSplicer.app'
}
format = 'UDBZ'
show_hidden = False
show_status = True

"""把 按事论点与道理_独立稿/ 合成单文件网页（合并版.html）。
先在临时目录里清掉不该显示的标记：页内锚点 <a id="..."></a>（不论单独成行还是夹在正文里）、
来源编号链接 [S01-1](#s01-1)，普通链接只留文字；再交给 daoli2page.py 渲染。
渲染完检查一遍：页面里不能再出现被转义成文字的标签（&lt;a、&lt;/a 之类），出现就报错退出。
用法：python3 独立稿2page.py"""
import re, glob, os, sys, tempfile, subprocess

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.abspath(os.path.join(here, '../../按事论点与道理_独立稿'))
out_html = os.path.join(src, '合并版.html')
title = '道理卡合并版'
intro = ('astra 独立稿和 Claude 重写稿逐面合并：21 件事，每面一句论点、主用和备用道理、作用链和核对。'
         '只换了道理位，其余三栏是 astra 的原稿。【】和〔2026省市 材料三〕是脚本核过的原文；'
         '〔常用说法〕仓库无原文，冠出处前先核；〔自拟〕没有出处。')

with tempfile.TemporaryDirectory() as tmp:
    files = sorted(glob.glob(os.path.join(src, '[0-9][0-9]_*.md'))) + [os.path.join(src, '合并记录_两版道理位.md')]
    for f in files:
        t = open(f, encoding='utf-8').read()
        t = re.sub(r'<a id="[^"]*">\s*</a>', '', t)                          # 页内锚点，不论在哪
        t = re.sub(r'^\s*$\n(?=\s*$)', '', t, flags=re.M)                     # 删锚点后留下的连续空行
        t = re.sub(r'\[[A-Z][A-Za-z0-9\-]{1,12}\]\([^)]*\)', '', t)           # 来源编号链接整个去掉
        t = re.sub(r'\[([^\]]*)\]\((?:#|https?://)[^)]*\)', r'\1', t)         # 其余链接只留文字
        name = '00_说明.md' if os.path.basename(f).startswith('合并记录') else os.path.basename(f)
        open(os.path.join(tmp, name), 'w', encoding='utf-8').write(t)
    subprocess.run([sys.executable, os.path.join(here, 'daoli2page.py'), tmp, out_html, title, intro], check=True)

page = open(out_html, encoding='utf-8').read()
leaks = re.findall(r'&lt;/?[a-zA-Z][^&]{0,20}', page)
if leaks:
    print('页面里还有标签文字：', sorted(set(leaks))[:10]); sys.exit(1)
print('检查通过：页面里没有漏出来的标签')

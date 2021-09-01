
```python 
import logging

from LAC import LAC
from django.conf import settings
from django.core.management.base import BaseCommand
from rich.console import Console
from rich.table import Table

logger = logging.getLogger('mxlog')


class Command(BaseCommand):
    def add_arguments(self, parser):
        self.lac = LAC(mode='lac')
        self.lac.load_customization(str(settings.RESOURCE_ROOT / 'docs' / 'program' / 'lac_person_costom.txt'))

    def handle(self, *args, **options):
        pmap = {
            'n': '普通名词',
            'f': '方位名词',
            's': '处所名词',
            'nw': '作品名',
            'nz': '其他专名',
            'v': '普通动词',
            'vd': '动副词',
            'vn': '名动词',
            'a': '形容词',
            'ad': '副形词',
            'an': '名形词',
            'd': '副词',
            'm': '数量词',
            'q': '量词',
            'r': '代词',
            'p': '介词',
            'c': '连词',
            'u': '助词',
            'xc': '其他虚词',
            'w': '标点符号',
            'PER': '人名',
            'LOC': '地名',
            'ORG': '机构名',
            'TIME': '时间',
        }
        for line in (settings.RESOURCE_ROOT / 'docs' / 'program' / '姓名识别100个例子.txt').read_text(
                encoding='utf8').splitlines():
            line = line.strip()
            if not line:
                continue
            ws, ps = self.lac.run(line)
            # tb = pt.PrettyTable(range(len(ws)))
            # tb.add_row(ws)
            # tb.add_row(ps)
            # tb.add_row([pmap[p] for p in ps])
            # print(tb)
            # print('*'*100)

            console = Console()

            table = Table(show_header=True, header_style="bold yellow")  # show_header是否显示表头，header_style表头样式
            for i in range(len(ws)):
                table.add_column(f'{i}', overflow='fold', max_width=100, justify='right', min_width=12)
            # table.add_column("Date", style="dim", width=12)  # 添加表头列
            # table.add_column("Title")
            # table.add_column("Production Budget", justify="right")
            # table.add_column("Box Office", justify="right")
            table.add_row(  # 添加行
                *ps
            )
            table.add_row(
                *[pmap[p] for p in ps]
            )
            console.print(table)
            print('*' * 50)
```


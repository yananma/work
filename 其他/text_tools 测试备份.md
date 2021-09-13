
```python 
from django.core.management import BaseCommand
from data_analysis.models import ZKYCountry
from data_analysis.tools.text_tools import TextFactory, reverse_keyfilter_result, add_tag_from_keyfilter_result

s = '''2020 年 12 月 18 日，上汽通用 ( 沈阳 ) 北盛汽车有限公司生产车间。/ 视觉中国 全球制造业的产业格局正发生显著调整，" 逆全球化 " 暗流涌动、产业价值链呈现 " 缩短 " 态势、发展中国家创新能力提高、人工智能等高科技不断成熟，在种种内外环境变化下，中国制造业面临着新的机遇和挑战。 改革开放以来，巨大的政策优势和卓越的经济活力让我们抓住了全球第三次、第四次产业转移的契机，在 " 世界工厂 "" 中国制造 " 成为国际舞台上属于中国人的闪亮名片后，我们也迎来了从 " 中国制造 " 到 " 中国创造 " 的转型。《重建大陆》等。'''

ss = '来源：证券日报本报记者汪世军“链上星城，链接未来”。5月28日，由国家信息中心和长沙市人民政府共同主办的2021年区块链服务网络（BSN）应用峰会在长沙梅溪湖国际文化艺术中心隆重召开。'


TEXT_COUNTRY_TAG = 'textcountry'
country_keyname = '中国大陆'

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            dest='index',
            default='test-zky',
            help='插入到的ES的索引',
        )

    def handle(self, *args, **options):
        country_indexes = ZKYCountry.get_country_indexes()  # 国家AC自动机索引
        text_country_keyresults = reverse_keyfilter_result(country_indexes.exec_filter(s))

        result_s = add_tag_from_keyfilter_result(s, text_country_keyresults, TEXT_COUNTRY_TAG)
        test_list = [
            # ss,
            # '',
            # 'a',
            # 'aa.',
            # '\t',
            # '\t\t',
            # s,
            # ('(《生态环境部哦哦 哦》)','《'),
            # ('《生态环境部哦哦 哦》','《'),
            # ('《生》','《'),
            # ('《》','《'),
            # ('(《生》)','《'),
            # ('(《》)','《'),
            '<textcountry keyname="美国">美国</textcountry>当地时间5月22日，<textcountry keyname="中国大陆">美国</textcountry>宇航局(NASA)的火星直升机“机智号”完成了第六次飞行，这也是“毅力”号火星任务的第91天。惊险的是，在这次飞行途中，“机智号”遭遇故障，导致飞机在火星10米高空疯狂乱飞近1分钟，所幸最后安全着陆。研究人员称由于导航时间错误，直升机无法判断位置造成乱飞。据报道，“机智号”通过腹部的相机进行导航，后者将图像传输到它的飞行计算机中。但是在飞行大约54秒后，相机在把航行图像传输到飞行计算机过程中出现了一个小故障，丢失了一张图像，导致随后传输的每一张图像都带有错误的时间戳。这使得“机智号”出现上下、左右摇晃，从一侧向另外一侧倾斜了20多度，从而出现大幅颠簸，持续约1分钟。尽管飞行过程惊险，多亏了完善的计划和内置的故障保护装置，“机智号”依旧在目标着陆点的大约5米的范围内安全着陆，证实了系统的健壮性。',
            # ('测试这“句话“对不对好。aa”的”你也好。','不对'),
            # ('测试这“句话“对不对好”的”你也好。', '不对'),
            # ('测试这“句话“对不对。好”的”你也好。', '不对'),
            # ('aaa(a《生态环境部哦哦》)','《'),
            s
        ]
        for it in test_list:
            search_flag = None
            # if isinstance(it,tuple):
            #     it,search_flag = it
            #     print(TextFactory(it).chunk_tag_with_max_size_v2(tag_name=TEXT_COUNTRY_TAG,
            #                                                      search_flag_str=f'<{TEXT_COUNTRY_TAG} {country_keyname}')
            #           .replace_countrytag_to_others(TEXT_COUNTRY_TAG, source_extra_data=country_keyname).now)
            print(TextFactory(it).chunk_tag_with_max_size_v2(tag_name=TEXT_COUNTRY_TAG,search_flag_str=f'<{TEXT_COUNTRY_TAG} keyname="{country_keyname}')
                .replace_countrytag_to_others(TEXT_COUNTRY_TAG, source_extra_data=country_keyname).now)
            # print(TextFactory(it).chunk_tag_with_max_size_v2(search_flag_str="文歧业").now)
```

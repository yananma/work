import logging

from django.core.management.base import BaseCommand

from post.models import lastday, today, ZKYPosts_EN, ZKYHotPosts_EN

from data_analysis.tools.utils import get_logger
logger = get_logger(__file__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            dest='isall',
            action='store_true',
            help='是否导入全部时间段',
        )
        parser.add_argument(
            '-f',
            '--from',
            dest='from_time',
            default=lastday(time_str='08:00:00', to_datetime_str=True),  # 默认从昨天开始
            help='起始时间，格式 yyyy-MM-dd HH:mm:ss',
        )
        parser.add_argument(
            '-t',
            '--to',
            dest='to_time',
            default=today(time_str='08:00:00', to_datetime_str=True),  # 默认今天0点
            help='结束时间，格式 yyyy-MM-dd HH:mm:ss',
        )
        parser.add_argument(
            '-l',
            '--last',
            dest='last_days',
            type=int,
            help='起始日期为距离今天的天数前的日期"',
        )
        pass

    def handle(self, *args, **options):
        # 优先last参数
        if options.get('last_days', None):
            from_date = lastday(options['last_days'], to_datetime_str=True)
            to_date = today(to_datetime_str=True)
        else:
            from_date = options['from_time']
            to_date = options['to_time']

        pre_posts = list(ZKYPosts_EN.objects.filter(post_time__gte=from_date,
                                                    post_time__lt=to_date).values_list('title', 'site_name',
                                                                                       'entry_name',
                                                                                       'url', 'post_time',
                                                                                       'author_name',
                                                                                       'text', 'title_hash'))

        count = 0
        hotposts_titles = [title_hash for title_hash in
                           ZKYHotPosts_EN.objects.filter(post_time__gte=from_date, post_time__lt=to_date).values_list(
                               'md5', flat=True)]
        site_name_list = []
        for post in pre_posts:
            if post[1] not in site_name_list:
                site_name_list.append(post[1])
                result = (post[-1] not in hotposts_titles)
                if result:
                    print(post[0])
                    md5_value = post[-1]
                    _, iscreated = ZKYHotPosts_EN.objects.get_or_create(
                        md5=md5_value,
                        defaults={
                            'title': post[0],
                            'site_name': post[1],
                            'entry_name': post[2],
                            'url': post[3],
                            'post_time': post[4],
                            'author_name': post[5],
                        }
                    )
                    if iscreated:
                        count += 1
                        logger.info('插入了一个')
                        if count == 5:
                            break

        logger.info(f'完成')

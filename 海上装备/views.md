```python
import json
from fractions import Fraction

import more_itertools
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.db import models
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from hszb_backend.except_settings import WEBExceptionManage
from models.models import TaskInfo, TopicModel, EmergingTechTopicModel, RDTENByTopicModel, RDTENByRDTENModel, \
    BurstWordsResults, TopicSimResult, TopicsAuthorResults, TopicsOrganResults, TopicYearCountResult, NormResults, \
    LinkPredictionResults, RDTENProjectExtraModel, TechRDTENProjectRelation, RDTENProjectModel, NAVYExtraModel, \
    NAVYModel
from models.tasks.base import BaseTask
from models.tasks.cluster_task import ClusterTask
from tools.args_warper import arg_warp, TaskInfoArgsWrap
from tools.common import TSValidate, SourceValidate, sucess_response_warp, pager_warp, pager_func


class HotTopicsViewSet(ViewSet):

    @action(methods=['get'], detail=False, url_path='atlas')
    @TaskInfoArgsWrap(ClusterTask)
    def atlas(self, request: Request):
        task_info: TaskInfo = request.task_info
        max_count_topic_node_id = TopicModel.objects.filter(task=task_info).order_by('-document_count').values_list(
            'id', flat=True).first()
        similarity_data = [
            {
                'source': topic_a_sort + 1,
                'target': topic_b_sort + 1,
                'lineStyle': {'width': sim * 10}
            }
            for topic_a_sort, topic_b_sort, sim in TopicSimResult.objects
                .filter(task=task_info)
                .exclude(Q(topic_a_id=max_count_topic_node_id) | Q(topic_b_id=max_count_topic_node_id))
                .values_list('topic_a__sort', 'topic_b__sort', 'sim_num')
        ]
        nodes = list(TopicModel.objects.filter(task=task_info).order_by('sort')
                     .exclude(id=max_count_topic_node_id)
                     .annotate(symbolSize=F('document_count'))
                     .extra(select={'value': "''", 'id': 'sort+1'})
                     .values('id', 'name', 'symbolSize', 'value', 'category'))

        categories = [{'name': f'大类{i + 1}'} for i in range(task_info.args_json['category_num'])]

        return Response({
            'nodes': nodes,
            'links': similarity_data,
            'categories': categories
        })

    @action(methods=['get'], detail=False, url_path='author_and_organ')
    @TaskInfoArgsWrap(ClusterTask)
    @arg_warp('pageSize', arg_type=int, default=10, save_value=True)
    @arg_warp('pageNo', arg_type=int, default=1, save_value=True)
    def author_and_organ(self, request):
        task_info: TaskInfo = request.task_info
        topic_ids = TopicModel.topic_ids(task_info)
        results = pager_func(topic_ids, request.ARGS['pageSize'], request.ARGS['pageNo'])
        topic_name_map = TopicModel.topic_name_map(task_info)
        topics_list = results.pop('data')
        results['children'] = [
            {
                'name': topic_name_map[topic_id],
                'value': TopicModel.objects.filter(id=topic_id).values_list('document_count', flat=True).first(),
                'children': {
                    "author": list(
                        TopicsAuthorResults.objects
                            .filter(topic_id=topic_id)
                            .annotate(name=F('author_name'), value=F('count'))
                            .extra(select={'category': '"专家"'})
                            .values('name', 'value', 'category')
                    ),
                    "organ": list(
                        TopicsOrganResults.objects
                            .filter(topic_id=topic_id)
                            .annotate(name=F('organ_name'), value=F('count'))
                            .extra(select={'category': '"机构"'})
                            .values('name', 'value', 'category')
                    )
                }
            }
            for topic_id in topics_list
        ]
        return Response(results)

    @action(methods=['get'], detail=False, url_path='river')
    @TaskInfoArgsWrap(ClusterTask)
    @arg_warp('pageSize', arg_type=int, default=10, save_value=True)
    @arg_warp('pageNo', arg_type=int, default=1, save_value=True)
    def river(self, request: Request):
        task_info: TaskInfo = request.task_info
        topic_ids = TopicModel.topic_ids(task_info)
        results = pager_func(topic_ids, request.ARGS['pageSize'], request.ARGS['pageNo'])
        topic_name_map = TopicModel.topic_name_map(task_info)
        ids = results.pop('data')
        results.update({
            'legend': {
                'data': [topic_name_map[id] for id in ids]
            },
            'data': [
                [str(year), count, topic__name]
                for year, count, topic__name in
                TopicYearCountResult.objects.filter(topic_id__in=ids).values_list('year', 'count', 'topic__name')
            ]
        })
        return Response(results)

    @action(methods=['get'], detail=False, url_path='front_list')
    @TaskInfoArgsWrap(ClusterTask)
    @arg_warp('pageSize', arg_type=int, default=10, save_value=True)
    @arg_warp('pageNo', arg_type=int, default=1, save_value=True)
    def front_topic_list(self, request):
        task_info: TaskInfo = request.task_info
        return Response({
            'data': [
                {
                    'id': id,
                    'name': name,
                    'sort': sort,
                    'keywords': [keyword_name for keyword_name, _ in json.loads(keywords)],
                    'count': document_count
                }
                for id, name, sort, keywords, document_count in
                TopicModel.objects.filter(task_id=task_info.taskid).order_by('sort').values_list('id', 'name', 'sort',
                                                                                                 'keywords',
                                                                                                 'document_count')
            ]
        })


class TopicViewSet(ViewSet):

    @action(methods=['get'], detail=False, url_path='test')
    def my_test(self, request):
        raise WEBExceptionManage.MY_NO_ARGS_EXP

    @action(methods=['get'], detail=False, url_path='count')
    @TaskInfoArgsWrap(ClusterTask)
    def topic_count(self, request):
        task_info: TaskInfo = request.task_info
        return Response({
            'count': TopicModel.objects.filter(task=task_info).count()
        })

    @action(methods=['get'], detail=False, url_path='list')
    @TaskInfoArgsWrap(ClusterTask)
    def topic_list(self, request):
        task_info: TaskInfo = request.task_info
        return Response({
            'data': [
                {
                    'id': id,
                    'name': name,
                    'sort': sort,
                    'keywords': json.loads(keywords),
                    'task_id': task_id
                }
                for id, name, sort, keywords, task_id in
                TopicModel.objects.filter(task_id=task_info.taskid).order_by('sort').values('id', 'name', 'sort',
                                                                                            'keywords', 'task_id')
            ]
        })

    @action(methods=['post'], detail=False, url_path='update')
    # @TaskInfoArgsWrap(ClusterTask)
    @sucess_response_warp
    @arg_warp('authorid', arg_type=int, save_value=True, default=None, ignore_default_value_apply_func=True)
    @arg_warp('bulk', save_value=True, arg_type=lambda data: json.loads(data) if isinstance(data, str) else data)
    def topic_update(self, request):
        for it in request.ARGS['bulk']:
            topic = TopicModel.objects.get(id=it['id'])
            topic.name = it['name']
            topic.save()
            pass
        return Response({})

    @action(methods=['get'], detail=False, url_path='post/list')
    @TaskInfoArgsWrap(ClusterTask)
    @arg_warp('topicid', arg_type=int, must_have=True, save_value=True)
    @arg_warp('pageSize', arg_type=int, default=10, save_value=True)
    @arg_warp('pageNo', arg_type=int, default=1, save_value=True)
    @pager_warp('data')
    def posts(self, request):
        task_info: TaskInfo = request.task_info
        count_top_n_keywords__data = ClusterTask.load_func_data('count_top_n_keywords', task_instance=task_info,
                                                                model_name=ClusterTask.__name__)
        topicid_to_sort_map = TopicModel.topic_map_reverse(task_info)
        return Response({
            'data': count_top_n_keywords__data['post_topic_ids'][topicid_to_sort_map[request.ARGS['topicid']]]
        })


def edit_year_range(response_data):
    min_year, max_year = float('inf'), float('-inf')
    for it in response_data['data']['data']:
        if it['start'] < min_year:
            min_year = it['start']
        if it['end'] > max_year:
            max_year = it['end']
    response_data['year_range'] = [min_year, max_year]
    return response_data


class EmergingTechTopicViewSet(ViewSet):

    @action(methods=['get'], detail=False, url_path='list')
    @TaskInfoArgsWrap(ClusterTask)
    def topic_list(self, request):
        task_info: TaskInfo = request.task_info
        return Response({
            'data': [
                {
                    'id': it['topic_id'],
                    'name': it['name'],
                    'sort': it['sort'],
                }
                for it in
                EmergingTechTopicModel.objects.filter(task_id=task_info.taskid).order_by('sort').values('topic_id',
                                                                                                        'name', 'sort')
            ]
        })

    @action(methods=['post'], detail=False, url_path='update')
    @TaskInfoArgsWrap(ClusterTask)
    @arg_warp('authorid', arg_type=int, save_value=True, default=None, ignore_default_value_apply_func=True)
    @arg_warp('bulk', save_value=True, arg_type=lambda data: json.loads(data) if isinstance(data, str) else data)
    def topic_update(self, request):
        task_info: TaskInfo = request.task_info
        for it in request.ARGS['bulk']:
            em_tech_topic = EmergingTechTopicModel.objects.filter(task_id=task_info.taskid,
                                                                  sort=int(it['sort'])).first()
            if em_tech_topic is None:
                it['id'] = it['id'] if it['id'] != -1 else None
                em_tech_topic = EmergingTechTopicModel(
                    name=it['name'],
                    sort=int(it['sort']),
                    task_id=task_info.taskid,
                    topic_id=it['id'],
                    author_id=request.ARGS['authorid'],
                )
            else:
                it['id'] = it['id'] if it['id'] != -1 else None
                em_tech_topic.name = it['name']
                em_tech_topic.sort = it['sort']
                em_tech_topic.task_id = task_info.taskid
                em_tech_topic.topic_id = it['id']
                em_tech_topic.author_id = request.ARGS['authorid']
            em_tech_topic.save()
            pass
        return Response({})

    @action(methods=['get'], detail=False, url_path='norm')
    @TaskInfoArgsWrap(ClusterTask)
    @arg_warp('yearRate', save_value=True, default='1/3')
    @arg_warp('oriRate', save_value=True, default='1/3')
    @arg_warp('risRate', save_value=True, default='1/3')
    def norm(self, request):
        task_info: TaskInfo = request.task_info
        topic_ids = TopicModel.topic_ids(task_info)
        year_rate = Fraction(request.ARGS['yearRate'])
        ori_rate = Fraction(request.ARGS['oriRate'])
        ris_rate = Fraction(request.ARGS['risRate'])
        return Response({
            'dimensions': {
                'x': '新颖性',
                'y': '增长性',
                'z': '原创性'
            },
            'data': [
                [['新颖性', '增长性', '原创性', '主题ID', '指标值']]
                +
                list(
                    NormResults.objects
                        .filter(topic_id__in=topic_ids)
                        .order_by('topic__sort')
                        .annotate(rate=F('year_num') * year_rate + F('ori_num') * ori_rate + F('ris_num') * ris_rate)
                        .values_list('year_num', 'ris_num', 'ori_num', 'topic_id', 'rate')
                )
            ]
        })

    @action(methods=['get'], detail=False, url_path='linkpred')
    @TaskInfoArgsWrap(ClusterTask)
    def linkpred(self, request):
        task_info: TaskInfo = request.task_info
        return Response({
            'data': [
                {
                    'topic_a': {
                        'id': topic_a_id,
                        'name': topic_a__name
                    },
                    'topic_b': {
                        'id': topic_b_id,
                        'name': topic_b__name
                    },
                    'sim': sim_num
                }
                for topic_a_id, topic_a__name, topic_b_id, topic_b__name, sim_num in
                LinkPredictionResults.objects
                    .filter(task=task_info)
                    .order_by('-sim_num')
                    .values_list('topic_a_id', 'topic_a__name', 'topic_b_id', 'topic_b__name', 'sim_num')
            ]
        })

    @action(methods=['get'], detail=False, url_path='burst')
    @TaskInfoArgsWrap(ClusterTask)
    @arg_warp('pageSize', arg_type=int, default=20, save_value=True)
    @arg_warp('pageNo', arg_type=int, default=1, save_value=True)
    @pager_warp('data', final_func=edit_year_range)
    def burst(self, request):
        task_info: TaskInfo = request.task_info
        document_tokenizer_combine__data = ClusterTask.load_func_data('document_tokenizer_combine',
                                                                      task_instance=task_info,
                                                                      model_name=ClusterTask.__name__)
        return Response({
            'year_range': [document_tokenizer_combine__data['year_range'][0],
                           document_tokenizer_combine__data['year_range'][1] - 1],
            'data': BurstWordsResults.objects.filter(task=task_info, end__gte=F('start')).order_by('-weight').annotate(
                length=(F('end') - F('start') + 1)).values('word', 'start', 'end', 'length', 'weight')
        })


class RDTENViewSet(ViewSet):
    @action(methods=['get'], detail=False, url_path='list')
    @TaskInfoArgsWrap(ClusterTask)
    def rdten_list(self, request):
        task_info: TaskInfo = request.task_info
        return Response({
            'data': [
                dict(
                    row_map,
                    topics=list(
                        RDTENProjectExtraModel.objects
                            .filter(document__id=row_map['id'])
                            .order_by('-topics__rdtenprojectextratotopicmodel__sim', 'topics__sort')
                            .annotate(name=F('topics__name'))
                            .annotate(value=F('topics__rdtenprojectextratotopicmodel__sim'))
                            .values('name', 'value')
                    )
                )
                for row_map in
                RDTENProjectModel.objects
                    .filter(techrdtenprojectrelation__tech=task_info.ts)
                    .order_by('program_code', 'code')
                    .annotate(
                    next_five_years=F('total_budget') + F('budget_fy1') + F('budget_fy2') + F('budget_fy3') + F(
                        'budget_fy4'))
                    .annotate(program_name=F('program__name'))
                    .values('program_code', 'program_name', 'id', 'name', 'fiscal_year', 'total_budget',
                            'next_five_years')
            ]
        })

    @action(methods=['get'], detail=False, url_path='by_topic')
    @TaskInfoArgsWrap(ClusterTask)
    def by_topic(self, request):
        task_info: TaskInfo = request.task_info
        return Response({
            'data': list(
                RDTENByTopicModel.objects.filter(ts=task_info).annotate(topic_name=F('topic__name')).values('topic_id',
                                                                                                            'topic_name',
                                                                                                            'year',
                                                                                                            'count',
                                                                                                            'money')
            )
        })

    @action(methods=['get'], detail=False, url_path='by_rdten')
    @TaskInfoArgsWrap(ClusterTask)
    def by_rdten(self, request):
        task_info: TaskInfo = request.task_info
        return Response({
            'data': list(
                RDTENByRDTENModel.objects.filter(ts=task_info).annotate(rdten_name=F('rdten__document__name')).values(
                    'rdten_id', 'rdten_name', 'year', 'count', 'money')
            )
        })


class NAVYViewSet(ViewSet):
    @action(methods=['get'], detail=False, url_path='list')
    @TaskInfoArgsWrap(ClusterTask)
    def navy_list(self, request):
        task_info: TaskInfo = request.task_info
        return Response({
            'data': [
                dict(
                    row_map,
                    topics=list(
                        NAVYExtraModel.objects
                            .filter(document__id=row_map['id'])
                            .order_by('-topics__navyextratotopicmodel__sim', 'topics__sort')
                            .annotate(name=F('topics__name'))
                            .annotate(value=F('topics__navyextratotopicmodel__sim'))
                            .values('name', 'value')
                    )
                )
                for row_map in
                NAVYModel.objects
                    .filter(technavyrelation__tech=task_info.ts)
                    .order_by('create_time')
                    .values('id', 'two_title', 'three_title', 'four_title')
            ]
        })


```

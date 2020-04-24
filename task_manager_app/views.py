import json
import django
import datetime
from rest_framework.decorators import api_view
from django.http import HttpResponse
from .models import (
    Department,
    Role,
    User,
    UserRole,
    Priority,
    Task,
    TrackerRoadmap,
    TrackerRoadmapTask
)
from .validators import (
    Validation
)
from .helper import (
    error_handler,
    new_psw,
    check_valid_limit_and_offset,
    tag_grouping,
    query_string_filters
)
from .serializers import (
    PrioritySerializer,
    DepartmentSerializer,
    RoleSerializer,
    TrackedRoadmapSerializer,
    TrackedRoadmapTaskSerializer,
    UserSerializer
)


# @api_view(['POST'])
# def login(request):
#     body = request.data
#     if not Validation.login_validation(data=body):
#         return error_handler(error_status=400, message=f'Wrong data!')
#     user = User.get_user_by_username(username=body['username'])
#     if not user:
#         return error_handler(error_status=404, message='User not found!')
#     if user.blocked:
#         return error_handler(error_status=403, message='User has blocked!')
#     if user.password != new_psw(salt=user.salt, password=body['password']):
#         return error_handler(error_status=403, message='User or password is wrong!')
#     token = user.security_token()
#     user = UserSerializer(many=False, instance=user).data
#     user['token'] = token
#     return HttpResponse(
#         json.dumps(
#             {
#                 'status': f'OK',
#                 'code': 200,
#                 'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
#                 'message': f'User is successfully logged!',
#                 'result': user
#             }
#         ),
#         content_type='application/json',
#         status=200
#     )


@api_view(['GET'])
def get_priorities(request):
    """
    This method will get all priorities
    :param request:
    :return: list of priorities
    """
    priorities = Priority.get_all_priorities()
    priorities = PrioritySerializer(many=True, instance=priorities).data
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Priorities',
                'results': priorities
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_departments(request):
    """
    This method will get all departments
    :param request:
    :return: list of departments
    """
    departments = Department.get_all_departments()
    departments = DepartmentSerializer(many=True, instance=departments).data
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Departments',
                'results': departments
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_roles(request):
    """
    This method will get all roles
    :param request:
    :return: list of roles
    """
    query_string = request.GET
    filters = query_string_filters(query_string)
    roles = Role.get_all_roles(data=query_string, filters=filters)
    roles = RoleSerializer(many=True, instance=roles).data
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Roles',
                'results': roles
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_tracked_roadmaps(request):
    """
    This method will get all tracked road maps
    :param request:
    :return: list of tracked road maps
    """
    tracked_roadmaps = TrackerRoadmap.get_all_tracker_roadmap()
    tracked_roadmaps = TrackedRoadmapSerializer(many=True, instance=tracked_roadmaps).data
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Tracked roadmaps',
                'results': tracked_roadmaps
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_tracker_roadmap_tasks_by_id_tracker_roadmap_id(request, tracker_roadmap_id):
    """
    This method will get all tasks from chosen tracker road maps
    :param request:
    :param tracker_roadmap_id:
    :return: list of tasks
    """
    query_string = request.GET
    filters = query_string_filters(query_string)
    tracked_roadmap_tasks = TrackerRoadmapTask.get_tracker_roadmap_tasks_by_tracker_roadmap_id(
        tracker_roadmap_id=tracker_roadmap_id,
        data=query_string,
        filters=filters
    )
    tracked_roadmap_tasks = TrackedRoadmapTaskSerializer(many=True, instance=tracked_roadmap_tasks).data
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Tracked roadmap tasks',
                'results': tracked_roadmap_tasks
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['GET'])
def get_assigned_users(request):
    """
    This method will get all users that are assigned on tasks
    :param request:
    :return: list of users
    """
    query_string = request.GET
    filters = query_string_filters(query_string)
    assigned_users = Task.get_assigned_users(data=query_string, filters=filters)
    assigned_users = UserSerializer(many=True, instance=assigned_users).data
    return HttpResponse(
        json.dumps(
            {
                'status': f'OK',
                'code': 200,
                'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'message': f'Assigned users',
                'results': assigned_users
            }
        ),
        content_type='application/json',
        status=200
    )


@api_view(['POST'])
def edit_task(request, task_id):
    """
    This method will edit task by id
    :param request:
    :param task_id:
    :param body {'title': str, 'percent': int, 'estimate': int, 'priority_id': int, 'department_id': int, 'role_id': int
    'tracker_roadmap': int, 'assigned_to': int, 'content': str, 'start_date': string, 'end_date': string}
    :return:
    """
    body = request.data
    if not Validation.edit_task(data=body):
        return error_handler(error_status=400, message=f'Wrong data!')



# @api_view(['GET'])
# def get_image(request, id):
#     try:
#         int(id)
#     except ValueError as ex:
#         print(ex)
#         return error_handler(error_status=400, message='Bad data!')
#     image = Image.get_image_by_unique_id(id=id)
#     if not image:
#         return error_handler(error_status=404, message=f'Not found!')
#     image.increase_views()
#     comments = ImageComment.get_comments_by_image_id(image_id=image.id)
#     image = ImageSerializer(many=False, instance=image).data
#     comments = ImageCommentSerializer(many=True, instance=comments).data
#     image['comments'] = comments
#     return HttpResponse(
#         json.dumps(
#             {
#                 'status': f'OK',
#                 'code': 200,
#                 'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
#                 'message': f'Image',
#                 'result': image
#             }
#         ),
#         content_type='application/json',
#         status=200
#     )
#
#
# @api_view(['GET'])
# def get_next_image(request, id):
#     try:
#         int(id)
#     except ValueError as ex:
#         print(ex)
#         return error_handler(error_status=400, message='Bad data!')
#     image = Image.get_image_by_unique_id(id=id)
#     if not image:
#         return error_handler(error_status=404, message=f'Not found!')
#     next_image = Image.get_next_image(image_id=image.id)
#     if not next_image:
#         return error_handler(error_status=404, message=f'Not found!')
#     next_image.increase_views()
#     comments = ImageComment.get_comments_by_image_id(image_id=next_image.id)
#     next_image = ImageSerializer(many=False, instance=next_image).data
#     comments = ImageCommentSerializer(many=True, instance=comments).data
#     next_image['comments'] = comments
#     return HttpResponse(
#         json.dumps(
#             {
#                 'status': f'OK',
#                 'code': 200,
#                 'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
#                 'message': f'Image',
#                 'result': next_image
#             }
#         ),
#         content_type='application/json',
#         status=200
#     )
#
#
# @api_view(['GET'])
# def get_previous_image(request, id):
#     try:
#         int(id)
#     except ValueError as ex:
#         print(ex)
#         return error_handler(error_status=400, message='Bad data!')
#     image = Image.get_image_by_unique_id(id=id)
#     if not image:
#         return error_handler(error_status=404, message=f'Not found!')
#     next_image = Image.get_previous_image(image_id=image.id)
#     if not next_image:
#         return error_handler(error_status=404, message=f'Not found!')
#     next_image.increase_views()
#     comments = ImageComment.get_comments_by_image_id(image_id=next_image.id)
#     next_image = ImageSerializer(many=False, instance=next_image).data
#     comments = ImageCommentSerializer(many=True, instance=comments).data
#     next_image['comments'] = comments
#     return HttpResponse(
#         json.dumps(
#             {
#                 'status': f'OK',
#                 'code': 200,
#                 'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
#                 'message': f'Image',
#                 'result': next_image
#             }
#         ),
#         content_type='application/json',
#         status=200
#     )
#
#
# @api_view(['GET'])
# def get_home_posts(request):
#     posts = Post.get_home_posts()
#     posts = PostSerializer(many=True, instance=posts).data
#     for post in posts:
#         post['content'] = post['content'].replace('\r', '')
#         post['content'] = post['content'][:1555] + '...'
#         res = tag_grouping(post['content'], True)
#         post['content'] = res
#         date = post['created'].split('T')[0].split('-')
#         date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
#         post['created'] = date.strftime("%b %d %Y")
#     return HttpResponse(
#         json.dumps(
#             {
#                 'status': f'OK',
#                 'code': 200,
#                 'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
#                 'message': f'Posts',
#                 'results': posts
#             }
#         ),
#         content_type='application/json',
#         status=200
#     )
#
#
# @api_view(['GET'])
# def get_posts(request):
#     query_string = request.GET
#     limit = query_string['limit'] if 'limit' in query_string else None
#     offset = query_string['offset'] if 'offset' in query_string else None
#     limit, offset = check_valid_limit_and_offset(limit=limit, offset=offset)
#     posts = Post.get_posts(offset=offset, limit=limit)
#     posts_number = Post.count_posts()
#     posts = PostSerializer(many=True, instance=posts).data
#     for post in posts:
#         post['content'] = post['content'].replace('\r', '')
#         post['content'] = post['content'][:1555] + '...'
#         res = tag_grouping(post['content'], True)
#         post['content'] = res
#         date = post['created'].split('T')[0].split('-')
#         date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
#         post['created'] = date.strftime("%b %d %Y")
#         post['posts_number'] = posts_number
#     return HttpResponse(
#         json.dumps(
#             {
#                 'status': f'OK',
#                 'code': 200,
#                 'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
#                 'message': f'Posts',
#                 'results': posts
#             }
#         ),
#         content_type='application/json',
#         status=200
#     )
#
#
# @api_view(['GET'])
# def get_post(request, id):
#     try:
#         int(id)
#     except ValueError as ex:
#         print(ex)
#         return error_handler(error_status=400, message='Bad data!')
#     post = Post.get_post_by_unique_id(id=id)
#     if not post:
#         return error_handler(error_status=404, message=f'Not found')
#     post.increase_views()
#     comments = PostComment.get_comments_by_post_id(post_id=post.id)
#     post = PostSerializer(many=False, instance=post).data
#     date = post['created'].split('T')[0].split('-')
#     date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
#     post['created'] = date.strftime("%b %d %Y")
#     res = tag_grouping(post['content'], True)
#     post['content'] = res
#     comments = PostCommentSerializer(many=True, instance=comments).data
#     post['comments'] = comments
#     for i in post['content']:
#         print(i)
#     return HttpResponse(
#         json.dumps(
#             {
#                 'status': f'OK',
#                 'code': 200,
#                 'server_time': django.utils.timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
#                 'message': f'Image',
#                 'result': post
#             }
#         ),
#         content_type='application/json',
#         status=200
#     )

from rest_framework import serializers
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


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'created',
            'username',
            'email',
            'first_name',
            'last_name',
            'activated'
        ]


class PrioritySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Priority
        fields = [
            'id',
            'created',
            'name',
            'color'
        ]


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Department
        fields = [
            'id',
            'created',
            'name',
        ]


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    department = DepartmentSerializer(many=False)

    class Meta:
        model = Role
        fields = [
            'id',
            'created',
            'name',
            'department'
        ]


class TrackedRoadmapSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TrackerRoadmap
        fields = [
            'id',
            'created',
            'position',
            'name'
        ]


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    priority = PrioritySerializer(many=False)
    department = DepartmentSerializer(many=False)
    role = RoleSerializer(many=False)
    created_by = UserSerializer(many=False)
    assigned_to = UserSerializer(many=False)
    next_assigned_user = UserSerializer(many=False)

    class Meta:
        model = Task
        fields = [
            'id',
            'created',
            'title',
            'content',
            'start_date',
            'end_date',
            'estimate',
            'percent',
            'priority',
            'department',
            'role',
            'created_by',
            'assigned_to',
            'next_assigned_user'
        ]


class TrackedRoadmapTaskSerializer(serializers.HyperlinkedModelSerializer):
    tracker_roadmap = TrackedRoadmapSerializer(many=False)
    task = TaskSerializer(many=False)

    class Meta:
        model = TrackerRoadmapTask
        fields = [
            'id',
            'created',
            'position',
            'tracker_roadmap',
            'task'
        ]

# class RoleSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Role
#         fields = [
#             'id',
#             'name'
#         ]
#
#
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     role = RoleSerializer(many=False)
#
#     class Meta:
#         model = User
#         fields = [
#             'id',
#             'user_name',
#             'email',
#             'activated',
#             'newsletter',
#             'role',
#         ]
#
#
# class ImageSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = Image
#         fields = [
#             'id',
#             'created',
#             'google_drive_link',
#             'description',
#             'comment',
#             'views',
#             'likes',
#             'type',
#             'path',
#             'uniqueId'
#         ]
#
#
# class ImageCommentSerializer(serializers.HyperlinkedModelSerializer):
#     user = UserSerializer(many=False)
#     image = ImageSerializer(many=False)
#
#     class Meta:
#         model = ImageComment
#         fields = [
#             'id',
#             'created',
#             'content',
#             'approved',
#             'user',
#             'image',
#         ]
#
#
# class PostSerializer(serializers.HyperlinkedModelSerializer):
#     image = ImageSerializer(many=False)
#
#     class Meta:
#         model = Post
#         fields = [
#             'id',
#             'created',
#             'edited',
#             'title',
#             'content',
#             'comment',
#             'views',
#             'image',
#             'uniqueId'
#         ]
#
#
# class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
#     user = UserSerializer(many=False)
#     post = PostSerializer(many=False)
#
#     class Meta:
#         model = ImageComment
#         fields = [
#             'id',
#             'created',
#             'content',
#             'approved',
#             'user',
#             'post',
#         ]

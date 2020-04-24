import random
import string
from datetime import (
    datetime,
    timedelta
)
import uuid
import django
from django.db import models
from django.db.models import Q
from django.core.validators import ValidationError
from django.core.mail import send_mail
from jose import jwt
from .helper import (
    new_salt,
    new_psw
)
from .constants import (
    secret_key_word
)


class Department(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    name = models.CharField(
        max_length=256,
        unique=True
    )

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def get_all_departments():
        return Department.objects.filter().all()


class Role(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    name = models.CharField(
        max_length=256
    )

    # Relationships

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('name', 'department')

    def __str__(self):
        return f'{self.name} ({self.department.name})'

    @staticmethod
    def get_all_roles(data, filters=None):
        department_id = None
        if 'department_id' in filters:
            if int(data['department_id'][0]) != 0:
                department_id = data['department_id'][0]
        roles = Role.objects.filter()
        if department_id:
            roles = roles.filter(department_id=department_id)
        return roles.order_by('id').all()

    @staticmethod
    def get_all_roles_by_department_id(department_id):
        return Role.objects.filter(department_id=department_id).order_by('id').all()


class User(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    username = models.CharField(
        max_length=256,
        unique=True,
    )
    email = models.EmailField(
        max_length=256,
        unique=True
    )
    first_name = models.CharField(
        max_length=256
    )
    last_name = models.CharField(
        max_length=256
    )
    activated = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f'{self.username} ({self.email})'

    # def save(self, *args, **kwargs):
    #     """
    #     This method is override of main method!
    #     """
    #     if self.admin_password:
    #         if not User.password_strength(self.admin_password):
    #             raise ValueError(f'Password is not valid!')
    #         self.password = new_psw(self.salt, self.admin_password)
    #         self.admin_password = None
    #     super(User, self).save(*args, **kwargs)

    # @staticmethod
    # def password_strength(password):
    #     """
    #     This method will check the password strength.
    #     The password need have at least 8 symbols and less than 26 symbols.
    #     The password need have at least one digit, at least one upper character, at least one lower character and
    #     at least one special symbol. The password checking will stop when the all conditions are True, no need to check
    #     the whole password, only if the last symbol ist one of the condition.
    #     :return: True or False
    #     """
    #     is_lower = False
    #     is_upper = False
    #     is_digit = False
    #     is_special_character = False
    #     spec = "@#$%^&+=.!/?*-"
    #     if not password:
    #         return False
    #     if (len(password) < 8) and (len(password) > 25):
    #         return False
    #     for let in password:
    #         try:
    #             let = int(let)
    #             is_digit = True
    #         except Exception as ex:
    #             # print(ex)
    #             if let in spec:
    #                 is_special_character = True
    #             if let.isalpha() and let == let.upper():
    #                 is_upper = True
    #             if let.isalpha() and let == let.lower():
    #                 is_lower = True
    #         if is_digit and is_special_character and is_upper and is_lower:
    #             return True
    #     return False

    # def security_token(self):
    #     signed = jwt.encode(
    #         {'email': f'{self.email}',
    #          'username': f'{self.user_name}',
    #          'role': f'{self.role.name}',
    #          'user_id': self.id
    #          }, secret_key_word, algorithm='HS256')
    #     return signed


class UserRole(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)

    # Relationships

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user_id', 'role_id')

    def __str__(self):
        return f'{self.user.username} ({self.role.name}, {self.role.department.name})'


class Priority(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    name = models.CharField(
        max_length=256,
        unique=True
    )
    color = models.CharField(
        max_length=7
    )

    def __str__(self):
        return f'{self.name} ({self.color})'

    @staticmethod
    def get_all_priorities():
        return Priority.objects.filter().all()


class Task(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    title = models.CharField(
        max_length=256
    )
    content = models.TextField(
        max_length=10000
    )
    start_date = models.DateField(
        null=True,
        blank=True
    )
    end_date = models.DateField(
        null=True,
        blank=True
    )
    estimate = models.FloatField()
    percent = models.FloatField()

    # Relationships

    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_by'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_to'
    )
    next_assigned_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='next_assigned_user',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.title} ({self.assigned_to.username})'

    @staticmethod
    def get_assigned_users(data, filters=None):
        role_id = None
        if 'role_id' in filters:
            if int(data['role_id'][0]) != 0:
                role_id = data['role_id'][0]
        tasks = Task.objects.filter()
        if role_id:
            tasks = tasks.filter(assigned_to__userrole__role_id=role_id)
        tasks = tasks.order_by('-id').all()
        users = list(set([t.assigned_to for t in tasks]))
        return users


class TrackerRoadmap(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    position = models.IntegerField(
        unique=True
    )
    name = models.CharField(
        max_length=256,
        unique=True
    )

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def get_all_tracker_roadmap():
        return TrackerRoadmap.objects.filter().order_by('position').all()

    @staticmethod
    def get_tracker_roadmap_by_id(tracker_roadmap_id):
        return TrackerRoadmap.objects.filter(id=tracker_roadmap_id).first()

    # def save(self, *args, **kwargs):
    #     if self.id:
    #         edit_tracker_roadmap_id = TrackerRoadmap.get_tracker_roadmap_by_id(tracker_roadmap_id=self.id)
    #         if self.position != edit_tracker_roadmap_id.position:


class TrackerRoadmapTask(models.Model):
    created = models.DateTimeField(default=django.utils.timezone.now)
    position = models.IntegerField(
    )
    # Relationships

    tracker_roadmap = models.ForeignKey(
        TrackerRoadmap,
        on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.tracker_roadmap.name} ({self.task.title}, {self.position})'

    class Meta:
        unique_together = ('task', 'tracker_roadmap')

    @staticmethod
    def get_tracker_roadmap_tasks_by_tracker_roadmap_id(tracker_roadmap_id, data, filters=None):
        department_id = None
        role_id = None
        assigned_to_id = None
        priority_id = None
        if 'department_id' in filters:
            if int(data['department_id'][0]) != 0:
                department_id = int(data['department_id'][0])
        if 'role_id' in filters:
            if int(data['role_id'][0]) != 0:
                role_id = int(data['role_id'][0])
        if 'assigned_to_id' in filters:
            if int(data['assigned_to_id'][0]) != 0:
                assigned_to_id = int(data['assigned_to_id'][0])
        if 'priority_id' in filters:
            if int(data['priority_id'][0]) != 0:
                priority_id = int(data['priority_id'][0])
        tasks = Task.objects.filter()
        if priority_id:
            tasks = tasks.filter(priority_id=priority_id)
        if department_id:
            tasks = tasks.filter(department_id=department_id)
        if role_id:
            tasks = tasks.filter(role_id=role_id)
        if assigned_to_id:
            tasks = tasks.filter(assigned_to=assigned_to_id)
        tasks = tasks.all()
        task_ids = []
        if department_id or role_id or assigned_to_id or priority_id:
            if tasks:
                task_ids = list(set([task.id for task in tasks]))
            else:
                task_ids = [0]
        tracked_roadmap_tasks = TrackerRoadmapTask.objects.filter()
        if tracker_roadmap_id < 1:
            if task_ids:
                tracked_roadmap_tasks = tracked_roadmap_tasks.filter(task_id__in=task_ids)
            tracked_roadmap_tasks = tracked_roadmap_tasks.order_by('-id').all()
            return tracked_roadmap_tasks
        tracked_roadmap_tasks = tracked_roadmap_tasks.filter(tracker_roadmap_id=tracker_roadmap_id)
        if task_ids:
            tracked_roadmap_tasks = tracked_roadmap_tasks.filter(task_id__in=task_ids)
        tracked_roadmap_tasks = tracked_roadmap_tasks.order_by('-id').all()
        return tracked_roadmap_tasks

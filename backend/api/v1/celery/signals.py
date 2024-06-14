"""
    config.schedulers에 CustomDatabaseScheduler 적용으로 아래 로직이 필요없어진다.
"""

# from django.db.models.signals import pre_save
# from django.dispatch import receiver

# from django_celery_beat.models import (
#     PeriodicTask,
#     CrontabSchedule,
#     IntervalSchedule,
#     ClockedSchedule,
# )


# @receiver(pre_save, sender=CrontabSchedule)
# def crontab_schedule_pre_save(sender, instance, **kwargs):
#     PeriodicTask.objects.update(last_run_at=None)


# @receiver(pre_save, sender=IntervalSchedule)
# def interval_schedule_pre_save(sender, instance, **kwargs):
#     PeriodicTask.objects.update(last_run_at=None)


# @receiver(pre_save, sender=ClockedSchedule)
# def clocked_schedule_pre_save(sender, instance, **kwargs):
#     PeriodicTask.objects.update(last_run_at=None)


# @receiver(pre_save, sender=PeriodicTask)
# def periodic_task_pre_save(sender, instance, **kwargs):
#     is_need_init = False

#     try:
#         old_instance = PeriodicTask.objects.get(id=instance.pk)
#     except Exception as e:
#         is_need_init = True
#     else:
#         if instance.name != old_instance.name:
#             is_need_init = True
#         elif instance.task != old_instance.task:
#             is_need_init = True
#         elif instance.interval_id != old_instance.interval_id:
#             is_need_init = True
#         elif instance.crontab_id != old_instance.crontab_id:
#             is_need_init = True
#         elif instance.solar_id != old_instance.solar_id:
#             is_need_init = True
#         elif instance.clocked_id != old_instance.clocked_id:
#             is_need_init = True
#         elif instance.priority != old_instance.priority:
#             is_need_init = True
#         elif instance.one_off != old_instance.one_off:
#             is_need_init = True
#         elif instance.start_time != old_instance.start_time:
#             is_need_init = True
#         elif instance.enabled != old_instance.enabled:
#             is_need_init = True
#         elif instance.expire_seconds != old_instance.expire_seconds:
#             is_need_init = True
#         elif instance.args != old_instance.args:
#             is_need_init = True
#         elif instance.kwargs != old_instance.kwargs:
#             is_need_init = True

#     if is_need_init:
#         PeriodicTask.objects.update(last_run_at=None)

from django.db import models
from uuid import uuid4

from django.urls import reverse


class Group(models.Model):
    """The group model where multiple users can share and discuss ideas"""

    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"Group {self.name}-{self.uuid}"

    def get_absolute_url(self):
        return reverse("group", args=[str(self.uuid)])

    def add_user_to_group(self, user):
        """A helper function to add a user to a group and create an event object"""
        self.members.add(user)
        self.event_set.create(type="Join", user=user)
        self.save()

    def remove_user_from_group(self, user):
        """An helper function to remove users from group members when they \
        leave the group and create an event for the timestamp the user left the group"""
        self.members.remove(user)
        self.event_set.create(type="Left", user=user)
        self.save()


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self) -> str:
        date = self.timestamp.date()
        time = self.timestamp.time()
        return f"{self.author}:- {self.content} @{date} {time.hour}:{time.minute}"


class Event(models.Model):
    """
    A model that holds all events related to a group like when a user joins the group or leaves.
    """

    CHOICES = [("Join", "join"), ("Left", "left")]
    type = models.CharField(choices=CHOICES, max_length=10)
    description = models.CharField(
        help_text="A description of the event that occurred",
        max_length=50,
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.description = f"{self.user} {self.type} the {self.group.name} group"
        super().save(*args, kwargs)

    def __str__(self) -> str:
        return f"{self.description}"

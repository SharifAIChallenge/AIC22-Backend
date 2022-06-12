from django.db import models
from model_utils.models import TimeStampedModel

from account.models import User
from constants import SHORT_TEXT_MAX_LENGTH


class TicketStatus:
    OPEN = 'open'
    CLOSED = 'closed'

    TYPES = (
        (OPEN, OPEN),
        (CLOSED, CLOSED),
    )


class ReplyStatus:
    PENDING = 'pending'
    ANSWERED = 'answered'

    TYPES = (
        (PENDING, PENDING),
        (ANSWERED, ANSWERED),
    )


class Ticket(TimeStampedModel):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='tickets'
    )

    tag = models.ForeignKey(
        to='communication.Tag',
        related_name='tickets',
        on_delete=models.DO_NOTHING
    )
    title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    text = models.TextField()

    is_public = models.BooleanField(default=False)

    status = models.CharField(
        max_length=SHORT_TEXT_MAX_LENGTH,
        default=TicketStatus.OPEN,
        choices=TicketStatus.TYPES
    )

    def __str__(self):
        return f'{self.title} {self.author.username}'


class Reply(TimeStampedModel):
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ticket_replies'
    )
    text = models.TextField()

    status = models.CharField(
        max_length=SHORT_TEXT_MAX_LENGTH,
        default=ReplyStatus.PENDING,
        choices=ReplyStatus.TYPES
    )

    def __str__(self):
        return f'{self.user}'


class Tag(TimeStampedModel):
    title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)

    def __str__(self):
        return f'{self.title}'

from django.contrib.auth import get_user_model
from django.db import models

from model_utils.models import TimeStampedModel, UUIDModel, SoftDeletableModel

from team.models import Team

User = get_user_model()


class PaymentRequest(TimeStampedModel, UUIDModel, SoftDeletableModel):
    amount = models.PositiveIntegerField(default=100000)
    description = models.TextField(
        default='پرداخت مرحله اول ای آی چلنج ۲۲'
    )

    user = models.ForeignKey(
        User,
        related_name='payment_requests',
        on_delete=models.DO_NOTHING
    )
    callback_url = models.URLField(default='https://api.aichallenge.ir/api/v1/payment/callback')

    team_name = models.CharField(
        max_length=128
    )
    authority = models.CharField(max_length=128, blank=True, null=True)
    ref_id = models.CharField(max_length=64, blank=True, null=True)

    def get_team(self):
        return Team.objects.filter(name=self.team_name).last()


class PaymentConfig(TimeStampedModel, UUIDModel):
    amount = models.PositiveIntegerField(default=100000)
    description = models.TextField()

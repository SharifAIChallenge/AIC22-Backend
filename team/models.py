from django.db import models

from constants import SHORT_TEXT_MAX_LENGTH, TEAM_MAX_MEMBERS
from account.models import User


class Team(models.Model):
    name = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, unique=True)
    image = models.ImageField(upload_to='team_images', null=True, blank=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='created_team')

    def is_complete(self):
        return self.members.count() == TEAM_MAX_MEMBERS

    def reject_all_pending_invitations(self):
        invitations = self.invitations.filter(status="pending")
        invitations.update(status="rejected")

    def __str__(self):
        return str(self.name)


class InvitationTypes:
    TEAM_TO_USER = 'team_to_user'
    USER_TO_TEAM = 'user_to_team'

    TYPES = (
        (TEAM_TO_USER, 'Team to User invitation'),
        (USER_TO_TEAM, 'User to Team invitation')
    )


class InvitationStatusTypes:
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    TYPES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected')
    )


class Invitation(models.Model):  # maybe TimeStampedModel
    user = models.ForeignKey(to=User, related_name='invitations', on_delete=models.CASCADE)
    team = models.ForeignKey(to=Team, related_name='invitations', on_delete=models.CASCADE)
    type = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, choices=InvitationTypes.TYPES)
    status = models.CharField(
        max_length=SHORT_TEXT_MAX_LENGTH,
        choices=InvitationStatusTypes.TYPES,
        default=InvitationStatusTypes.PENDING
    )

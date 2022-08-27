from django.db import models

from constants import SHORT_TEXT_MAX_LENGTH, TEAM_MAX_MEMBERS
from account.models import User


class NotBotQueryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_bot=False)


class BotQueryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_bot=True)


class Team(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, unique=True)
    image = models.ImageField(upload_to='team_images', null=True, blank=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='created_team')
    is_finalist = models.BooleanField(default=False)
    MAX_BOT_NUMBER = 5
    humans = NotBotQueryManager()
    bots = BotQueryManager()

    is_bot = models.BooleanField(
        default=False
    )
    bot_number = models.PositiveSmallIntegerField(
        unique=True,
        blank=True,
        null=True
    )
    final_payed = models.BooleanField(default=False)

    @staticmethod
    def get_next_level_bot(team):
        bots = Team.bots.all().order_by('bot_number')
        next_bot = None
        for bot in bots:
            if not bot.has_won_me(team):
                next_bot = bot
                break

        return next_bot

    def is_complete(self):
        return self.members.count() == TEAM_MAX_MEMBERS

    def has_final_submission(self):
        return self.submissions.filter(is_final=True).first() is not None

    def final_submission(self):
        return self.submissions.filter(is_final=True).first()

    def rival_teams_wins(self):
        as_second_teams = self.matches_first.exclude(winner=None).exclude(
            winner=self).values_list(
            'team2_id', flat=True
        )
        as_first_teams = self.matches_second.exclude(winner=None).exclude(winner=self).values_list(
            'team1_id', flat=True
        )
        return list(as_first_teams) + list(as_second_teams)

    def has_won_me(self, team):
        as_second_teams = self.matches_first.filter(winner=team).exists()
        as_first_teams = self.matches_second.filter(winner=team).exists()

        return as_second_teams or as_first_teams

    def has_match_with_me(self, team, tournament):
        as_second_teams = self.matches_first.filter(
            team2=team,
            tournament=tournament
        ).exists()
        as_first_teams = self.matches_second.filter(
            team1=team,
            tournament=tournament
        ).exists()

        return as_second_teams or as_first_teams

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

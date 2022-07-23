import os
import uuid
import logging

from django.db import models
from django.shortcuts import get_object_or_404

from team.models import Team
from account.models import User
from constants import SHORT_TEXT_MAX_LENGTH, MEDIUM_TEXT_MAX_LENGTH, LONG_TEXT_MAX_LENGTH

logger = logging.getLogger(__name__)


class SubmissionLanguagesTypes:
    CPP = 'cpp'
    JAVA = 'java'
    PYTHON3 = 'python 3'

    TYPES = (
        (CPP, 'C++'),
        (JAVA, 'Java'),
        (PYTHON3, 'Python 3'),
    )


class SubmissionStatusTypes:
    UPLOADING = 'uploading'
    UPLOADED = 'uploaded'
    COMPILING = 'compiling'
    COMPILED = 'compiled'
    FAILED = 'failed'

    TYPES = (
        (UPLOADING, 'Uploading'),
        (UPLOADED, 'Uploaded'),
        (COMPILING, 'Compiling'),
        (COMPILED, 'Compiled'),
        (FAILED, 'Failed')
    )


def get_submission_file_directory(instance, filename):
    return os.path.join(
        instance.team.name,
        str(instance.user.id),
        filename + uuid.uuid4().__str__() + '.zip'
    )


class Submission(models.Model):
    team = models.ForeignKey(
        Team,
        related_name='submissions',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='submissions',
        on_delete=models.CASCADE
    )
    language = models.CharField(
        max_length=SHORT_TEXT_MAX_LENGTH,
        choices=SubmissionLanguagesTypes.TYPES
    )
    file = models.FileField(
        upload_to=get_submission_file_directory, null=True,
        blank=True
    )
    submit_time = models.DateTimeField(auto_now_add=True)
    is_final = models.BooleanField(default=False)
    status = models.CharField(
        max_length=SHORT_TEXT_MAX_LENGTH,
        choices=SubmissionStatusTypes.TYPES,
        default=SubmissionStatusTypes.UPLOADING
    )

    infra_compile_message = models.CharField(max_length=LONG_TEXT_MAX_LENGTH, null=True, blank=True)
    infra_token = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH, null=True, blank=True, unique=True)
    infra_compile_token = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH, null=True, blank=True, unique=True)

    is_mini_game = models.BooleanField(default=False)
    is_mini_game_final = models.BooleanField(default=False)

    def post_save(self):
        if not self.infra_token:
            self.handle()

    def save(self, *args, **kwargs):
        super(Submission, self).save(*args, **kwargs)
        self.post_save()

    def __str__(self):
        return "id: " + str(self.id) + ' team: ' + self.team.name + " user: " + self.user.username

    def set_final(self):
        """
            Use this method instead of changing the is_final attribute directly
            This makes sure that only one instance of TeamSubmission has
            is_final flag set to True.
        """
        if self.status != 'compiled':
            raise ValueError('This submission is not compiled yet.')

        if self.is_mini_game:
            Submission.objects.filter(
                is_mini_game_final=True,
                team=self.team
            ).update(
                is_mini_game_final=False
            )
            self.is_mini_game_final = True
        else:
            Submission.objects.filter(
                is_final=True,
                team=self.team,
            ).update(
                is_final=False
            )
            self.is_final = True

        self.save()

    def handle(self):
        # handle_submission.delay(self.id)
        # handle_submission(self.id)
        pass

    def upload(self):
        from ..logics import upload_code

        self.infra_token = upload_code(self)
        self.status = SubmissionStatusTypes.UPLOADED
        self.save()

    def compile(self):
        # from ..logics import compile_submissions
        # result = compile_submissions([self])
        # if result[0]['success']:
        #     self.status = SubmissionStatusTypes.COMPILING
        #     self.infra_compile_token = result[0]['run_id']
        # else:
        #     logger.error(result[0][self.infra_token]['errors'])
        # self.save()
        pass

    @classmethod
    def update_submission(cls, infra_token, status, infra_message=''):
        submission = get_object_or_404(cls, infra_token=infra_token)

        submission.status = status
        submission.infra_compile_message = infra_message
        submission.save()

        if status == SubmissionStatusTypes.COMPILED:
            submission.set_final()

        return submission

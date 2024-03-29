import logging

from AIC22_Backend.celery import app

logger = logging.getLogger(__name__)


@app.task(name='handle_submission')
def handle_submission(submission_id):
    from .models import Submission
    submission = Submission.objects.get(id=submission_id)
    try:
        if not submission.infra_token:
            submission.upload()
        # submission.compile()

    except Exception as error:
        logger.error(error)

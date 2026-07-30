from email.utils import parseaddr

from flask import current_app
from flask_mail import Message

from app.extensions import mail


MAX_RECIPIENTS = 20


def _validated_recipients(emails):
    if not isinstance(emails, list) or not emails:
        raise ValueError("Provide at least one recipient email address.")
    if len(emails) > MAX_RECIPIENTS:
        raise ValueError(f"You can send to at most {MAX_RECIPIENTS} recipients at once.")

    recipients = []
    seen = set()
    for value in emails:
        if not isinstance(value, str):
            raise ValueError("Each recipient email address must be a string.")
        _, address = parseaddr(value.strip())
        normalized = address.lower()
        local_part, separator, domain = normalized.rpartition("@")
        if (
            not normalized
            or not separator
            or not local_part
            or not domain
            or " " in normalized
        ):
            raise ValueError(f"Invalid email address: {value}")
        if normalized not in seen:
            seen.add(normalized)
            recipients.append(normalized)
    return recipients


def send_survey_invitations(survey, creator, emails):
    """Send private survey invitations for a creator-owned survey."""
    sender = current_app.config.get("MAIL_DEFAULT_SENDER")
    share_url_template = current_app.config.get("SURVEY_SHARE_URL_TEMPLATE")
    if not sender:
        raise RuntimeError("Email sending is not configured.")
    if not share_url_template:
        raise RuntimeError("SURVEY_SHARE_URL_TEMPLATE is not configured.")
    if "{share_token}" not in share_url_template:
        raise RuntimeError("SURVEY_SHARE_URL_TEMPLATE must contain {share_token}.")

    try:
        share_url = share_url_template.format(share_token=survey.share_token)
    except (KeyError, ValueError) as error:
        raise RuntimeError("SURVEY_SHARE_URL_TEMPLATE must contain {share_token}.") from error

    recipients = _validated_recipients(emails)
    subject = f'{creator.fullname} invited you to complete "{survey.title}"'
    body = (
        f"Hello,\n\n{creator.fullname} invited you to complete the survey "
        f'"{survey.title}".\n\nOpen the survey: {share_url}\n\nThank you.'
    )

    with mail.connect() as connection:
        for recipient in recipients:
            connection.send(Message(
                subject=subject,
                recipients=[recipient],
                body=body,
                sender=sender,
                reply_to=creator.email,
            ))
    return len(recipients)

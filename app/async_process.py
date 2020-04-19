from threading import Thread
import pandas as pd
import os
import logging

from app import app, mail, Attachment, Message
from app.mace.mace import Mace
from app.mace.reporter import MaceReporter


class AsyncProcess(object):
    """
    Run Mace asynchronously.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, inputs):
        self.inputs = inputs
        self.app_obj = app

    def start_async_process(self):
        """
        Start a thread that process the request asynchronously.
        """
        thr = Thread(target=self.run_async, args=[self.app_obj, self.inputs])
        thr.start()
        self.logger.info("Thread started")

    def run_async(self):
        """Send the mail asynchronously."""

        try:
            with self.app_obj.app_context():

                algo = Mace()
                algo.fit()
                self.logger.info("Mace finished")

                report = MaceReporter(algo)
                attachment = self.prepare_attachment(report)
                self.logger.info("Attachment prepared")

                email = self.prepare_email(attachment)
                self.logger.info("Email prepared")

                mail.send(email)
                self.logger.info("Email sent")

                # delete file from memory
                os.remove(path)
                self.logger.info("Attachement removed from disk")


        except Exception as e:
            with self.app_obj.app_context():

                msg = mail.send_message(
                    subject='Mace: Sorry, something went wrong',
                    sender=app.config['ADMINS'][0],
                    recipients=[self.inputs['email']],
                    body=(
                        """
                        Dear user,

                        Sorry, something went wrong while wordifying your file.
                        The administrators have been notified and the problem
                        will be solved as soon as possible.
                        
                        Your MilaNLP Team
                        """
                    )
                )

                msg_to_admin = mail.send_message(
                    subject='Wordify: Exception',
                    sender=app.config['ADMINS'][0],
                    recipients=[app.config['ADMINS']
                                [0], app.config['ADMINS'][1]],
                    body='{}\n{}'.format(e.__doc__, e)
                )

    def prepare_email(self, attachment) -> Message:
        with self.app_obj.open_resource('forms/{}'.format(f_name)) as file:
            attachment = Attachment(
                filename=f_name,
                data=attachment,
                content_type='application/vnd.ms-excel'
            )

        msg = Message(
            subject='Wordified file',
            sender=app.config['ADMINS'][0],
            recipients=[recipient],
            attachments=[attachment],
            body=(
                """
                Dear user,

                Please find attached your file. It contains two sheets:
                one with the positive indicators for each label and one
                with the negative indicators (note that if you have only
                two labels, the positive indicators of one label are the
                negative ones of the other, and vice versa). If you do not
                see any indicators, you might have provided too few texts
                per label.
                
                Your MilaNLP Team
                """
            ),
        )

        return msg

    def prepare_attachment(self, report):
        f_name = "file_completed"
        path = os.path.join(app.config['UPLOAD_FOLDER'], f_name)
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            report.to_excel(writer, sheet_name='Positive', index=False)

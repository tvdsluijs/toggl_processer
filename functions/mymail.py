import smtplib, ssl
import logging


class MyMail:
    def __init__(self, username: str = None, pwd: str = None, server: str = None, port: int = 587):
        try:
            if username is None:
                raise ValueError("We need a username to work")
            if pwd is None:
                raise ValueError("We need a Password to work")
            if server is None:
                raise ValueError("We need a server to work")

            self.username = username
            self.pwd = pwd
            self.port = port
            self.server = server

        except ValueError as e:
            logging.critical(e)
        except Exception as e:
            logging.warning(e)

    def send_that_mail(self, subject: str = "Very empty subject", message: str = "Sorry, empty message",
                    receiver: str = None, attachments: list = None):
        try:
            if receiver is None:
                raise ValueError("We need a receiver to send a mail")

            context = ssl.create_default_context()
            with smtplib.SMTP(self.server, self.port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(self.username, self.pwd)
                server.sendmail(self.username, receiver, message)

            # # Create a secure SSL context
            # context = ssl.create_default_context()
            #
            # # Try to log in to server and send email
            # server = smtplib.SMTP(self.server, self.port)
            # server.ehlo()  # Can be omitted
            # server.starttls(context=context)  # Secure the connection
            # server.ehlo()  # Can be omitted
            # server.login(self.username, self.password)
            #
            # server.sendmail(self.username, receiver, message)

        except ValueError as e:
            logging.critical(e)
        except Exception as e:
            logging.error(e)
            print(e)
        # finally:
        #     server.quit()


if __name__ == '__main__':
    mm = MyMail(username="info@resultants-e.nl", pwd="hnQ9gVDGfLrqHTsJH?yy", server="mail.resultants-e.nl")
    mm.send_that_mail(subject="Dit is het onderwerp", receiver="tvdsluijs@gmail.com", message="Hallo dit is een berichtje")

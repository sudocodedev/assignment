from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import redirect

from .forms import CustomUserCreationForm

from time import perf_counter as pc
import requests
import logging
import threading

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler(f'{__name__}.log', mode='a', encoding='utf-8')
formatter = logging.Formatter("{name} - {asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M",)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


URL = "https://icanhazdadjoke.com/"
timeouts = (4, 5)

def get_joke() -> str:
    try:
        res = requests.get(URL, headers={'Accept': 'application/json'}, timeout=timeouts)
    except TimeoutError:
        logger.error("There was a problem in getting a joke")
        return "Connection got timed out, pls after sometime"

    if res.status_code == 200:
        logger.info("got the joke")
    return res.json().get('joke', '')


@receiver(pre_save, sender=User)
def user_valid_handler(sender, instance, *args, **kwargs):
    if not instance.username.isalpha():
        logger.error(f"{instance.username} -> username should only contains letters")
        raise Exception("Username should only contains letters")

@receiver(post_save, sender=User)
def user_register_handler(sender, instance, created, *args, **kwargs):
    logger.info(f"user register handler signal got triggered for {instance.username}")
    if created:
        if instance.is_superuser: pass
        else:
            start_time = pc()

            user = sender.objects.get(id=instance.id)
            joke = get_joke()

            subject = "Example Mail with JOKE!"
            message = render_to_string('core/mail.html', {'user':user.username, 'joke':joke})
            email = EmailMessage(subject, message, to=[user.email,])

            current_thread = threading.current_thread()
            logger.info(f"signal received in threadName = {current_thread.name}, threadID = {current_thread.ident}")

            if email.send():
                logger.info(f"Email sent to {user.username} in this mail {user.email}")
            else:
                logger.error("There was a problem in sending a mail")

            logger.info(f"Time taken for sending email = {pc() - start_time} sec(s)")

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            start_time = pc()

            logger.info(f"saving {form.cleaned_data.get('username', 'N/A')} to DB")
            form.save()

            current_thread = threading.current_thread()
            logger.info(f"account creation happening in threadName = {current_thread.name}, threadID = {current_thread.ident}")
            logger.info(f"Time taken for saving the user to DB = {pc() - start_time} sec(s)")


            logger.info("a new user registered successfully")
            return redirect('home')
        else:
            logger.info("problem in submitting the form")
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'core/forms.html', context)



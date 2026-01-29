from django.db import models

# Create your models here.

class Message(models.Model):
    user_message = models.TextField()
    bot_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_message[:30]
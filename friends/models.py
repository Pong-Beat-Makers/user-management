from django.db import models
from social_login import models as social_login_models

# Create your models here.
class Friendship(models.Model):
	user = models.ForeignKey(social_login_models.User, on_delete=models.CASCADE, related_name='user')
	friend = models.ForeignKey(social_login_models.User, on_delete=models.CASCADE, related_name='friend')
	# created_at = models.DateTimeField(auto_now_add=True)
	# updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		unique_together = ('user', 'friend',)

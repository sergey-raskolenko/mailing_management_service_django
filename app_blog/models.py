from django.db import models

from users.models import NULLABLE


class Blog(models.Model):
	title = models.CharField(max_length=100, verbose_name='заголовок')
	content = models.TextField(verbose_name='cодержание')
	image = models.ImageField(verbose_name='изображение', upload_to='blog/', **NULLABLE)
	views = models.IntegerField(verbose_name='количество просмотров', default=0, editable=False)
	published_date = models.DateTimeField(verbose_name='дата публикации', auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'блог'
		verbose_name_plural = 'блоги'
		db_table = 'blogs'
		ordering = ['published_date']

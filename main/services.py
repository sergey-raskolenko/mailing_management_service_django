from django.core.cache import cache
from django.db import models
from config import settings


def cache_object_list(model):
	if settings.CACHE_ENABLED:
		name = str(model).split(".")[2][:-2]
		key = f'{name}_list'
		object_list = cache.get(key)
		if object_list is None:
			object_list = model.objects.all()
			cache.set(key, object_list)
	else:
		object_list = model.objects.all()
	return object_list

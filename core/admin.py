from django.contrib import admin
import core.models

for modelo in dir(core.models):
	if getattr(core.models, modelo).__class__.__name__ == 'ModelBase':
		try:
			admin.site.register(getattr(core.models, modelo))
		except:
			pass
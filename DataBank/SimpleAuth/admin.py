from django.contrib import admin

from models import Resource, Consumer, Token, TokenManager

class ResourceAdmin(admin.ModelAdmin):
	pass
	
class ConsumerAdmin(admin.ModelAdmin):
	raw_id_fields = ['user',]

class TokenAdmin(admin.ModelAdmin):
	pass

class TokenManagerAdmin(admin.ModelAdmin):
	raw_id_fields = ['user', 'consumer', 'resource']
	

admin.site.register(Resource, ResourceAdmin)
admin.site.register(Consumer, ConsumerAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(TokenManager, TokenManagerAdmin)
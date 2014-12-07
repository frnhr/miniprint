from django.contrib import admin

def admin_register(user_admin_class):
    admin.site.register(user_admin_class.model, user_admin_class)

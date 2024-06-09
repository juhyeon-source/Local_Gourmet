from django.contrib import admin
from accounts.models import Accounts, Bookmark


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    pass


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass
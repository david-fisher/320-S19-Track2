from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MembersOnlyConfig(AppConfig):
    name = 'members_only'
    verbose_name = _('members_only')

    def ready(self):
        import members_only.signals

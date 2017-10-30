from django.contrib.admin import SimpleListFilter


class PostOwnerFilter(SimpleListFilter):
    title = 'By owner'
    parameter_name = 'by_owner'

    class CHOICES:
        MY = 'my'
        TO_ME = 'to_me'

        LOOKUPS = [
            (MY, 'Only my'),
            (TO_ME, 'Assigned to me'),
        ]

    def lookups(self, request, model_admin):
        return self.CHOICES.LOOKUPS

    def queryset(self, request, queryset):
        queryset = queryset.all()
        if self.value() == self.CHOICES.MY:
            queryset = queryset.filter(author=request.user)
        if self.value() == self.CHOICES.TO_ME:
            queryset = queryset.filter(assigned=request.user)
        return queryset


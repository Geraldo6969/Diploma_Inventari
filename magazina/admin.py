from datetime import timedelta

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import LevizjeStoku, Produkti


admin.site.site_header = 'E Inventory'
admin.site.site_title = 'E Inventory'
admin.site.index_title = 'E Inventory'


class ChoiceTitleFilter(admin.SimpleListFilter):
    field_name = ''
    title = ''
    parameter_name = ''
    choices_source = ()

    def lookups(self, request, model_admin):
        return self.choices_source

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.field_name: self.value()})
        return queryset


class NjesiaMateseFilter(ChoiceTitleFilter):
    title = 'NJESIA'
    parameter_name = 'njesia'
    field_name = 'njesia_matese'
    choices_source = Produkti.NJESIA_CHOICES


class MonedhaFilter(ChoiceTitleFilter):
    title = 'MONEDHA'
    parameter_name = 'monedha'
    field_name = 'monedha'
    choices_source = Produkti.MONEDHA_CHOICES


class OfertaFilter(admin.SimpleListFilter):
    title = 'STATUSI OFERTES'
    parameter_name = 'oferta'

    def lookups(self, request, model_admin):
        return (
            ('po', 'Ne Oferte'),
            ('jo', 'Pa Oferte'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'po':
            return queryset.filter(ne_oferte=True)
        if self.value() == 'jo':
            return queryset.filter(ne_oferte=False)
        return queryset


class KrijuarNgaFilter(admin.SimpleListFilter):
    title = 'KRIJUAR NGA'
    parameter_name = 'krijuar_nga'

    def lookups(self, request, model_admin):
        users = model_admin.get_queryset(request).exclude(krijuar_nga__isnull=True).values_list(
            'krijuar_nga__id',
            'krijuar_nga__username',
        ).distinct().order_by('krijuar_nga__username')
        return [(user_id, username.title()) for user_id, username in users]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(krijuar_nga_id=self.value())
        return queryset


class SmartDateFilter(admin.SimpleListFilter):
    field_name = ''
    title = ''
    parameter_name = ''

    def lookups(self, request, model_admin):
        return (
            ('today', 'Sot'),
            ('week', '7 Ditet e Ardhshme'),
            ('month', 'Ky Muaj'),
            ('past', 'Ne Te Kaluaren'),
            ('future', 'Ne Te Ardhmen'),
            ('has_date', 'Me Date'),
            ('no_date', 'Pa Date'),
        )

    def queryset(self, request, queryset):
        today = timezone.localdate()
        value = self.value()

        if value == 'today':
            return queryset.filter(**{self.field_name: today})
        if value == 'week':
            return queryset.filter(**{
                f'{self.field_name}__gte': today,
                f'{self.field_name}__lte': today + timedelta(days=7),
            })
        if value == 'month':
            return queryset.filter(**{
                f'{self.field_name}__year': today.year,
                f'{self.field_name}__month': today.month,
            })
        if value == 'past':
            return queryset.filter(**{f'{self.field_name}__lt': today})
        if value == 'future':
            return queryset.filter(**{f'{self.field_name}__gt': today})
        if value == 'has_date':
            return queryset.filter(**{f'{self.field_name}__isnull': False})
        if value == 'no_date':
            return queryset.filter(**{f'{self.field_name}__isnull': True})
        return queryset


class DataHyrjesFilter(SmartDateFilter):
    title = 'DATA HYRJES'
    parameter_name = 'data_hyrjes_status'
    field_name = 'data_hyrjes'


class DataDaljesFilter(SmartDateFilter):
    title = 'DATA DALJES'
    parameter_name = 'data_daljes_status'
    field_name = 'data_daljes'


class DataSkadencesFilter(SmartDateFilter):
    title = 'DATA SKADENCES'
    parameter_name = 'data_skadences_status'
    field_name = 'data_skadences'

    def lookups(self, request, model_admin):
        return (
            ('expired', 'Skaduar'),
            ('expires_week', 'Skadon Ne 7 Dite'),
            ('expires_month', 'Skadon Kete Muaj'),
            ('future', 'Skadence Ne Te Ardhmen'),
            ('has_date', 'Me Date Skadence'),
            ('no_date', 'Pa Date Skadence'),
        )

    def queryset(self, request, queryset):
        today = timezone.localdate()
        value = self.value()

        if value == 'expired':
            return queryset.filter(data_skadences__lt=today)
        if value == 'expires_week':
            return queryset.filter(data_skadences__gte=today, data_skadences__lte=today + timedelta(days=7))
        if value == 'expires_month':
            return queryset.filter(data_skadences__year=today.year, data_skadences__month=today.month)
        return super().queryset(request, queryset)


@admin.register(Produkti)
class ProduktiAdmin(admin.ModelAdmin):
    list_display = (
        'emri',
        'shfaq_perdoruesi',
        'furnitori',
        'shfaq_sasia',
        'shfaq_njesia',
        'shfaq_monedha',
        'shfaq_cmimi_blerjes',
        'shfaq_cmimi_shitjes',
        'shfaq_oferte',
        'shfaq_data_hyrjes',
        'shfaq_data_daljes',
        'shfaq_data_skadences',
        'shfaq_qr_miniature',
    )
    list_display_links = ('emri',)
    list_filter = (
        NjesiaMateseFilter,
        MonedhaFilter,
        OfertaFilter,
        DataHyrjesFilter,
        DataDaljesFilter,
        DataSkadencesFilter,
        KrijuarNgaFilter,
    )
    search_fields = ('emri', 'pershkrimi', 'furnitori', 'krijuar_nga__username')
    readonly_fields = ('qr_code', 'shfaq_qr_madhe')
    ordering = ('emri',)
    sortable_by = (
        'emri',
        'shfaq_perdoruesi',
        'furnitori',
        'shfaq_sasia',
        'shfaq_njesia',
        'shfaq_monedha',
        'shfaq_cmimi_blerjes',
        'shfaq_cmimi_shitjes',
        'shfaq_oferte',
        'shfaq_data_hyrjes',
        'shfaq_data_daljes',
        'shfaq_data_skadences',
    )
    list_per_page = 25
    date_hierarchy = 'krijuar_me'

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if not request.user.is_superuser and 'shfaq_perdoruesi' in list_display:
            list_display.remove('shfaq_perdoruesi')
        return list_display

    def get_search_fields(self, request):
        if request.user.is_superuser:
            return super().get_search_fields(request)
        return ('emri', 'pershkrimi', 'furnitori')

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return super().get_list_filter(request)
        return (
            NjesiaMateseFilter,
            MonedhaFilter,
            OfertaFilter,
            DataHyrjesFilter,
            DataDaljesFilter,
            DataSkadencesFilter,
        )

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('krijuar_nga')
        if request.user.is_superuser:
            return queryset
        return queryset.filter(krijuar_nga=request.user)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser and 'krijuar_nga' not in readonly_fields:
            readonly_fields.append('krijuar_nga')
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'krijuar_nga' and not request.user.is_superuser:
            kwargs['queryset'] = request.user.__class__.objects.filter(pk=request.user.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.krijuar_nga_id:
            obj.krijuar_nga = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='KRIJUAR NGA', ordering='krijuar_nga__username')
    def shfaq_perdoruesi(self, obj):
        if obj.krijuar_nga:
            return format_html('<span class="ei-user-pill">{}</span>', obj.krijuar_nga.username.title())
        return format_html('<span class="ei-muted-pill">{}</span>', 'Pa User')

    @admin.display(description='STOKU', ordering='sasia')
    def shfaq_sasia(self, obj):
        css_class = 'ei-stock-low' if obj.sasia < obj.stoku_minimal else 'ei-stock-ok'
        return format_html(
            '<span class="ei-stock-pill {}">{} {}</span>',
            css_class,
            obj.sasia,
            obj.njesia_matese,
        )

    @admin.display(description='NJESIA', ordering='njesia_matese')
    def shfaq_njesia(self, obj):
        return format_html('<span class="ei-soft-pill">{}</span>', obj.get_njesia_matese_display())

    @admin.display(description='MONEDHA', ordering='monedha')
    def shfaq_monedha(self, obj):
        return format_html('<span class="ei-currency-pill">{}</span>', obj.monedha)

    @admin.display(description='CMIMI BLERJES', ordering='cmimi_blerjes')
    def shfaq_cmimi_blerjes(self, obj):
        return format_html('<strong class="ei-price-buy">{} {}</strong>', f'{obj.cmimi_blerjes:.2f}', obj.monedha)

    @admin.display(description='CMIMI SHITJES', ordering='cmimi_shitjes')
    def shfaq_cmimi_shitjes(self, obj):
        if obj.ne_oferte and obj.cmimi_ofertes:
            return format_html(
                '<span class="ei-old-price">{} {}</span><br><strong class="ei-price-sell">{} {}</strong>',
                f'{obj.cmimi_shitjes:.2f}',
                obj.monedha,
                f'{obj.cmimi_ofertes:.2f}',
                obj.monedha,
            )
        return format_html('<strong class="ei-price-sell">{} {}</strong>', f'{obj.cmimi_shitjes:.2f}', obj.monedha)

    @admin.display(description='OFERTA', ordering='ne_oferte')
    def shfaq_oferte(self, obj):
        if obj.ne_oferte:
            return format_html('<span class="ei-offer-pill">{}</span>', 'NE OFERTE')
        return format_html('<span class="ei-muted-pill">{}</span>', 'NORMAL')

    @admin.display(description='DATA HYRJES', ordering='data_hyrjes')
    def shfaq_data_hyrjes(self, obj):
        return self._date_pill(obj.data_hyrjes)

    @admin.display(description='DATA DALJES', ordering='data_daljes')
    def shfaq_data_daljes(self, obj):
        return self._date_pill(obj.data_daljes)

    @admin.display(description='DATA SKADENCES', ordering='data_skadences')
    def shfaq_data_skadences(self, obj):
        return self._date_pill(obj.data_skadences, danger=True)

    def _date_pill(self, value, danger=False):
        if not value:
            return format_html('<span class="ei-muted-pill">{}</span>', 'Pa Date')
        css_class = 'ei-date-danger' if danger else 'ei-date-pill'
        return format_html('<span class="{}">{}</span>', css_class, value)

    @admin.display(description='QR')
    def shfaq_qr_miniature(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:8px;border:1px solid #dbeafe;padding:2px;background:white;"/>',
                obj.qr_code.url,
            )
        return 'Ne pritje...'

    @admin.display(description='Linku i kodit')
    def shfaq_qr_madhe(self, obj):
        if obj.qr_code:
            return format_html('<a href="{}" target="_blank" rel="noopener">Hap QR Code</a>', obj.qr_code.url)
        return 'Do te gjenerohet pas ruajtjes'


@admin.register(LevizjeStoku)
class LevizjeStokuAdmin(admin.ModelAdmin):
    list_display = ('produkti', 'lloji', 'sasia', 'vlera', 'stoku_pas', 'krijuar_me', 'perdoruesi')
    list_filter = ('lloji', 'krijuar_me')
    search_fields = ('produkti__emri',)
    readonly_fields = ('produkti', 'lloji', 'sasia', 'vlera', 'stoku_pas', 'krijuar_me', 'perdoruesi')
    ordering = ('-krijuar_me',)
    list_per_page = 30

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('produkti', 'perdoruesi')
        if request.user.is_superuser:
            return queryset
        return queryset.filter(produkti__krijuar_nga=request.user)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

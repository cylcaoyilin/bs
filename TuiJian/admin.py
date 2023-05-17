from django.contrib import admin
from .models import *
from openpyxl import Workbook
from django.http import HttpResponse


admin.site.site_title = "短视频标签推荐系统"
admin.site.site_header = "短视频标签推荐系统"

class ExportExcelMixin(object):
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        for obj in queryset:
            for field in field_names:
                data = [f'{getattr(obj, field)}' for field in field_names]
            row = ws.append(data)

        wb.save(response)
        return response
    export_as_excel.short_description = '导出Excel'


# Register your models here.
@admin.register(Case_item)
class Case_item_Admin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ("name", "text", "itype", "biaoqian", "lianjie",)
    actions = ['export_as_excel']
    search_fields = ("name",)
    list_filter = ['itype']

@admin.register(Users)
class Users_Admin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ("username", "email", "set", "age")
    actions = ['export_as_excel']
    search_fields = ("username",)


@admin.register(Pinfen)
class Pinfen_Admin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ("user", "case", "data")
    actions = ['export_as_excel']
    search_fields = ("user",)


@admin.register(PinLun)
class PinLun_Admin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ("user", "case","content", "data")
    actions = ['export_as_excel']
    search_fields = ("user","content",)

@admin.register(Biaoqian)
class Biaoqian_Admin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ("user", "biaoqian","fenshu", "data")
    actions = ['export_as_excel']
    search_fields = ("user","biaoqian",)

from django.contrib import admin
from django.http import HttpResponse
import csv
from openpyxl import Workbook
from .models import Service, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    actions = ['export_as_csv', 'export_as_excel']

    def export_as_csv(self, request, queryset):
        # Создаем HTTP-ответ с типом содержимого 'text/csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users_services_report.csv"'
        response.write('\ufeff'.encode('utf8'))  # Добавляем BOM для корректной кодировки

        writer = csv.writer(response)

        # Записываем заголовки колонок
        writer.writerow(['Username', 'Phone Number', 'Address', 'Services'])

        for profile in queryset:
            # Получаем список названий услуг для каждого пользователя
            services = profile.services.all()
            services_list = ', '.join(service.name for service in services)

            # Записываем данные пользователя в CSV
            writer.writerow([profile.user.username, profile.phone_number, profile.address, services_list])

        return response

    def export_as_excel(self, request, queryset):
        # Создаем HTTP-ответ с типом содержимого 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="users_services_report.xlsx"'

        # Создаем новый Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Users Services Report"

        # Записываем заголовки колонок
        ws.append(['Username', 'Phone Number', 'Address', 'Services'])

        for profile in queryset:
            # Получаем список названий услуг для каждого пользователя
            services = profile.services.all()
            services_list = ', '.join(service.name for service in services)

            # Записываем данные пользователя в Excel
            ws.append([profile.user.username, profile.phone_number, profile.address, services_list])

        # Сохраняем workbook в ответ
        wb.save(response)
        return response

    export_as_csv.short_description = "Export Selected to CSV"
    export_as_excel.short_description = "Export Selected to Excel"


admin.site.register(Service)
admin.site.register(UserProfile, UserProfileAdmin)

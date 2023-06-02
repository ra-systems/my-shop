from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from erp_framework.reporting.registry import register_report_view
from erp_framework.reporting.views import ReportView
from slick_reporting.fields import SlickReportField, TotalReportField

from .models import Sale, Product


@register_report_view
class SaleListReportView(ReportView):
    report_model = Sale
    report_title = "Sales List"
    columns = [
        "number",
        "date",
        ("client__name", {"verbose_name": "Client Name"}),
        "product__name",
        "quantity",
        "price",
        ("value", {"is_summable": True}),
    ]


@register_report_view
class TotalProductSales(ReportView):
    # the model to use for the report
    report_model = Sale
    base_model = Product

    # the field to use for the date
    date_field = "date"

    report_title = "Total Product Sales"

    # the field to use for the group by
    group_by = "product"

    # Columns to display ,
    with_type = False
    columns = [
        "name",
        SlickReportField.create(Sum, "value", verbose_name="Total Value"),
    ]


@register_report_view
class TotalProductSalesTimeSeries(ReportView):
    # the model to use for the report
    report_model = Sale
    base_model = Product

    # the field to use for the date
    date_field = "date"

    report_title = "Product SalesTime Series"

    # the field to use for the group by
    group_by = "product"

    with_type = False

    # Columns to display ,
    columns = [
        "name",
        "__time_series__",
        SlickReportField.create(Sum, "value", verbose_name="Total Value"),
    ]

    time_series_selector = True
    time_series_selector_default = "monthly"

    time_series_columns = [
        SlickReportField.create(Sum, "value", verbose_name=_("Value"), name="value")
    ]

    chart_settings = [
        {
            "type": "column",
            "data_source": ["value"],
            "title_source": "type",
        },
        {
            "title": "Total",
            "engine_name": "chartsjs",
            "type": "column",
            "data_source": ["value"],
            "title_source": "type",
            "plot_total": True,
        },
        {
            "title": "Total",
            "engine_name": "chartsjs",
            "type": "pie",
            "data_source": ["value"],
            "title_source": "type",
            "plot_total": True,
        },
    ]


class TotalValue(SlickReportField):
    calculation_method = Sum
    calculation_field = "value"
    is_summable = True
    verbose_name = _("Total Value")
    name = "total_value"

    # def final_calculation(self, debit, credit, dep_dict):
    #     result = super().final_calculation(debit, credit, dep_dict)
    #     print(result)
    #     return round(result, 2)


class PercentageToTotal(SlickReportField):
    requires = (TotalValue,)
    prevent_group_by = True
    is_summable = False
    name = "percentage_to_total"
    verbose_name = _("% Total")

    @classmethod
    def get_time_series_field_verbose_name(cls, date_period, index, dates, pattern):
        return "%"

    def final_calculation(self, debit, credit, dep_dict):
        debit = debit or 0
        credit = credit or 0
        try:
            return round((dep_dict.get("total_value", 0) / (debit - credit)) * 100, 2)
        except ZeroDivisionError:
            return 0


@register_report_view
class TotalProductSalesTimeSeriesWithPercentage(ReportView):
    report_model = Sale
    # base_model = Product

    # the field to use for the date
    date_field = "date"

    report_title = "Product Sales Time Series (with %)"

    # the field to use for the group by
    group_by = "product"

    # Columns to display ,
    columns = [
        "name",
        "__time_series__",
        TotalValue,
        PercentageToTotal,
    ]

    time_series_selector = True
    time_series_selector_default = "monthly"
    #
    time_series_columns = [
        TotalValue,
        PercentageToTotal,
    ]

    chart_settings = [
        {
            "type": "column",
            "data_source": ["total_value"],
            "title_source": ["name"],
        },
        {
            "title": "Total",
            # "engine_name": "chartsjs",
            "type": "column",
            "data_source": ["total_value"],
            "title_source": ["name"],
            "plot_total": True,
        },
        {
            "title": "Total",
            # "engine_name": "chartsjs",
            "type": "pie",
            "data_source": ["total_value"],
            "title_source": ["name"],
            "plot_total": True,
        },
    ]


class CustomCrossTabTotalField(TotalReportField):
    # Customizing how the verbose names are constructed
    # if not set, the verbose name will display the id of the crosstab field,
    # and the remainder column will be called "The remainder"

    @classmethod
    def get_crosstab_field_verbose_name(cls, model, id):
        from .models import Client

        if id == "----":
            return _("Rest of clients")
        name = Client.objects.get(pk=id).name
        return f"{cls.verbose_name} {name}"


@register_report_view
class ProductClientSalesCrossTab(ReportView):
    report_model = Sale
    base_model = Product

    report_title = "Product Client Sales Cross Tab"

    group_by = "product"

    crosstab_field = "client"
    crosstab_columns = ["__total__"]

    with_type = False

    columns = [
        "name",
        "__crosstab__",
    ]

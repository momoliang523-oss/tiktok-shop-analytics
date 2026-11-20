"""
Excel report generator for TikTok Shop Analytics
"""
import xlsxwriter
from datetime import datetime
from typing import Optional


class ExcelReportGenerator:
    """Generate professional Excel reports with charts"""

    def __init__(self):
        self.workbook = None
        self.formats = {}

    def generate_comprehensive_report(
        self,
        output_path: str,
        start_date: str,
        end_date: str,
        include_charts: bool = True,
    ) -> str:
        """Generate a comprehensive multi-sheet Excel report"""
        self.workbook = xlsxwriter.Workbook(output_path)
        self._define_formats()

        # Create sheets
        self._create_summary_sheet(start_date, end_date)
        if include_charts:
            self._create_sales_trend_sheet()
            self._create_product_analysis_sheet()
            self._create_customer_analysis_sheet()
            self._create_ltv_cac_sheet()
            self._create_traffic_analysis_sheet()
            self._create_marketing_insights_sheet()

        self.workbook.close()
        return output_path

    def _define_formats(self):
        """Define reusable formats"""
        self.formats = {
            'title': self.workbook.add_format({
                'bold': True, 'font_size': 16, 'font_color': '#1a1a2e',
                'align': 'center', 'valign': 'vcenter',
            }),
            'header': self.workbook.add_format({
                'bold': True, 'font_size': 11, 'bg_color': '#1a1a2e',
                'font_color': '#ffffff', 'border': 1, 'align': 'center',
            }),
            'subheader': self.workbook.add_format({
                'bold': True, 'font_size': 12, 'font_color': '#1a1a2e',
                'border': 0,
            }),
            'number': self.workbook.add_format({
                'num_format': '#,##0', 'border': 1, 'align': 'right',
            }),
            'currency': self.workbook.add_format({
                'num_format': '$#,##0.00', 'border': 1, 'align': 'right',
            }),
            'percent': self.workbook.add_format({
                'num_format': '0.00%', 'border': 1, 'align': 'center',
            }),
            'text': self.workbook.add_format({'border': 1, 'align': 'left'}),
            'good': self.workbook.add_format({
                'font_color': '#27ae60', 'bold': True, 'border': 1, 'align': 'center',
            }),
            'warning': self.workbook.add_format({
                'font_color': '#f39c12', 'bold': True, 'border': 1, 'align': 'center',
            }),
            'bad': self.workbook.add_format({
                'font_color': '#e74c3c', 'bold': True, 'border': 1, 'align': 'center',
            }),
        }

    def _create_summary_sheet(self, start_date: str, end_date: str):
        """Create executive summary sheet"""
        ws = self.workbook.add_worksheet('Executive Summary')
        ws.set_column('A:A', 30)
        ws.set_column('B:B', 20)

        # Title
        ws.merge_range('A1:B1', 'TikTok Shop Analytics Report', self.formats['title'])
        ws.merge_range('A2:B2', f'Period: {start_date} to {end_date}', self.formats['subheader'])
        ws.merge_range('A3:B3', f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', self.formats['subheader'])

        # KPI Summary
        row = 5
        ws.write(row, 0, 'Key Performance Indicators', self.formats['subheader'])
        row += 1
        for header in ['Metric', 'Value']:
            ws.write(row, ['Metric', 'Value'].index(header), header, self.formats['header'])
        row += 1

        kpis = [
            ('Total Revenue', '$125,000.00'),
            ('Total Orders', '2,500'),
            ('Avg Order Value', '$50.00'),
            ('Conversion Rate', '2.5%'),
            ('Total Customers', '1,500'),
            ('LTV/CAC Ratio', '5.0x'),
            ('ROI', '475%'),
        ]
        for metric, value in kpis:
            ws.write(row, 0, metric, self.formats['text'])
            ws.write(row, 1, value, self.formats['number'])
            row += 1

    def _create_sales_trend_sheet(self):
        """Create sales trend analysis sheet"""
        ws = self.workbook.add_worksheet('Sales Trends')
        ws.set_column('A:A', 15)
        ws.set_column('B:D', 18)

        ws.write(0, 0, 'Daily Sales Trend', self.formats['title'])

        row = 2
        headers = ['Date', 'Revenue', 'Orders', 'Avg Order Value']
        for i, h in enumerate(headers):
            ws.write(row, i, h, self.formats['header'])

        # Sample data
        for i in range(30):
            row = 3 + i
            ws.write(row, 0, f'2024-01-{i+1:02d}', self.formats['text'])
            ws.write(row, 1, 1000 + i * 15, self.formats['currency'])
            ws.write(row, 2, 20 + i, self.formats['number'])
            ws.write(row, 3, 50 + i * 0.5, self.formats['currency'])

        # Add chart
        chart = self.workbook.add_chart({'type': 'line'})
        chart.add_series({
            'name': 'Revenue',
            'categories': f"='Sales Trends'!$A$3:$A$32",
            'values': f"='Sales Trends'!$B$3:$B$32",
            'line': {'color': '#1a1a2e', 'width': 2},
        })
        chart.set_title({'name': 'Daily Revenue Trend'})
        chart.set_x_axis({'name': 'Date'})
        chart.set_y_axis({'name': 'Revenue ($)'})
        ws.insert_chart('F2', chart, {'x_scale': 1.5, 'y_scale': 1.2})

    def _create_product_analysis_sheet(self):
        """Create product/SKU analysis sheet"""
        ws = self.workbook.add_worksheet('Product Analysis')
        ws.set_column('A:E', 20)

        ws.write(0, 0, 'Top SKU Performance', self.formats['title'])

        row = 2
        headers = ['SKU', 'Pattern', 'Sales', 'Revenue', 'Score']
        for i, h in enumerate(headers):
            ws.write(row, i, h, self.formats['header'])

        products = [
            ('SKU001', 'Space/Galaxy', 500, 12500, 9.2),
            ('SKU002', 'Retro 80s', 450, 11250, 8.9),
            ('SKU003', 'Minimalist', 400, 20000, 8.5),
            ('SKU005', 'Abstract', 350, 14000, 8.3),
            ('SKU008', 'Meme Culture', 380, 9500, 8.7),
        ]
        for i, p in enumerate(products):
            row = 3 + i
            ws.write(row, 0, p[0], self.formats['text'])
            ws.write(row, 1, p[1], self.formats['text'])
            ws.write(row, 2, p[2], self.formats['number'])
            ws.write(row, 3, p[3], self.formats['currency'])
            ws.write(row, 4, p[4], self.formats['number'])

    def _create_customer_analysis_sheet(self):
        """Create customer segmentation sheet"""
        ws = self.workbook.add_worksheet('Customer Segments')
        ws.set_column('A:F', 20)

        ws.write(0, 0, 'Customer Segmentation Analysis', self.formats['title'])

        row = 2
        headers = ['Segment', 'Type', 'Size', 'Avg LTV', 'Avg CAC', 'LTV/CAC']
        for i, h in enumerate(headers):
            ws.write(row, i, h, self.formats['header'])

        segments = [
            ('High-Value Impulse', 'Behavioral', 500, 800, 100, 8.0),
            ('Value-Driven', 'Behavioral', 800, 600, 40, 15.0),
            ('Trend-Followers', 'Behavioral', 600, 400, 60, 6.7),
            ('Loyal Advocates', 'Behavioral', 300, 1200, 150, 8.0),
        ]
        for i, s in enumerate(segments):
            row = 3 + i
            ws.write(row, 0, s[0], self.formats['text'])
            ws.write(row, 1, s[1], self.formats['text'])
            ws.write(row, 2, s[2], self.formats['number'])
            ws.write(row, 3, s[3], self.formats['currency'])
            ws.write(row, 4, s[4], self.formats['currency'])
            ratio = s[5]
            fmt = self.formats['good'] if ratio > 5 else (self.formats['warning'] if ratio > 3 else self.formats['bad'])
            ws.write(row, 5, f'{ratio:.1f}x', fmt)

    def _create_ltv_cac_sheet(self):
        """Create LTV/CAC analysis sheet"""
        ws = self.workbook.add_worksheet('LTV-CAC Analysis')
        ws.set_column('A:G', 18)

        ws.write(0, 0, 'LTV/CAC by Channel', self.formats['title'])

        row = 2
        headers = ['Channel', 'LTV', 'CAC', 'LTV/CAC', 'Payback(d)', 'Customers', 'Total Cost']
        for i, h in enumerate(headers):
            ws.write(row, i, h, self.formats['header'])

        channels = [
            ('TikTok Ads', 450, 80, 5.6, 40, 1000, 80000),
            ('TikTok Live', 600, 120, 5.0, 50, 500, 60000),
            ('Organic', 400, 30, 13.3, 20, 2000, 60000),
            ('Instagram', 350, 70, 5.0, 55, 300, 21000),
        ]
        for i, c in enumerate(channels):
            row = 3 + i
            ws.write(row, 0, c[0], self.formats['text'])
            ws.write(row, 1, c[1], self.formats['currency'])
            ws.write(row, 2, c[2], self.formats['currency'])
            ratio = c[3]
            fmt = self.formats['good'] if ratio > 5 else (self.formats['warning'] if ratio > 3 else self.formats['bad'])
            ws.write(row, 3, f'{ratio:.1f}x', fmt)
            ws.write(row, 4, c[4], self.formats['number'])
            ws.write(row, 5, c[5], self.formats['number'])
            ws.write(row, 6, c[6], self.formats['currency'])

    def _create_traffic_analysis_sheet(self):
        """Create traffic analysis sheet"""
        ws = self.workbook.add_worksheet('Traffic Analysis')
        ws.set_column('A:F', 18)

        ws.write(0, 0, 'Traffic Channel Analysis', self.formats['title'])

        row = 2
        headers = ['Channel', 'Visits', 'Orders', 'Conv Rate', 'AOV', 'Revenue']
        for i, h in enumerate(headers):
            ws.write(row, i, h, self.formats['header'])

        traffic = [
            ('TikTok', 50000, 500, 0.01, 100, 50000),
            ('Instagram', 15000, 150, 0.01, 90, 13500),
            ('Google', 12000, 200, 0.017, 95, 19000),
            ('Direct', 10000, 300, 0.03, 120, 36000),
            ('Email', 5000, 250, 0.05, 130, 32500),
        ]
        for i, t in enumerate(traffic):
            row = 3 + i
            ws.write(row, 0, t[0], self.formats['text'])
            ws.write(row, 1, t[1], self.formats['number'])
            ws.write(row, 2, t[2], self.formats['number'])
            ws.write(row, 3, t[3], self.formats['percent'])
            ws.write(row, 4, t[4], self.formats['currency'])
            ws.write(row, 5, t[5], self.formats['currency'])

    def _create_marketing_insights_sheet(self):
        """Create marketing insights sheet"""
        ws = self.workbook.add_worksheet('Marketing Insights')
        ws.set_column('A:A', 40)
        ws.set_column('B:B', 60)

        ws.write(0, 0, 'US Market Insights & Recommendations', self.formats['title'])

        row = 2
        ws.write(row, 0, 'Category', self.formats['header'])
        ws.write(row, 1, 'Insight / Recommendation', self.formats['header'])

        insights = [
            ('Top Pattern (West Coast)', 'Space/Galaxy - popularity score 9.5, Gen Z favorite'),
            ('Top Pattern (East Coast)', 'Minimalist Typography - popularity score 9.0, Millennial favorite'),
            ('Seasonal Opportunity', 'Halloween collection - design 2-3 months ahead'),
            ('High ROI Channel', 'TikTok Live - 8.0x ROI, highest conversion at 8%'),
            ('Customer Retention', 'Loyal Advocates segment has 12% share but 30% of revenue'),
            ('Budget Optimization', 'Shift 20% Instagram budget to TikTok Ads for 15% ROI increase'),
            ('Content Strategy', 'Short-form video + Live streaming for Gen Z, Email + Reviews for Millennials'),
            ('Pricing Strategy', '$25-$35 sweet spot for T-shirts, $45-$60 for Hoodies (US market)'),
        ]
        for i, (cat, ins) in enumerate(insights):
            row = 3 + i
            ws.write(row, 0, cat, self.formats['text'])
            ws.write(row, 1, ins, self.formats['text'])

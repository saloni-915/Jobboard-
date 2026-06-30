from django.contrib.sitemaps import Sitemap

from .models import Job


class JobSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Job.objects.filter(is_approved=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/job/{obj.pk}/"

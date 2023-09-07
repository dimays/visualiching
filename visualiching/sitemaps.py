from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        items_list = [
            "visual-i-ching-app-home",
            "visual-i-ching-app-about",
            "register",
            "visual-i-ching-app-new-reading",
            "visual-i-ching-app-purchase-credits",
            "login",
            "password_reset",
        ]
        return items_list

    def location(self, item):
        return reverse(item)
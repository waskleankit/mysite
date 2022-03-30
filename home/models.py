from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey

from wagtail.api import APIField

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel
    ,PageChooserPanel ,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel,StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from streams import blocks

from rest_framework.fields import Field


class HomePageCarouselImages(Orderable):
    """between 1 and 5 images for hte home page carousel."""
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels=[
        ImageChooserPanel("carousel_image"),
    ]

    api_fields = [
        APIField("carousel_image"),
        # APIField("a_differrent_field_name"),
    ]


class BannerCTASerializer(Field):
    def to_representation(self, page):
        return {
            'id':page.id,
            'title': page.title,
            'first_published_at': page.first_published_at,
            # 'owner': page.owner.username,
            'owner': page.owner,
            # 'slug':page.slug,
            'url': page.url,
        }


class HomePage(RoutablePageMixin,Page):
    """Home page model"""
    templates = "home/home_page.html"
    subpage_types = [
        'blog.BlogListingPage',
        'contact.ContactPage',
        'flex.FlexPage',
    ]
    parent_page_type = [
        'wagtailcore.Page'
    ]
    # max_count = 1

    banner_title = models.CharField(max_length=100,blank=False,null=True)
    banner_subtitle = RichTextField(features=["bold","italic"])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"

    )

    content = StreamField(
        [
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    api_fields = [
        APIField("banner_title"),
        APIField("banner_subtitle"),
        APIField("banner_image"),
        APIField("banner_cta",serializer= BannerCTASerializer()),
        APIField("carousel_images"),
        APIField("content"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            ImageChooserPanel("banner_image"),
            PageChooserPanel("banner_cta"),
        ], heading="Banner Options"),
        MultiFieldPanel([
            InlinePanel("carousel_images",max_num=5,min_num=1,label="Image"),
        ], heading="Carousel Images"),
        StreamFieldPanel("content"),
    ]

    #Thisis how you'd normally hide promote and settings tabs
    # promote_panels = []
    # settings_panels = []

    banner_panels = [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            ImageChooserPanel("banner_image"),
            PageChooserPanel("banner_cta"),
        ], heading="Banner Options"),

    ]


    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels,heading='Custom'),
            ObjectList(Page.promote_panels, heading='Promotional Stuff'),
            ObjectList(Page.settings_panels, heading='Settings Stuff'),
            ObjectList(banner_panels, heading='Banner Settings'),
        ]
    )

    class Meta:

        verbose_name = "HOME PAGE"
        verbose_name_plural = "HOME PAGES"

    @route(r'^subscribe/$')
    def the_subscribe_page(self, request ,*args, **kwargs):
        context = self.get_context(request , *args, **kwargs)
        return render(request,"home/subscribe.html", context)
    def get_admin_display_title(self):
        return "Home "

# HomePage._meta.get_field("title").verbose_name = "To any verbouse name"
# HomePage._meta.get_field("title").help_text = "CUSTOM HELP TEXT"
# HomePage._meta.get_field("title").help_text = None
# HomePage._meta.get_field("title").default = "Some default title for Home Page"
# HomePage._meta.get_field("slug").default = "Some-default-title-for-Home-Page"
from django.db import models
from django.shortcuts import render
from django import forms
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.api import APIField

from wagtail.core.models import Page
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import \
    FieldPanel,\
    StreamFieldPanel,\
    MultiFieldPanel,\
    InlinePanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.models import Page ,Orderable
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet

from streams import blocks

from rest_framework.fields import Field
from taggit.models import TaggedItemBase

class ImageSerializedField(Field):
    """A custom serializer used in wagtail v2 API"""

    def to_representation(self, value):
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }


class BlogAUthorOrderable(Orderable):
    """ This us to select one or more blog authors from snippets"""
    page = ParentalKey("blog.BlogDetailPage",related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]

    @property
    def author_name(self):
        return self.author.name
    @property
    def author_website(self):
        return self.author.website

    @property
    def author_image(self):
        return self.author.image

    api_fields = [
        # APIField("author"),
        APIField("author_name"),
        APIField("author_website"),
        # APIField("author_image", serializer=ImageSerializedField()),
        APIField(
            "image_anything_test",
            serializer=ImageRenditionField(
                'fill-200x250',
                source="author_image")
        ),
    ]

class BlogAuthor(models.Model):
    """Blog autthor for snippet"""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True,null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete= models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading = "Name and Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading = "Links",
        )
    ]
    def __str__(self):
        """String reppresentation of this classs."""
        return self.name

    class Meta:
        verbose_name = " Blog Author"
        verbose_name_plural = "Blog Authors"

register_snippet(BlogAuthor)

class BlogCategory(models.Model):
    """  Blog actegory for a snipper. """

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text = "A slug to identify posts by this category",

    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        """String reppresentation of this classs."""
        return self.name

    class Meta:
        verbose_name = " Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

register_snippet(BlogCategory)



# class BannerCTASerializer(Field):
#     def to_representation(self, page):
#         return {
#             'id':page.id,
#             'title': page.title,
#             'first_published_at': page.first_published_at,
#             'owner': page.owner.username,
#             # 'owner': page.owner,
#             'slug':page.slug,
#             'url': page.url,
#         }


class BlogListingPage(RoutablePageMixin, Page):
    """Listing Page Lists all the Blog Detail Pages."""

    template = "blog/blog_listing_page.html"
    ajax_template = "blog/blog_listing_page_ajax.html"
    max_count = 1
    subpage_types = [
        'blog.VedioBlogPage',
        'blog.ArticleBlogPage',
    ]

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
        )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self,request, *args, **kwargs):
        """adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        #  "posts" will have child pages; you'll need to use . specific in thetemplate
        # in order to access child properties, such as youtube_video_id and subtitle
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')

        if request.GET.get('tag',None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])

        paginator = Paginator(all_posts, 2)   # @todo change to 5 per page
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        # context['posts'] = BlogDetailPage.objects.live().public()
        # context['a_special_link'] = self.reverse_subpage("latest_posts")
        context["authors"] = BlogAuthor.objects.all()
        context["categories"] = BlogCategory.objects.all()
        return context
    @route(r"^july-2019/$",name="july_2019")
    @route(r'^year/(\d+)/(\d+)/$', name="blogs_by_year")
    def blogs_by_year(self, request, year=None, month=None):
        context = self.get_context(request)
        print("july 2019")
        print(year)
        print(month)
        return render(request,"blog/latest_posts.html",context)

    @route(r'^searchall/$', name="searchallblog")
    def searchallblog(self, request ,*args, **kwargs):
        context = self.get_context(request , *args, **kwargs)
        """Find blog posts based on a category."""
        if request.method == "POST":
            if request.POST['sv'] != None:
                searchtag = request.POST['sv']
        # cat_slug = request.form[sv]
        context = self.get_context(request)
        context["posts"] = BlogDetailPage.objects.live().public().filter(title__contains=searchtag)
        context["posts"] = BlogDetailPage.objects.live().public().filter(custom_title__contains=searchtag)
        context["posts"] = BlogDetailPage.objects.live().public().filter(draft_title__contains=searchtag)
        context["posts"] = BlogDetailPage.objects.live().public().filter(content__contains=searchtag)
        context["posts"] = BlogDetailPage.objects.live().public().filter(slug__contains=searchtag)
        # | (slug__contains=searchtag) | (tags__contains=searchtag)
        # try:
        #     category = BlogCategory.objects.get(slug=searchtag)
        #     context["posts"] = BlogDetailPage.objects.live().public().filter(categories__in=[category])
        # except Exception:
        #     author = BlogAuthor.objects.get(name=searchtag)
        #     context["posts"] = BlogDetailPage.objects.live().public().filter(content__in=[searchtag])
        # except Exception:
        #     pass
        #
        # if category is None:
        #     #Redirect the user to /blog/
        #     pass
        return render(request, "blog/latest_posts.html", context)
    @route(r'^searchlink/(?P<auth_id>[-\w]*)/$', name="search_view")
    def search_view(self, request, auth_id):
        """Find blog posts based on a category."""
        context = self.get_context(request)
        # try:
        #     author = BlogAuthor.objects.get(id=auth_id)
        #     # print(author)
        # except Exception:
        #     author =None
        #
        # if author is None:
        #     #Redirect the user to /blog/
        #     pass
        # print(author.name)
        context["posts"] = BlogDetailPage.objects.live().public().filter(blog_authors__in=[auth_id])
        return render(request, "blog/latest_posts.html", context)


    # /blog/category
    @route(r'^category/(?P<cat_slug>[-\w]*)/$', name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on a category."""
        context = self.get_context(request)

        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            category =None

        if category is None:
            #Redirect the user to /blog/
            pass

        # print(category.name)
        context["posts"] = BlogDetailPage.objects.live().public().filter(categories__in=[category])
        return render(request, "blog/latest_posts.html", context)

    @route(r'^latest/$',name="latest_posts")
    def latest_blog_posts_only_shows_last_5(self, request ,*args, **kwargs):
        context = self.get_context(request , *args, **kwargs)
        # context["posts"] = context["posts"][:1]
        context['latest_posts'] = BlogDetailPage.objects.live().public()
        return render(request,"blog/latest_posts.html", context)

    def get_sitemap_urls(self, request):
        # uncomment to have no side maps in this page
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_posts"),
                "lastmod": (self.last_published_at  or self.latest_revision_created_at),
                "priority":0.9,
            }
        )
        return sitemap


    @route(r'^createblog/(?P<author>[-\w]*)/$', name="create_blog")
    def new_blog_creation(self, request, author):
        """creating new blog."""
        blogauthor = request.user.get_full_name()
        check = BlogAuthor.objects.filter(name = blogauthor).first()
        # print(check)
        # print(check.name)
        try:
            check.name == blogauthor
            # print(check)
            # print(blogauthor)
        except:
            last = BlogAuthor.objects.last()
            previd = last.id
            id = previd + 1
            name = request.user.get_full_name()
            website = "https://learnwagtail.com/"
            image_id = 5
            authorsave=BlogAuthor(id,name,website,image_id)
            authorsave.save();
        # else:
        #     print("else condition")




        subtitle = 1
        intro_image = "intro_image"
        custom_title = "custom_title"
        # subtitle = "subtitle"
        tags = "tags"
        banner_image = "banner_image"
        intro_image = "intro_image"
        author = "author"
        categories = "categories"
        content = "content"
        # articlebloginsert = BlogListingPage(subtitle,intro_image,custom_title,subtitle,tags,banner_image,intro_image,author,categories,content)
        # articlebloginsert.save();


        """blogs  name se esa kuch variable me sari values dalenge fir usko save """
        context = self.get_context(request)
        context["author"] = author
        context["categories"] = BlogCategory.objects.all()
        return render(request, "blog/create_blog.html", context)



class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogDetailPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogDetailPage(Page):
    """    Parental Blog detail page"""

    subpage_types = []
    parent_page_types = ['blog.BlogListingPage']
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
        )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    categories =ParentalManyToManyField("blog.BlogCategory",blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("tags"),
        ImageChooserPanel("banner_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors",label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="categories"
        ),
        StreamFieldPanel("content"),
    ]

    api_fields = [
        APIField("blog_authors"),
        APIField("content"),
        # APIField("banner_image"),
        # APIField("banner_cta"),
        # APIField("carousel_images"),
        # APIField("content"),
    ]

    def save(self, *args, **kwargs):
        key = make_template_fragment_key(
            "blog_post_preview",
            [self.id]
        )
        cache.delete(key)
        # key = make_template_fragment_key(
        #     "navigation",
        # )
        # cache.delete(key)
        return super().save(*args, **kwargs)


# First subclassed blog post page
class ArticleBlogPage(BlogDetailPage):
    """A subclassed blog post page for articles."""

    templates = "blog/article_blog_page.html"
    subtitle = models.CharField(
        max_length=100,
        default='',
        blank=True,
        null=True
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Best size for the image will be 1400x400'
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("subtitle"),
        FieldPanel("tags"),
        ImageChooserPanel("banner_image"),
        ImageChooserPanel("intro_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors",label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="categories"
        ),
        StreamFieldPanel("content"),
    ]


# Second subclassed page
class VedioBlogPage(BlogDetailPage):
    """A vedio subclassed page."""

    templates = "blog/video_blog_page.html"
    youtube_vedio_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("tags"),
        ImageChooserPanel("banner_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors",label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="categories"
        ),
        FieldPanel("youtube_vedio_id"),
        StreamFieldPanel("content"),
    ]


# name = request.user.username

        # check = BlogAuthor.objects.filter(name=author)
        # check.id
        # print(check)
        # print(check.id)
        # print(BlogAuthor.objects.all())

    # title = request.POST['name']
    # description = request.POST['desc']
    # date_created = timezone.now()
    # category_id = request.POST['category']
    # image_upload = request.FILES['img_name']
    # try:
    #     name = request.user
    #     email = request.user.email
    # except:
    #     name = None
    #     email =None
    # user = Users.objects.filter(email = email).first()
    # userid = user.user_id
    # latest_post = Posts.objects.latest('id')
    # id=latest_post.id + 1
    # post=Posts(id,title,description,date_created,category_id,userid,image_upload)
    # post.save();



    # @route(r'^createblog/(?P<author>[-\w]*)/$', name="create_blog")
    # def new_blog_creation(self, request, author):
    #     """creating new blog."""
    #     context = self.get_context(request)
    #     context["author"] = author
    #     context["categories"] = BlogCategory.objects.all()
    #     return render(request, "blog/create_blog.html", context)




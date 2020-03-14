from django.db import models
from django.db import connection


class Author(models.Model):
    class Meta():
        ordering = ["first_name", "last_name"]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True, verbose_name="e-mail")
    last_accessed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def _get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    full_name = property(_get_full_name)


# class Author2(models.Model):
#     salutation = models.CharField(max_length=10)
#     name = models.CharField(max_length=200)
#     email = models.EmailField()
#     headshot = models.ImageField(upload_to='author_headshots')
#
#     def __str__(self):
#         return self.name


class PublisherManager(models.Manager):
    def count_books(self):
        result_list = []
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    select 
                           p.id,
                           p.name,
                           p.address,
                           p.city,
                           p.state_province,
                           p.country,
                           p.website,
                           count(*) as amount
                    from books_publisher as p, books_book as b
                    where p.id = b.publisher_id
                    group by p.name
                    order by b.publication_date desc;
                """
            )
            for r in cursor.fetchall():
                publisher = self.model(
                    id=r[0],
                    name=r[1],
                    address=r[2],
                    city=r[3],
                    state_province=r[4],
                    country=r[5],
                    website=r[6]
                )
                publisher.amount = r[7]
                result_list.append(publisher)
        return result_list


class Publisher(models.Model):
    class Meta():
        ordering = ["name"]

    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField(max_length=200)
    objects = models.Manager()
    publisher_manager = PublisherManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        print("保存之前做些事情")
        super(Publisher, self).save(*args, **kwargs)
        print("保存之后做些事情")


class BookManager(models.Manager):
    def title_count(self, keyword):
        return self.filter(title__icontains=keyword).count()


class FlaskManager(models.Manager):
    def get_queryset(self):
        return super(FlaskManager, self).get_queryset().filter(title__icontains="flask")


class PythonManager(models.Manager):
    def get_queryset(self):
        return super(PythonManager, self).get_queryset().filter(title__icontains="python")


class Book(models.Model):
    class Meta():
        ordering = ["publication_date"]

    title = models.CharField(max_length=100)
    publication_date = models.DateField(blank=True, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)
    objects = models.Manager()
    title_count = BookManager()
    python_filter = PythonManager()
    flask_filter = FlaskManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title.find("低俗") != -1:
            super(Book, self).save(*args, **kwargs)
        else:
            return


def dictfetchall(cursor):
    desc = cursor.description
    result = [dict(zip((fn[0] for fn in desc), row)) for row in cursor.fetchall()]
    return result


def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("select * from books_author;")
        result = dictfetchall(cursor)
        cursor.execute("select * from books_author;")
        result2 = cursor.fetchall()
    return result, result2


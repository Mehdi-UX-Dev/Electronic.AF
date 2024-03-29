import os
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image as PilImage, ImageFilter, ImageOps


TYPES = [("LT", "Laptop"), ("DT", "Desktop")]
MEMORY_CAPACITIES = [
    ("4", "4GB"),
    ("8", "8GB"),
    ("16", "16GB"),
    ("32", "32GB"),
    ("64", "64GB"),
    ("128", "128GB"),
]
STORAGE_CAPACITIES = [
    ("256", "256GB"),
    ("512", "512GB"),
    ("1000", "1TB"),
    ("2000", "2TB"),
    ("4000", "4TB"),
]
VENDORS = [
    ("dell", "DELL"),
    ("hp", "HP"),
    ("apple", "APPLE"),
    ("asus", "ASUS"),
    ("lenovo", "LENOVO"),
    ("msi", "MSI"),
]
STORAGE_TYPES = [("1", "HDD"), ("2", "SSD")]
STARS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
ORDER_STATES = [("P", "Pending"), ("OD", "OutForDelivery"), ("D", "Delivered")]
PROVINCES = (
    ("BDK", "Badakhshan"),
    ("BDG", "Badghis"),
    ("BGH", "Baghlan"),
    ("BLK", "Balkh"),
    ("BAM", "Bamyan"),
    ("DYK", "Daykundi"),
    ("FRH", "Farah"),
    ("FRB", "Faryab"),
    ("GHZ", "Ghazni"),
    ("GHR", "Ghor"),
    ("HEL", "Helmand"),
    ("HRT", "Herat"),
    ("JZJ", "Jowzjan"),
    ("KBL", "Kabul"),
    ("KDR", "Kandahar"),
    ("KPS", "Kapisa"),
    ("KST", "Khost"),
    ("KNR", "Kunar"),
    ("KDZ", "Kunduz"),
    ("LGH", "Laghman"),
    ("LGR", "Logar"),
    ("NGR", "Nangarhar"),
    ("NMZ", "Nimruz"),
    ("NRT", "Nuristan"),
    ("ORZ", "Oruzgan"),
    ("PTI", "Paktia"),
    ("PTK", "Paktika"),
    ("PJR", "Panjshir"),
    ("PRW", "Parwan"),
    ("SMG", "Samangan"),
    ("SRP", "Sar-e-Pol"),
    ("TKH", "Takhar"),
    ("WDK", "Wardak"),
    ("ZBL", "Zabul"),
)


class Product(models.Model):
    title = models.CharField("Product name", max_length=255)
    type = models.CharField(max_length=2, choices=TYPES)
    vendor = models.CharField(max_length=55, choices=VENDORS, default="dell")
    model = models.CharField(max_length=4,default='2016')
    cpu = models.CharField(max_length=255)
    gpu = models.CharField(max_length=255)
    memory = models.CharField(max_length=3, choices=MEMORY_CAPACITIES)
    storage = models.CharField(max_length=4, choices=STORAGE_CAPACITIES)
    storage_type = models.CharField(max_length=1, choices=STORAGE_TYPES)
    os = models.CharField(max_length=55, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title

    def get_images(self):
        product_images = Image.objects.filter(product=self)
        if product_images.exists():
            return product_images
        return None


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    thumbnail = models.ImageField(upload_to="products/tumbnails", blank=True)

    def __str__(self) -> str:
        return f"image of {self.product.title}"

    def create_thumbnail(self):
        if not self.image:
            return
        THUMBNAIL_SIZE = (600, 450)

        if self.image.name.endswith(".jpg"):
            PIL_TYPE = "jpeg"
            FILE_EXTENSION = "jpg"
            DJANGO_TYPE = "image/jpeg"

        elif self.image.name.endswith(".png"):
            PIL_TYPE = "png"
            FILE_EXTENSION = "png"
            DJANGO_TYPE = "image/png"

        image = PilImage.open(BytesIO(self.image.read()))
        image.thumbnail(THUMBNAIL_SIZE, PilImage.ANTIALIAS)
        image = ImageOps.exif_transpose(image.filter(ImageFilter.GaussianBlur(4)))
        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)
        suf = SimpleUploadedFile(
            os.path.split(self.image.name)[-1],
            temp_handle.read(),
            content_type=DJANGO_TYPE,
        )
        self.thumbnail.save(
            "%s_thumbnail.%s" % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False,
        )

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            self.create_thumbnail()
        super(Image, self).save()


def deleteFilesFromDisk(instance, **kwargs):
    if instance.image:
        instance.image.delete(False)
    if instance.thumbnail:
        instance.thumbnail.delete(False)


pre_delete.connect(deleteFilesFromDisk, sender=Image)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def cart_id(self) -> int:
        return self.cart.id

    def __str__(self) -> str:
        return self.product.title


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"cart of {self.user.get_full_name() or self.user.email.split('@')[0]}"

    def get_items(self):
        items = CartItem.objects.filter(cart=self)
        return items

    def get_total_price(self):
        total = 0
        if len(self.get_items()) > 0:
            for item in self.get_items():
                total += item.product.price * item.quantity
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    province = models.CharField(max_length=3, choices=PROVINCES)
    district = models.CharField(max_length=55)
    home_address = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=9)

    def __str__(self) -> str:
        return f"Address of user {self.user.get_full_name()}"


class Order(models.Model):
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    cart = models.OneToOneField(Cart, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=ORDER_STATES, default="P")
    timestamp = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f"Order of user {self.cart.user.email}"


class CustomerReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    review = models.TextField(blank=True)
    rating = models.IntegerField(choices=STARS)

    def __str__(self) -> str:
        return f"Review for product ${self.product.title}"

    def get_average_rating(self):
        reviews = CustomerReview.objects.filter(product=self.product)
        if reviews.exists():
            total = 0
            for review in reviews:
                total += int(review.rating)
            return (total / reviews.count(), reviews.count())
        else:
            return (0, 0)

    def get_user_identifier(self):
        if self.user.get_full_name() != "":
            return self.user.get_full_name()
        else:
            return self.user.email.split("@")[0]

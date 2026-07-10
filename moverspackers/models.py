from django.db import models
from django.contrib.auth.models import User


# ================= AGENTS =================
class Agent(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else "Agent"


# ================= SITE USER / BOOKING =================
class SiteUser(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=15, null=True)
    location = models.CharField(max_length=50, null=True)
    shiftingloc = models.CharField(max_length=200, null=True)

    # ✅ USER INPUT DATE
    shiftingdate = models.DateField(null=True)

    briefitems = models.CharField(max_length=200, null=True)
    items = models.TextField(null=True)

    # ✅ SYSTEM DATE
    requestdate = models.DateTimeField(null=True)

    remarks = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=50, null=True)
    updatedate = models.DateTimeField(null=True)

    # ================= 🔥 SERVICE CONNECTION =================
    service = models.ForeignKey('Services', on_delete=models.SET_NULL, null=True, blank=True)

    # ================= AGENT ASSIGNMENT =================
    assigned_agent = models.ForeignKey(
        Agent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )

    # ================= 💰 PAYMENT FIELDS =================
    total_amount = models.FloatField(null=True, blank=True)
    advance_paid = models.FloatField(null=True, blank=True)

    PAYMENT_STATUS = (
        ("Pending", "Pending"),
        ("Partial", "Partial"),
        ("Completed", "Completed"),
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    def __str__(self):
        return self.name if self.name else "Booking"


# ================= SERVICES =================
class Services(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    image = models.FileField(null=True, blank=True)  # optional 👍
    price = models.FloatField(null=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title) if self.title else "Service"


# ================= CONTACT =================
class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    contact_no = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    subject = models.CharField(max_length=200, null=True)
    message = models.TextField(null=True)

    messagedate = models.DateField(auto_now_add=True)
    isread = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.name else "Query"
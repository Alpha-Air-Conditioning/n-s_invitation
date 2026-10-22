from django.db import models

class RSVP(models.Model):
    ATTENDANCE_CHOICES = [("yes", "Attending"), ("no", "Declined")]
    SIDE_CHOICES = [
        ("Bride's Side", "Bride's Side"),
        ("Groom's Side", "Groom's Side"),
        ("Family Friend", "Family Friend"),
    ]
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, blank=True)
    guests = models.PositiveSmallIntegerField(default=1)
    side = models.CharField(max_length=30, choices=SIDE_CHOICES, blank=True)
    attendance = models.CharField(max_length=3, choices=ATTENDANCE_CHOICES, default="yes")
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.get_attendance_display()}"

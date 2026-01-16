from django.db import models
from django.contrib.auth.models import User

class HormonalTwin(models.Model):
    """Model for connecting women with similar hormonal issues"""
    HORMONE_ISSUES = [
        ('PCOS', 'Polycystic Ovary Syndrome (PCOS)'),
        ('Endometriosis', 'Endometriosis'),
        ('Thyroid', 'Thyroid Disorder'),
        ('Irregular_Cycle', 'Irregular Menstrual Cycle'),
        ('Heavy_Bleeding', 'Heavy Menstrual Bleeding'),
        ('Hormonal_Acne', 'Hormonal Acne'),
        ('Low_Estrogen', 'Low Estrogen'),
        ('High_Testosterone', 'High Testosterone'),
        ('PMS', 'Premenstrual Syndrome (PMS)'),
        ('PMDD', 'Premenstrual Dysphoric Disorder (PMDD)'),
        ('Perimenopause', 'Perimenopause'),
        ('Other', 'Other Hormonal Issues'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hormonal_twin_profile')
    primary_issue = models.CharField(max_length=50, choices=HORMONE_ISSUES)
    secondary_issues = models.CharField(max_length=200, blank=True, help_text="Comma-separated list of other issues")
    bio = models.TextField(max_length=500, blank=True, help_text="Share a bit about your journey")
    profile_picture = models.ImageField(upload_to='twin_profiles', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.primary_issue}"
    
    def get_matches(self):
        """Get other users with the same primary hormonal issue"""
        return HormonalTwin.objects.filter(
            primary_issue=self.primary_issue
        ).exclude(id=self.id)[:20]


class TwinConnection(models.Model):
    """Model for connections between hormonal twins"""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='twin_connections_sent')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='twin_connections_received')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('connected', 'Connected'),
            ('blocked', 'Blocked'),
        ],
        default='pending'
    )
    connected_at = models.DateTimeField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, help_text="Optional message when connecting")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user1.username} <-> {self.user2.username} ({self.status})"

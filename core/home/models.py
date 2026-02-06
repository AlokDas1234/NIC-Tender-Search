from django.db import models
from django.contrib.auth.models import User

class ScraperControl(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_running = models.BooleanField(default=False)
    searching_state_name = models.CharField(max_length=250,null=True,blank=True)
    searching_key = models.CharField(max_length=350,null=True,blank=True)


class Client(models.Model):
    site_url = models.URLField(max_length=350,null=True,blank=True)
    search_key = models.TextField(null=True,blank=True)
    exclude_key = models.TextField(null=True,blank=True)
    state_name = models.CharField(max_length=350,null=True,blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


class Search(models.Model):
    site_url = models.URLField(max_length=500,null=True,blank=True)
    search_key = models.TextField(null=True,blank=True)
    exclude_key = models.TextField(null=True,blank=True)
    state_name = models.CharField(max_length=250,null=True,blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


class TenderResults(models.Model):
    # search_time=models.CharField(max_length=150,null=True,blank=True)
    search_time=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    tender_id = models.CharField(max_length=250,null=True,blank=True)
    state_name=models.CharField(max_length=250,null=True,blank=True)
    search_key=models.CharField(max_length=350,null=True,blank=True)
    site_link=models.CharField(max_length=250,null=True,blank=True)
    work_description=models.TextField(null=True,blank=True)
    organization_chain = models.TextField(null=True,blank=True)
    bid_submission_end_date = models.CharField(max_length=100,null=True,blank=True)
    bid_submission_end_time = models.CharField(max_length=100,null=True,blank=True)
    tender_value = models.CharField(max_length=150,null=True,blank=True)
    emd_amt = models.CharField(max_length=150,null=True,blank=True)
    tender_fee = models.CharField(max_length=250,null=True,blank=True)
    # user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

class SiteName(models.Model):
    state_name= models.CharField(max_length=250,null=True,blank=True)
    site_url = models.CharField(max_length=350,null=True,blank=True)
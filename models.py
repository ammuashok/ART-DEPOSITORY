from django.db import models

# Create your models here.
class Creator(models.Model):
    Name=models.CharField(max_length=100)
    Gender=models.CharField(max_length=100)
    DOB=models.DateField()
    ContactNo=models.IntegerField()
    Email=models.EmailField()
    Password=models.CharField(max_length=100)
    usertype=models.CharField(default="creator",max_length=10)
    otp=models.IntegerField(null=True,blank=True)
class usermodel(models.Model):
    Name=models.CharField(max_length=100)
    Gender=models.CharField(max_length=100)
    DOB=models.DateField(null=True)
    Adress=models.CharField(max_length=100)
    ContactNo=models.IntegerField()
    Email=models.EmailField()
    Password=models.CharField(max_length=100)
    usertype=models.CharField(default="user",max_length=10)
    otp=models.IntegerField(null=True,blank=True)
class loginmodel(models.Model):
    Email=models.EmailField()
    Password=models.CharField(max_length=100)
class CreatorHomepage(models.Model):
    ArtCatogory=models.CharField(max_length=100)
    Image=models.FileField(upload_to='image/')
    Amount=models.IntegerField()
    ArtDetails=models.CharField(max_length=100)
    CurrentDate=models.DateField(auto_now_add=True,null=True)
    CreatorId=models.ForeignKey(Creator,on_delete=models.CASCADE,null=True)
    sellstatus=models.IntegerField(default=0)
class bid(models.Model):
    bidid=models.AutoField(primary_key=True)
    CreatorId=models.ForeignKey(CreatorHomepage,on_delete=models.CASCADE,null=True)
    userid=models.ForeignKey(usermodel,on_delete=models.CASCADE,null=True)
    sellstatus=models.IntegerField(default=0)
    CurrentDate=models.DateField(auto_now_add=True,null=True)
class CreatorBid(models.Model):
    biddingid=models.AutoField(primary_key=True)
    productid=models.ForeignKey(CreatorHomepage,on_delete=models.CASCADE,null=True)
    creatorid=models.ForeignKey(Creator,on_delete=models.CASCADE,null=True)
    CurrentDate=models.DateField(auto_now_add=True,null=True)
    Bidstartdate=models.DateField()
    Bidstarttime=models.TimeField()
    Bidendtime=models.TimeField()
class Auction(models.Model):
    Auctionid=models.AutoField(primary_key=True)
    productid=models.ForeignKey(CreatorHomepage,on_delete=models.CASCADE,null=True)
    userid=models.ForeignKey(usermodel,on_delete=models.CASCADE,null=True)
    Amount=models.IntegerField()
    status=models.IntegerField(default=0)
    sellstatus=models.IntegerField(default=0)
class payment(models.Model):
    paymentid=models.AutoField(primary_key=True)
    Cardno=models.IntegerField()
    nameoncard=models.CharField(max_length=100)
    expiredate=models.DateField()
    totalamount=models.IntegerField()
    currentdate=models.DateField(auto_now_add=True,null=True)
    cvv=models.IntegerField()
    userid=models.ForeignKey(usermodel,on_delete=models.CASCADE,null=True)
    prooductid=models.ForeignKey(CreatorHomepage,on_delete=models.CASCADE,null=True)
    
class WishList(models.Model):
    wishlist_id=models.AutoField(primary_key=True)
    art_id=models.ForeignKey(CreatorHomepage,on_delete=models.CASCADE,null=True)
    user_id=models.ForeignKey(usermodel,on_delete=models.CASCADE,null=True)
    current_date=models.DateField(auto_now_add=True)


class UserComplaint(models.Model):
    complaint_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(usermodel,on_delete=models.CASCADE,null=True)
    subject=models.CharField(max_length=100)
    complaint=models.CharField(max_length=500)
    complaint_date=models.DateField(auto_now_add=True)
    reply=models.CharField(max_length=100)

class ArtistComplaint(models.Model):
    complaint_id=models.AutoField(primary_key=True)
    artist_id=models.ForeignKey(Creator,on_delete=models.CASCADE,null=True)
    subject=models.CharField(max_length=100)
    complaint=models.CharField(max_length=500)
    complaint_date=models.DateField(auto_now_add=True)
    reply=models.CharField(max_length=100)






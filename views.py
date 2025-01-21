from django.shortcuts import render,get_object_or_404,redirect
from .forms import CreatorRegistrationForm,UserRegistrationForm,loginform,CreatorHomepageForm,CreatorBidForm,AuctionForm, PaymentForm, ComplaintForm, ReplayForm, ArtistComplaintForm, ArtistReplayForm
from .models import Creator,usermodel,loginmodel,CreatorHomepage,bid,CreatorBid,Auction,WishList, UserComplaint, ArtistComplaint
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages


def creator_registration(request):
    if request.method=='POST':
        form=CreatorRegistrationForm(request.POST)
        if form.is_valid():
            
            form.save()
            
            return redirect('homeindex')
    else:
        form=CreatorRegistrationForm()
    return render(request,'creator_reg.html',{'form':form})

def art_list(request):
    list=Creator.objects.all()
    return render(request,'sample.html',{'art':list})
def delete_data(request,art_id):
    instance=get_object_or_404(Creator,id=art_id)
    instance.delete()
    return redirect('art')
def edit_data(request,art_id):
    instance=get_object_or_404(Creator,id=art_id)
    form=CreatorRegistrationForm(request.POST or None,instance=instance)
    if form.is_valid():
           form.save()
           return redirect('art_list')
    return render(request,'edit.html',{'art':form})

 #Create your views here.
def user_registration(request):
    if request.method=='POST':
        form2=UserRegistrationForm(request.POST)
        if form2.is_valid():
           form2.save()
           return redirect('homeindex')
    else:
        form2=UserRegistrationForm()
    return render(request,'user_reg.html',{'form2':form2})

def art_list1(request):
    list=usermodel.objects.all()
    return render(request,'sampleuser.html',{'art1':list})
def delete_data(request,art_id):
    instance=get_object_or_404(usermodel,id=art_id)
    instance.delete()
    return redirect('art1')
def edit_data(request,art_id):
    instance=get_object_or_404(usermodel,id=art_id)
    form=UserRegistrationForm(request.POST or None,instance=instance)
    if form.is_valid():
           form.save()
           return redirect('art_list1')
    return render(request,'edituser.html',{'art1':form})


def userload(request):
    id=request.session['userid']
    public=usermodel.objects.get(pk=id)
    if public:
        wishlist_count = WishList.objects.filter(user_id=public).count()
    else:
        wishlist_count = 0
    
    context = {
        'wishlist_count': wishlist_count,
    }
    
    return render(request, 'user_page.html', context)

def adminload(request):
    return render(request,'admin_page.html')

def loginload(request):
    return render(request,'login_page.html')

def homeindex(request):
    return render(request,'homeindex.html')
def artist(request):
    message = request.GET.get('message', '')
    return render(request,'artist.html', {'message': message})

def adminheader(request):
    return render(request,'adminheader.html')

def userheader(request):
    return render(request,'userheader.html')

def artistheader(request):
    return render(request,'artistheader.html')


def loginindex1(request, usertype):
    if usertype == "user":
        if request.method == "POST":
            form = loginform(request.POST)

            if form.is_valid():
                email = form.cleaned_data['Email']
                password = form.cleaned_data['Password']

                try:
                    user = usermodel.objects.get(Email=email,Password=password)
                    request.session['userid'] = user.id
                    request.session['Name'] = user.Name

                    return redirect('userload')

                except ObjectDoesNotExist:
                    form.add_error(None, 'Invalid Username or Password')

        else:
            form = loginform()

        return render(request, 'login_page.html', {'form': form})
    
    if usertype == "creator":
        if request.method == "POST":
            form = loginform(request.POST)

            if form.is_valid():
                email = form.cleaned_data['Email']
                password = form.cleaned_data['Password'] 

                try:
                    creator = Creator.objects.get(Email=email, Password=password)
                    request.session['creatorid'] = creator.id
                    request.session['creatorname']=creator.Name
                    return redirect('artist')

                except ObjectDoesNotExist:
                    form.add_error(None, 'Invalid Username or Password')

        else:
            form = loginform()

        return render(request, 'login_page.html', {'form': form})
    
def update_user_profile(request):
    user=request.session.get('userid')
    mydata=usermodel.objects.get(pk=user)
    if request.method=='POST':
        form=UserRegistrationForm(request.POST,instance=mydata)
        if form.is_valid():
            form.save()
            return redirect('userload')
    else:
        form=UserRegistrationForm(instance=mydata)
    return render(request,'updateuser.html',{'form':form})

def update_creator_profile(request):
    creator=request.session.get('creatorid')
    mydata=Creator.objects.get(pk=creator)
    if request.method=='POST':
        form=CreatorRegistrationForm(request.POST,instance=mydata)
        if form.is_valid():
            form.save()
            return redirect('update_creator_profile')
    else:
        form=CreatorRegistrationForm(instance=mydata)
    return render(request,'creatorupdate.html',{'form':form})    

def adminuserview(request):
    form=usermodel.objects.all()
    return render(request,'adminuserview.html',{'form':form})
def adminartistview(request):
    form=Creator.objects.all()
    return render(request,'adminartistview.html',{'form':form})

def  creator_myartview(request):
    id=request.session.get("creatorid")
    name=request.session.get("creatorname")
    creator=get_object_or_404(Creator,pk=id)
    print(creator.Name)
    form=CreatorHomepage.objects.filter(CreatorId=id)
    return render(request,'creator_myartview.html',{'form':form,'name':creator})
def deletecreator(request,pk):
    instance= CreatorHomepage.objects.get(id=pk)
    instance.delete()
    return redirect('creator_myartview')
def editcreator(request,pk):
    instance=get_object_or_404(CreatorHomepage,id=pk)
    form=CreatorHomepageForm(request.POST or None,instance=instance)
    if form.is_valid():
           form.save()
           return redirect('creator_myartview')
    return render(request,'editmyart.html',{'form':form})
# def  userartview(request):
#     form=CreatorHomepage.objects.all()
#     return render(request,'userartview.html',{'form':form})
def userartview(request):
    artworks = CreatorHomepage.objects.filter(sellstatus=0)
    user_id = request.session.get('userid')
    artworks_with_wishlist_status = []    
    for artwork in artworks:
        if user_id is not None and WishList.objects.filter(art_id=artwork, user_id=user_id).exists():
            in_wishlist = True
        else:
            in_wishlist = False
        artworks_with_wishlist_status.append({
            'artwork': artwork,
            'in_wishlist': in_wishlist,
        })
    
    # Pass the list to the template
    return render(request, 'userartview.html', {'artworks': artworks_with_wishlist_status})


def bidding(request,id):
    instance=request.session.get('userid')
    var=usermodel.objects.get(pk=instance)
    instance1=get_object_or_404(CreatorHomepage,pk=id)
    form=bid.objects.create(userid=var,CreatorId=instance1)
    return redirect('userload')
# def biddetails(request):
#     instance=request.session.get('creatorid')
#     data=get_object_or_404(Creator,pk=instance)
#     var=bid.objects.filter(CreatorId__CreatorId=data)
#     return render(request,'artistbiddetailsview.html',{'var':var})

  # Adjust the import based on your app structure

from django.db.models import Count, Q, Max, OuterRef, Subquery


def biddetails(request):
    user_id = request.session.get('creatorid')
    if user_id is not None:
        creator_arts = CreatorHomepage.objects.filter(CreatorId=user_id)
        bid_info = CreatorBid.objects.filter(productid=OuterRef('pk')).values('Bidstartdate', 'Bidstarttime', 'Bidendtime')[:1]
        
        products = creator_arts.annotate(
            total_bids=Count('bid'),
            total_participants=Count('bid__userid', filter=Q(bid__sellstatus=0), distinct=True),
            bid_start_date=Subquery(bid_info.values('Bidstartdate')),
            bid_start_time=Subquery(bid_info.values('Bidstarttime')),
            bid_end_time=Subquery(bid_info.values('Bidendtime'))
        )

        return render(request, 'artistbiddetailsview.html', {'products': products})
    else:
        return HttpResponse("User session not found.")

def view_participants(request, art_id):
    art_piece = CreatorHomepage.objects.get(pk=art_id)
    participants = bid.objects.filter(CreatorId=art_piece).select_related('userid')

    return render(request, 'participant_list.html', {'art_piece': art_piece, 'participants': participants})
    
def bidparticipants(request, id):
    creator_homepage = get_object_or_404(CreatorHomepage, pk=id)
    auctions = Auction.objects.filter(productid=creator_homepage)
    highest_bid = auctions.order_by('-Amount').first()
    participants = []
    for auction in auctions:
        participant = {
            'user': auction.userid,
            'amount': auction.Amount,
            'status': 'Active' if auction.status == 0 else 'Left',
            'sellstatus': auction.sellstatus
        }
        participants.append(participant)
    
    return render(request, 'participants.html', {
        'participants': participants,
        'highest_bid': highest_bid,
    })




from django.utils import timezone

import pytz
from django.utils import timezone


# current_time_utc = timezone.now()
# mumbai_timezone = pytz.timezone('Asia/Kolkata')
# current_time_mumbai = current_time_utc.astimezone(mumbai_timezone)
# print(current_time_mumbai)

def biddetailsview(request):
    user_id = request.session.get('userid')
    user1=get_object_or_404(usermodel,pk=user_id)
    if user_id is not None:
        user_instance = get_object_or_404(usermodel, pk=user1.pk)
        bids = bid.objects.filter(userid=user_instance)
        
        # Get current time in Mumbai timezone
        mumbai_timezone = pytz.timezone('Asia/Kolkata')
        current_time_utc = timezone.now()
        current_time_mumbai = current_time_utc.astimezone(mumbai_timezone)
        current_date_mumbai = current_time_mumbai.date()
        current_time_mumbai_only = current_time_mumbai.time()
        
        for b in bids:
            creator_bid = CreatorBid.objects.filter(productid=b.CreatorId).first()
            auction = Auction.objects.filter(productid=b.CreatorId).first()
            if creator_bid:
                b.bid_start_date = creator_bid.Bidstartdate 
                b.bid_start_time = creator_bid.Bidstarttime
                b.bid_end_time = creator_bid.Bidendtime
                b.is_coming_soon = b.bid_start_date > current_date_mumbai or (b.bid_start_date == current_date_mumbai and b.bid_start_time > current_time_mumbai_only)
                b.is_active = b.bid_start_date == current_date_mumbai and b.bid_start_time <= current_time_mumbai_only and b.bid_end_time >= current_time_mumbai_only
                b.sellstatus = auction.sellstatus if auction else 0

        context = {
            'bids': bids,
            'current_date': current_date_mumbai,
            'current_time': current_time_mumbai_only,
        }

        return render(request, 'userbiddetailsview.html', context)
    else:
        return HttpResponse("User session not found.")

    
def deletebid(request,pk):
    instance= get_object_or_404(bid,bidid=pk)
    instance.delete()
    return redirect('biddetailsview')
def creatorbidding(request,id):
    instance=request.session.get('creatorid')
    var=Creator.objects.get(pk=instance)
    instance1=get_object_or_404(CreatorHomepage,pk=id)
    if request.method=='POST':
        form=CreatorBidForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.creatorid=var
            f.productid=instance1
            f.save()
            return redirect('biddetails')
    else:
        form=CreatorBidForm()
    return render(request,'biddateandtime.html',{'form':form})
def auction(request, CreatorId):
    user_id = request.session.get('userid')
    if user_id is None:
        return HttpResponse("User session not found.")

    user_instance = get_object_or_404(usermodel, pk=user_id)
    item_instance = get_object_or_404(CreatorHomepage, pk=CreatorId)
    current_auctions = Auction.objects.filter(productid=item_instance)
    highest_bid = current_auctions.order_by('-Amount').first()
    highest_bid_amount = highest_bid.Amount if highest_bid else item_instance.Amount
    user_auction = current_auctions.filter(userid=user_instance).first()

    if request.method == 'POST':
        form = AuctionForm(request.POST)
        
        if form.is_valid():
            new_bid_amount = form.cleaned_data['Amount']
            if new_bid_amount <= highest_bid_amount:
                form.add_error('Amount', f"Bid amount must be greater than {highest_bid_amount}.")
            elif user_auction and new_bid_amount <= user_auction.Amount:
                form.add_error('Amount', "You must bid a higher amount than your previous bid.")
            else:
                if user_auction: 
                    user_auction.Amount = new_bid_amount
                    user_auction.save()
                else:
                    f = form.save(commit=False)
                    f.userid = user_instance
                    f.productid = item_instance
                    f.save()
                return redirect('auction', CreatorId=CreatorId)
    else:
        form = AuctionForm()
    user_status = current_auctions.filter(userid=user_instance).first()
    leave_participants = current_auctions.filter(status=1)

    return render(request, 'bidamount.html', {
        'form': form,
        'var': current_auctions,
        'statuss': user_status,
        'highest_bid_amount': highest_bid_amount,
        'leave_participants': leave_participants,
    })



def Leave(request):
    user_id = request.session.get('userid')
    user_instance = get_object_or_404(usermodel, pk=user_id)
    
    user_auctions = Auction.objects.filter(userid=user_instance, status=0)

    user_auctions.update(status=1)

    return redirect('userload')

def artist_bid_details_view(request, pk):
    instance = get_object_or_404(CreatorHomepage, pk=pk)
    auctions = Auction.objects.filter(productid=instance).order_by('-Amount')
    highest_bid = auctions.first()

    participants = []
    for auction in auctions:
        participant = {
            'user': auction.userid,
            'amount': auction.Amount,
            'status': 'Active' if auction.status == 0 else 'Left',
            'sellstatus': auction.sellstatus,
            'productid': auction.productid.pk
        }
        participants.append(participant)

    return render(request, 'bid_details.html', {
        'participants': participants,
        'highest_bid': highest_bid,
    })

def artistsell(request, id):
    creator_homepage = get_object_or_404(CreatorHomepage, pk=id)
    highest_bid = Auction.objects.filter(productid=creator_homepage).order_by('-Amount').first()
    
    if highest_bid:
        highest_bid.sellstatus = 1
        highest_bid.save()
    url= request.META.get('HTTP_REFERER')
    if url:
        return redirect(url)

def addtowishlist(request, id):
    instance = request.session.get('userid')
    var = usermodel.objects.get(pk=instance)
    instance1 = get_object_or_404(CreatorHomepage, pk=id)
    try:
        wishlist_item = WishList.objects.get(art_id=instance1, user_id=var)
        wishlist_item.delete()
    except WishList.DoesNotExist:
        WishList.objects.create(art_id=instance1, user_id=var)
    
    return redirect('userartview')


def viewwishlist(request):
    instance = request.session.get('userid')
    var = usermodel.objects.get(pk=instance)
    data = WishList.objects.filter(user_id=var)
    return render(request, "wishlist.html", {'data': data})

    



def art_payment(request, auction_id):
    print(f"Received auction_id: {auction_id}")
    auction1 = get_object_or_404(CreatorHomepage, pk=auction_id)
    print(auction1)
    user_id = request.session.get('userid')
    user = get_object_or_404(usermodel, pk=user_id)
    print(user)
    payment_successful = False
    
    auction = get_object_or_404(Auction, productid=auction1.pk, userid=user.pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_instance = form.save(commit=False)
            payment_instance.userid = user
            payment_instance.prooductid = auction1  
            payment_instance.totalamount = auction.Amount
            payment_instance.save()
            
            auction.sellstatus = 2 
            auction.save()

            payment_successful = True

            return redirect('biddetailsview')  
    else:
        form = PaymentForm(initial={'totalamount': auction.Amount})

    return render(request, 'art_payment.html', {
        'form': form,
        'amount': auction.Amount,
        'payment_successful': payment_successful
    })

def user_complaint(request):
    id=request.session['userid']
    public=usermodel.objects.get(pk=id)
    if request.method=='POST':
        form=ComplaintForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.user_id=public
            f.save()
            return redirect('user_complaint_view')
    else:
        form=ComplaintForm()
    return render(request,'usercomplaint.html',{'form':form})
    
def user_complaint_view(request):
    id=request.session['userid']
    public=usermodel.objects.get(pk=id)
    form=UserComplaint.objects.filter(user_id=public)
    return render(request,'usercomplaintview.html',{'form':form})

def complaint_edit(request,pk):
    instance=UserComplaint.objects.get(complaint_id=pk)
    form=ComplaintForm(request.POST or None,instance=instance)
    if form.is_valid():
        form.save()
        return redirect('user_complaint_view')
    return render(request,'usercomplaintedit.html',{'form':form})

def complaint_delete(request,pk):
    var=UserComplaint.objects.get(complaint_id=pk)
    var.delete()
    return redirect('user_complaint_view')

def adminusercomplaintview(request):
    form=UserComplaint.objects.all()
    return render(request,'adminusercomplaintview.html',{'complaints':form})               

def complaint_replay(request,pk):
   if request.method=='POST':
        Compliant=get_object_or_404( UserComplaint,complaint_id=pk)
        form= ReplayForm(request.POST)
        if form.is_valid():
            v=form.cleaned_data['reply']
            Compliant.reply=v
            Compliant.save()
            return redirect('adminusercomplaintview')
   else:
        form=ReplayForm()
   return render(request,'user_complaint_reply.html',{'form':form})


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('index')


def artist_complaint(request):
    id=request.session['creatorid']
    artist=Creator.objects.get(pk=id)
    if request.method=='POST':
        form=ArtistComplaintForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.artist_id=artist
            f.save()
            return redirect('artist_complaint_view')
    else:
        form=ArtistComplaintForm()
    return render(request,'artistcomplaint.html',{'form':form})
    
def artist_complaint_view(request):
    id=request.session['creatorid']
    creator=Creator.objects.get(pk=id)
    form=ArtistComplaint.objects.filter(artist_id=creator)
    return render(request,'artistcomplaintview.html',{'form':form})

def artist_complaint_edit(request,pk):
    instance=ArtistComplaint.objects.get(complaint_id=pk)
    form=ArtistComplaintForm(request.POST or None,instance=instance)
    if form.is_valid():
        form.save()
        return redirect('artist_complaint_view')
    return render(request,'artistcomplaintedit.html',{'form':form})

def artist_complaint_delete(request,pk):
    var=ArtistComplaint.objects.get(complaint_id=pk)
    var.delete()
    return redirect('artist_complaint_view')

def adminartistcomplaintview(request):
    form=ArtistComplaint.objects.all()
    return render(request,'adminartistcomplaintview.html',{'complaints':form})               

def artist_complaint_replay(request,pk):
   if request.method=='POST':
        Compliant=get_object_or_404( ArtistComplaint,complaint_id=pk)
        form= ArtistReplayForm(request.POST)
        if form.is_valid():
            v=form.cleaned_data['reply']
            Compliant.reply=v
            Compliant.save()
            return redirect('adminartistcomplaintview')
   else:
        form=ArtistReplayForm()
   return render(request,'artist_complaint_reply.html',{'form':form})


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------


import os
import logging
import datetime
from io import BytesIO
from urllib.parse import urlencode

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from django.conf import settings
from PIL import Image, ImageChops, ImageDraw, ImageFont

from .models import Creator, CreatorHomepage
from .forms import CreatorHomepageForm

logger = logging.getLogger(__name__)


def get_database_image_paths(creator_id):
    """
    Retrieve paths of images previously uploaded by the creator from the database.
    """
    try:
        creator_homepages = CreatorHomepage.objects.filter(CreatorId=creator_id)
        user_image_paths = []

        # Assuming that 'Image' is a FileField or ImageField in your model
        for homepage in creator_homepages:
            if homepage.Image:
                # Generate a path for the image; adjust if necessary based on how paths are stored
                image_path = os.path.join(settings.MEDIA_ROOT, homepage.Image.name)
                user_image_paths.append(image_path)

        return user_image_paths

    except Exception as e:
        logger.error(f"Error retrieving user image paths from database: {e}")
        raise

def is_image_unique_in_database(uploaded_image, dataset_path, user_image_paths):
    """
    Check if the uploaded image is unique compared to images in the dataset
    and images previously uploaded by the same user.
    """
    try:
        # Check against dataset
        for img_path in os.listdir(dataset_path):
            dataset_image_path = os.path.join(dataset_path, img_path)
            logger.debug(f"Checking image against dataset: {dataset_image_path}")
            dataset_image = Image.open(dataset_image_path)
            if uploaded_image.size != dataset_image.size:
                logger.debug(f"Size mismatch with {img_path}. Skipping this image.")
                continue
            diff = ImageChops.difference(uploaded_image, dataset_image)
            if not diff.getbbox():
                logger.info(f"Image is not unique. It matches with dataset image {img_path}.")
                return False

        # Check against user-uploaded images
        for img_path in user_image_paths:
            logger.debug(f"Checking image against user-uploaded images: {img_path}")
            user_image = Image.open(img_path)
            if uploaded_image.size != user_image.size:
                logger.debug(f"Size mismatch with {img_path}. Skipping this image.")
                continue
            diff = ImageChops.difference(uploaded_image, user_image)
            if not diff.getbbox():
                logger.info(f"Image is not unique. It matches with user-uploaded image {img_path}.")
                return False

        logger.info("Image is unique.")
        return True

    except Exception as e:
        logger.error(f"An error occurred during image uniqueness check: {e}")
        raise


def add_watermark(image_file, creator_name):
    try:
        with Image.open(image_file) as img:
            width, height = img.size
            watermark_text = f"{creator_name}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Font setup
            try:
                font_path = "arialbd.ttf"  # Update this to the path of your font file
                font_size = int(min(width, height) * 0.05)
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                font = ImageFont.load_default()

            draw = ImageDraw.Draw(img)
            lines = watermark_text.split('\n')

            # Calculate maximum width and height needed for watermark
            max_line_width = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)
            total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines) + (len(lines) - 1) * 10

            # Positioning: Bottom Right Corner
            x = width - max_line_width - 10
            y = height - total_text_height - 10

            for i, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font)
                line_height = bbox[3] - bbox[1]
                draw.text((x, y + i * (line_height + 10)), line, font=font, fill=(255, 255, 255, 255))  # White color

            # Save watermarked image to a BytesIO object
            watermarked_image_io = BytesIO()
            img.save(watermarked_image_io, format='JPEG')
            watermarked_image_io.seek(0)
            return watermarked_image_io
    except Exception as e:
        logger.error(f"Error adding watermark: {e}")
        raise




def save_image_to_dataset(image_file, dataset_path):
    try:
        # Ensure dataset path exists
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
        
        destination_path = os.path.join(dataset_path, image_file.name)
        
        # Save the image to the dataset directory
        with open(destination_path, 'wb') as dest_file:
            for chunk in image_file.chunks():
                dest_file.write(chunk)
        
        logger.info(f"Image successfully saved to dataset: {destination_path}")
    except Exception as e:
        logger.error(f"Failed to save image to dataset: {e}")
        raise



def myart(request):
    logger.debug("Starting myart view...")

    creator_id = request.session.get('creatorid')
    logger.debug(f"Retrieved Creator ID from session: {creator_id}")

    if not creator_id:
        logger.warning("No creator ID found in session. Redirecting to login.")
        return redirect('login')

    try:
        logger.debug(f"Attempting to retrieve Creator object with ID {creator_id}...")
        creator = Creator.objects.get(pk=creator_id)
        logger.debug(f"Creator found: {creator}")
    except Creator.DoesNotExist:
        logger.warning(f"Creator with ID {creator_id} does not exist. Redirecting to login.")
        return redirect('login')

    if request.method == 'POST':
        logger.debug("Handling POST request for form submission...")
        form = CreatorHomepageForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug("Form submission is valid.")
            image_file = request.FILES['Image']
            logger.debug(f"Received image file: {image_file.name}")
            uploaded_image = Image.open(image_file)

            # Paths for checking uniqueness
            dataset_path = r'D:\auction_12_08_with_val\auction\myproject\dataset'
            user_image_paths = get_database_image_paths(creator_id)

            logger.debug(f"Checking image uniqueness against dataset and user uploads...")
            if is_image_unique_in_database(uploaded_image, dataset_path, user_image_paths):
                logger.debug("Image is unique. Proceeding to save the image and form instance.")
                
                # Save the unique image to the dataset
                save_image_to_dataset(image_file, dataset_path)

                # Optionally add watermark if needed
                watermarked_image_io = add_watermark(image_file, creator.Name)
                watermarked_image_file = InMemoryUploadedFile(
                    watermarked_image_io, 
                    'ImageField', 
                    image_file.name, 
                    'image/jpeg', 
                    watermarked_image_io.getbuffer().nbytes, 
                    None
                )

                form_instance = form.save(commit=False)
                form_instance.CreatorId = creator
                form_instance.Image = watermarked_image_file
                form_instance.save()
                logger.debug("Form instance saved successfully. Redirecting to artist page.")

                return redirect(f'/artist/?message=Image%20is%20unique%20and%20has%20been%20successfully%20uploaded!')

            else:
                message = urlencode({'message': 'The image uploaded is already uploaded by another user or is not found unique. Please upload a unique image.'})
                return redirect(f'/myart/?{message}')

        else:
            message = urlencode({'message': 'Form is invalid. Please correct the errors and try again.'})
            return redirect(f'/myart/?{message}')
    else:
        logger.debug("Handling GET request. Rendering the form for the first time.")
        form = CreatorHomepageForm()

    logger.debug("Rendering myart.html template with the form.")
    return render(request, 'myart.html', {'form': form})


def purchase(request, auction_id):
    auction1 = get_object_or_404(CreatorHomepage, pk=auction_id)
    user_id = request.session.get('userid')
    user = get_object_or_404(usermodel, pk=user_id)
    payment_successful = False

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_instance = form.save(commit=False)
            payment_instance.userid = user
            payment_instance.prooductid = auction1
            payment_instance.totalamount = auction1.Amount
            payment_instance.save()
            auction1.sellstatus = 1
            auction1.save()
            payment_successful = True
    else:
        form = PaymentForm(initial={'totalamount': auction1.Amount})

    return render(request, 'art_payment.html',{
        'form': form,
        'amount': auction1.Amount,
        'payment_successful': payment_successful})

import random
from django.core.mail import send_mail
from .forms import PasswordResetRequestForm
from .forms import OTPVerificationForm
from .forms import SetNewPasswordForm
def send_otp(Email):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    if Creator.objects.filter(Email=Email):
        gadgetotp=Creator.objects.filter(Email=Email).first()
        gadgetotp.otp=otp
        gadgetotp.save()
    else:
        gadgetotp=usermodel.objects.filter(Email=Email).first()
        gadgetotp.otp=otp
        gadgetotp.save()
        
    subject = 'Your Password Reset OTP'
    message = f'Your OTP for password reset is {otp}.'
    send_mail(subject, message, 'examplemail@gmail.com',[Email])
    return otp

def get_user_by_email(Email):
    try:
        return Creator.objects.get(Email=Email)
    except Creator.DoesNotExist:
        pass

    try:
        return usermodel.objects.get(Email=Email)
    except usermodel.DoesNotExist:
        pass
    return None

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            Email = form.cleaned_data['Email']
            user = get_user_by_email(Email)
            if user:
                otp = send_otp(Email)
                request.session['otp'] = otp
                request.session['Email'] = Email
                return redirect('password-resetverify')
            else:
                form.add_error('email', 'Email does not exist.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password_reset_request.html', {'form': form})

def password_reset_verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            saved_otp = request.session.get('otp')
            if entered_otp == str(saved_otp):
                return redirect('password-resetnew')
            else:
                form.add_error('otp', 'Invalid OTP.')
    else:
        form = OTPVerificationForm()
    return render(request, 'password_reset_verify_otp.html', {'form': form})

def password_reset_form(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            Email = request.session.get('Email')
            user = get_user_by_email(Email)
            if user:
                user.Password = new_password
                user.save()
                user_type = user.usertype  # Retrieve the usertype from the user object
                return redirect(f'/loginindex1/{user_type}')
            else:
                form.add_error(None, 'Something went wrong.')
    else:
        form = SetNewPasswordForm()
    return render(request, 'password_reset_form.html', {'form': form})
from django.urls import path
from .views import userload,adminload,loginload
from django.conf.urls.static import static
from django.conf import settings

from .views import creator_registration,user_registration,art_list,delete_data,edit_data,art_list1,loginindex1,update_user_profile,homeindex,artist,update_creator_profile,adminheader,userheader,artistheader
from .views import adminuserview,adminartistview,myart,creator_myartview,deletecreator,editcreator,userartview,bidding,biddetails,biddetailsview,user_complaint_view,complaint_delete,adminusercomplaintview,artist_complaint
from .views import deletebid,creatorbidding,auction,Leave,artist_bid_details_view,artistsell,addtowishlist,viewwishlist,bidparticipants,art_payment, user_complaint,complaint_edit,complaint_replay,logout_view,artist_complaint_view
from .views import artist_complaint_edit,artist_complaint_delete,adminartistcomplaintview,artist_complaint_replay,view_participants,purchase,password_reset_request,password_reset_verify_otp,password_reset_form
urlpatterns = [
    path('',homeindex,name='homeindex'),
    path('index',homeindex,name='index'),
    path('userload/',userload,name='userload'),
    path('adminload/',adminload,name='adminload'),
    path('loginload/',loginload,name='loginload'),
    path('loginindex1/<str:usertype>/',loginindex1,name='loginindex1'),
    path('update_user_profile/',update_user_profile,name='update_user_profile'),
    path('creator_registration/',creator_registration,name='creator_registration'),
    path('user_registration/',user_registration,name='user_registration'),
    path('art/',art_list,name='art'),
    path('delete/<int:pk>/',delete_data,name='delete_data'),
    path('edit/<int:pk>/',edit_data,name='edit_data'),
    path('art1/',art_list1,name='art1'),
    path('artist/',artist,name='artist'),
    path('update_creator_profile/',update_creator_profile,name='update_creator_profile'),
    path('adminheader/',adminheader,name='adminheader'),
    path('userheader/',userheader,name='userheader'),
    path('artistheader/',artistheader,name='artistheader'),
    path('adminuserview/',adminuserview,name='adminuserview'),
    path('adminartistview/',adminartistview,name='adminartistview'),
    path('myart/',myart,name='myart'),
    path('creator_myartview/',creator_myartview,name='creator_myartview'),
    path('deletecreator/<int:pk>/',deletecreator,name='deletecreator'),
    path('editcreator/<int:pk>/',editcreator,name='editcreator'),
    path('userartview/',userartview,name='userartview'),
    path('bidding/<int:id>/',bidding,name='bidding'),
    path('biddetails/',biddetails,name='biddetails'),
    path('biddetailsview/',biddetailsview,name='biddetailsview'),
    path('deletebid/<int:pk>',deletebid,name='deletebid'),
    path('creatorbidding/<int:id>/',creatorbidding,name='creatorbidding'),
    path('auction/<int:CreatorId>/',auction,name='auction'),
    path('Leave/',Leave,name='Leave'),
    path('artist_bid_details_view/<int:pk>/', artist_bid_details_view, name='artist_bid_details_view'),
    path('view_participants/<int:art_id>/',view_participants, name='view_participants'),
    path('artistsell/<int:id>/',artistsell, name='artistsell'),
    
    path('addtowishlist/<int:id>/', addtowishlist, name='addtowishlist'),
    path('viewwishlist/',viewwishlist,name="viewwishlist"),
    path('bidparticipants/<int:id>',bidparticipants,name="bidparticipants"),
    path('payment/<int:auction_id>/', art_payment, name='payment'),


    path('user_complaint/',user_complaint,name='user_complaint'),
    path('user_complaint_view/',user_complaint_view,name='user_complaint_view'),
    path('complaint_delete/<int:pk>',complaint_delete,name='complaint_delete'),
    path('complaint_edit/<int:pk>',complaint_edit,name='complaint_edit'),
    path('complaint_replay/<int:pk>',complaint_replay,name='complaint_replay'),
    path('adminusercomplaintview/',adminusercomplaintview,name='adminusercomplaintview'),
    path('purchase/<int:auction_id>/',purchase,name="purchase"),

    path('artist_complaint/',artist_complaint,name='artist_complaint'),
    path('artist_complaint_view/',artist_complaint_view,name='artist_complaint_view'),
    path('artist_complaint_edit/<int:pk>',artist_complaint_edit,name='artist_complaint_edit'),
    path('artist_complaint_delete/<int:pk>',artist_complaint_delete,name='artist_complaint_delete'),
    path('adminartistcomplaintview/',adminartistcomplaintview,name='adminartistcomplaintview'),
    path('artist_complaint_replay/<int:pk>',artist_complaint_replay,name='artist_complaint_replay'),
    
    path('password-reset/',password_reset_request, name='password-reset'),
    path('password-resetverify/',password_reset_verify_otp, name='password-resetverify'),
    path('password-resetnew/', password_reset_form, name='password-resetnew'),


    path('logout/', logout_view, name='logout'),

    

    

    
          
          


   
 ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
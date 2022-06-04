from email.mime import base
from django.urls import path,include
from Products import views

from rest_framework import routers


router = routers.DefaultRouter()
router.register('cart',views.MyCart,basename="MyCart")
router.register('orders',views.OrderViewset,basename="OrderViewset")


urlpatterns = [

    path("",include(router.urls)),
    #Category part
    path('categories/', views.CategoriesViewSet.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoriesUpdateDelete.as_view(), name='categories_update_delete'),
    
    #Sub Category part
    path('sub_categories/', views.SubCategoriesViewSet.as_view(), name='sub_categories'),
    path('sub_categories/<int:pk>/', views.SubCategoriesUpdateDelete.as_view(),name='sub_categories_update_delete'),

    # product part 
    path('product/', views.ProductListViewSet.as_view(), name='products' ),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create' ),
    path('product/<slug:slug>/', views.ProductRetUpDesViewSet.as_view(), name='products_delete_update' ),

    # supplier part 
    path('supplier/', views.SupplierView.as_view(), name='supplier' ),
    path('supplier/<int:pk>/', views.SupplierUpdateDelete.as_view(), name='supplier_update_delete' ),

    # Brand part 
    path('brand/', views.BrandView.as_view(), name='brand' ),
    path('brand/<int:pk>/', views.BrandUpdateDelete.as_view(), name='brand_update_delete' ),


    #Country part 
    path('countries/', views.CountryView.as_view(), name='country' ),
    path('countries/<int:pk>/', views.CountryUpdateDelete.as_view(), name='country_update_delete' ),

    #Country part 
    path('stock/', views.StockView.as_view(), name='stock' ),
    path('stock/<int:pk>/', views.StockUpdateDelete.as_view(), name='stock_update_delete' ),
    
    # cart part
    path("addtocart/",views.AddtoCartView.as_view(),name="addtocart"),
    path('updatecart/',views.Updatecart.as_view(),name='updatecart'),
    path('editcart/',views.Editcart.as_view(),name='editcart'),
    path('deletecart/',views.DeleteCart.as_view(),name='deleltecart'),
    
] 

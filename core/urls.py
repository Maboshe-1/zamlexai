from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_view, name='input'),
    path('article/<str:article_id>/', views.article_detail, name='article_detail'),
    path('case/<str:case_id>/', views.case_detail, name='case_detail'),
    path('refine/', views.refine_argument, name='refine_argument'),
    path('augment/', views.augment_argument, name='augment_argument'),
    path('contracts/',views.contract_list,        name='contract_list'),
    path("load/<int:pk>/", views.load_scenario, name="load_scenario"),
    path('draft/will/', views.will_view, name='will_draft'),
    path('draft/petition/', views.petition_view, name='petition_draft'),
    path('contracts/nda/',        views.nda_view,        name='contract_nda'),
    path('contracts/sale/',       views.sale_view,       name='contract_sale'),
    path('contracts/lease/',      views.lease_view,      name='contract_lease'),
    path('contracts/employment/', views.employment_view, name='contract_employment'),
]
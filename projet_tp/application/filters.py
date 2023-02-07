import django_filters
from .models import Product , Client , Fournisseur , Facture , Bon_Livraison , Commande

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {"Type_produit" : ['exact']}

class ProductStockFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {"Type_produit" : ['exact'] }

class FournisseurFilter(django_filters.FilterSet):
    class Meta:
        model = Fournisseur
        fields = {"Solde_Fournisseur" : ['gt' , 'lt']}

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = {"Credit" : ['gt' , 'lt']}

class FactureFilter(django_filters.FilterSet):
    class Meta:
        model = Facture
        fields = {"Date_Facture" : ['gt' , 'lt']}

class BLFilter(django_filters.FilterSet):
    class Meta:
        model = Bon_Livraison
        fields = {"Date_BL" : ['gt' , 'lt']}

class CommandeFilter(django_filters.FilterSet):
    class Meta:
        model = Commande
        fields = {"Date_BC" : ['gt' , 'lt']}


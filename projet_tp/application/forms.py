from django.forms import ModelForm
from django.forms import formset_factory
from django import forms
from .models import Product , Client , Product_type , Fournisseur , Stock , Vente , Effectuer_vente , Facture , Bon_Livraison , Commande , Etablire_facture , Etablire_BL , Commander

class ProductForm(ModelForm):
    class Meta : 
        model = Product
        fields = ['Nom_produit' , 'Type_produit']

        widget = {
            'Nom_produit': forms.TextInput(attrs={'class':'form-control ml-2'}),
            'Type_produit': forms.Select(attrs={'class':'form-control ml-2'})
        }

class ProductStockForm(ModelForm):
    class Meta : 
        model = Product
        fields = '__all__'
        exclude = ['factures' , 'commandes' , 'ventes' , 'BLs' , 'Motif' , 'Qte_destocker']
        # widget={
        #     'factures'  , 'commandes' , 'ventes' , 'BLs' , 'Motif' , 'Qte_destocker'
        # }

class TypeForm(ModelForm):
    class Meta : 
        model = Product_type
        fields = '__all__'

class ClientForm(ModelForm):
    class Meta : 
        model = Client
        fields = ['Nom_client' , 'Prenom_client' , 'Adr_client' , 'Tel_client']

class FournisseurForm(ModelForm):
    class Meta : 
        model = Fournisseur
        fields = ['Nom_Fournisseur' , 'Prenom_Fournisseur' , 'Adr_Fournisseur' , 'Tel_Fournisseur' , 'Email_Fournisseur']

class StockeForm(ModelForm):
    class Meta : 
        model = Stock
        fields = ['Adr_Stock']

    
class FactureForm(ModelForm):
    class Meta :
        model = Facture
        fields = ['Remise_Facture' , 'TVA' , 'Fournisseurs' , 'facture_payé']

class CommandeForm(ModelForm):
    class Meta :
        model = Commande
        fields = ['Fournisseur']

class BLForm(ModelForm):
    class Meta :
        model = Bon_Livraison
        fields = ['Remise_BL' , 'Fournisseurs' , 'BL_payé']

class EtablireFactureForm(ModelForm):
    class Meta :
        model = Etablire_facture
        fields = ['Produits' , 'Qte_Facture' , 'Prix_HT_Facture' , 'Prix_Vente_Facture']
        
Etablire_factureFormset = formset_factory(Etablire_facture, extra=1)

class EtablireBLForm(ModelForm):
    class Meta :
        model = Etablire_BL
        fields = ['Produits_BL' , 'Qte_BL' , 'Prix_HT_BL' , 'Prix_Vente_BL']

class EtablireCommandeForm(ModelForm):
    class Meta :
        model = Commander
        fields = ['Produits_cmd' , 'Qte_cmd']

class StockForm(ModelForm):
    class Stock:
        model = Stock
        fields = '__all__'

class VenteForm(ModelForm):
    class Meta:
        model = Vente
        fields = ['Client']


class EffectuerVenteForm(ModelForm):
    class Meta:
        model = Effectuer_vente
        fields = ['Produits_vente' , 'Qte_vente']

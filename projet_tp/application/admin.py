from django.contrib import admin
from .models import Product , Product_type , Fournisseur , Facture , Etablire_facture , Bon_Livraison , Etablire_BL , Commande , Commander , Client , Stock , Vente , Effectuer_vente

# Register your models here.
admin.site.register(Product)
admin.site.register(Product_type)
admin.site.register(Fournisseur)
admin.site.register(Facture)
admin.site.register(Etablire_facture)
admin.site.register(Bon_Livraison)
admin.site.register(Etablire_BL)
admin.site.register(Commande)
admin.site.register(Commander)
admin.site.register(Client)
admin.site.register(Stock)
admin.site.register(Vente)
admin.site.register(Effectuer_vente)


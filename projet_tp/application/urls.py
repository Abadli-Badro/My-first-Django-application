from django.urls import path
from . import views

urlpatterns = [
path('home/' , views.homepage , name='Home'),
    
path('dashboard/bestclients/' , views.bestclients , name='Best_Clients'),
path('dashboard/bestfournisseurs/' , views.bestfournisseurs , name='Best_Fournisseurs'),
path('dashboard/bestproducts/' , views.bestproducts , name='Best_Products'),

path('dashboard/evolution_benefice/' , views.evolution_benefice , name='evolution_benefice'),
path('dashboard/evolution_achat/' , views.evolution_achat , name='evolution_achat'),
path('dashboard/evolution_valeur/' , views.evolution_valeur , name='evolution_valeur'),
path('dashboard/produit_plusAchete/' , views.produit_plusAchete , name='produit_plusAchete'),

path('achat/' , views.achat , name='Achat'),
path('vente/' , views.vente , name='Vente'),
path('stock/' , views.stock , name='Stock'),

#------------------------Affichage---------------------------------- 
path('produits/',views.afficher_produits , name='ProdList'),
path('fournisseurs/',views.afficher_fournisseurs , name='FournisseursList'),
path('clients/',views.afficher_clients , name='ClientList'),
path('types/',views.afficher_types , name='TypeList'),
path('achat/bon_commande' , views.afficher_bon_commande , name='Bon_commande'),                             #affichage d'une liste des commandes
path('achat/bon_livraison' , views.afficher_bon_livraison , name='Bon_livraison'),                          #affichage d'une commande particulière
path('achat/facture' , views.afficher_facture , name='Facture'),                                            #affichage d'une liste des factures
path('achat/facture/afficher<int:pk>', views.afficher_contenu_facture, name="Afficher_facture"),            #affichage d'une facture particulière
path('achat/bon_livraison/afficher<int:pk>', views.afficher_contenu_BL, name="Afficher_BL"),                #affichage d'une liste des bons
path('achat/bon_commande/afficher<int:pk>', views.afficher_contenu_commande, name="Afficher_commande"),     #affichage d'un bon particulier
path('stock/afficher/<int:pk>' , views.afficher_produits_stock , name="Afficher_stock"),
path('vente/afficher/<int:pk>' , views.afficher_vente , name="Afficher_vente"),
path('vente/afficher_payer/<int:pk>' , views.afficher_vente_payer , name="Afficher_vente_payer"),
#------------------------Ajout--------------------------------------
path('produits/ajouter/', views.ajout_produit, name="Ajouter_produit"),
path('clients/ajouter/', views.ajout_client, name="Ajouter_client"),
path('types/ajouter/', views.ajout_type, name="Ajouter_type"),
path('stocks/ajouter/', views.ajout_stock, name="Ajouter_stock"),
path('fournisseurs/ajouter/', views.ajout_fournisseur, name="Ajouter_fournisseur"),
path('achat/facture/ajouter' , views.ajout_facture , name='Ajouter_facture'),
path('achat/facture/ajouter/etablire' , views.etablire_facture , name='Etablire_facture'),
path('achat/bon_commande/ajouter' , views.ajout_commande , name='Ajouter_commande'),
path('achat/bon_commande/ajouter/etablire' , views.etablire_commande , name='Etablire_Commande'),
path('achat/bon_livraison/ajouter' , views.ajout_BL , name='Ajouter_BL'),
path('achat/bon_livraison/ajouter/etablire' , views.etablire_BL , name='Etablire_BL'),
path('vente/ajouter/', views.ajout_vente, name="Ajouter_vente"),
path('vente/ajouter/chercher' , views.chercher_produit_vente , name='Chercher_vente'),
path('Stocker/ajouter/<int:pk>' , views.stocker , name='Stocker_produit'),
path('Stocker/qte/<int:pk>' , views.stocker_qte , name='Stocker_Qte'),
path('vente/ajouter/<int:pk>' , views.ajouter_produit_vente , name='Effectuer_Vente'),
#------------------------Edit---------------------------------------
path('produits/edit/<int:pk>', views.edit_produit, name="Edit_produit"),
path('fournisseurs/edit/<int:pk>', views.edit_fournisseur, name="Edit_fournisseur"),
path('clients/edit/<int:pk>', views.edit_client, name="Edit_client"),
path('types/edit/<int:pk>', views.edit_type, name="Edit_type"),
path('stocks/edit/<int:pk>', views.edit_stock, name="Edit_stock"),
path('achat/bon_commande/edit<int:pk>', views.edit_commande, name="Edit_commande"),
path('achat/bon_livraison/edit<int:pk>', views.edit_BL, name="Edit_bon_livraison"),
path('achat/facture/edit<int:pk>', views.edit_facture, name="Edit_facture"),
path('stock/edit/<int:pk>' , views.edit_produit_stock , name='Edit_Produit_Stock'),
#-----------------------Suppression---------------------------------
path('produits/delete/<int:pk>', views.supp_produit, name="Supp_produit"),
path('fournisseurs/delete/<int:pk>', views.supp_fournisseur, name="Supp_fournisseur"),
path('types/delete/<int:pk>', views.supp_type, name="Supp_type"),
path('stocks/delete/<int:pk>', views.supp_stock, name="Supp_stock"),
path('clients/delete/<int:pk>', views.supp_client, name="Supp_client"),
path('achat/bon_commande/delete<int:pk>', views.supp_commande, name="supp_commande"),
path('achat/bon_livraison/delete<int:pk>', views.supp_BL, name="supp_BL"),
path('achat/facture/delete<int:pk>', views.supp_facture, name="supp_facture"),
path('stock/déstocker/<int:pk>', views.destocker, name="déstocker"),
#-----------------------Réglements----------------------------------
path('achat/réglements' , views.réglements_achat , name='Réglements_achat'),
path('achat/réglements/<int:pk>' , views.régler_achat , name='Régler'),
path('vente/réglements/<int:pk>' , views.régler_vente , name='Régler_vente'),
path('vente/réglements/payer/<int:pk>' , views.payer_credit, name='Payer_credit'),
path('vente/réglements' , views.réglements_vente , name='Réglements_vente'),
path('achat/réglements/régler/f<int:pk>' , views.régler_facture , name='Régler_facture'),
path('achat/réglements/régler/bl<int:pk>' , views.régler_BL , name='Régler_BL'),
#-----------------------Recherche-----------------------------------
path('produits/rechercher',views.chercher_produit , name='Chercher_produit'),
path('fournisseurs/rechercher',views.chercher_fournisseur , name='Chercher_fournisseur'),
path('clients/rechercher',views.chercher_client , name='Chercher_client'),
path('achat/facture/rechercher',views.chercher_facture , name='Chercher_facture'),
path('achat/bon_livraison/rechercher',views.chercher_BL , name='Chercher_BL'),
path('achat/bon_commande/rechercher',views.chercher_commande , name='Chercher_commande'),
path('Stocker/<int:pk>-rechercher',views.chercher_produit_stocker , name='Chercher_stocker'),
#-----------------------Export(CSV)---------------------------------
path('produits/export_csv' , views.export_produits_csv , name="ExpProdCSV"),
path('clients/export_csv' , views.export_clients_csv , name="ExpClientCSV"),
path('fournisseurs/export_csv' , views.export_fournisseurs_csv , name="ExpFournisseursCSV"),
path('clients/export_csv' , views.export_types_csv , name="ExpTypesCSV"),
#-----------------------Export(PDF)---------------------------------
path('achat/facture/export/<int:pk>' , views.export_facture , name='ExpFacture'),
path('achat/bon_commande/export/<int:pk>' , views.export_commande , name='ExpCommande'),
path('achat/bon_livraison/export/<int:pk>' , views.export_bl , name='ExpBL'),
]

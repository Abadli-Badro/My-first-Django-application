from django.db import models

# Create your models here.

class Product_type(models.Model):
    Nom_type = models.CharField(max_length=50)
    def __str__(self):
        return self.Nom_type

class Stock(models.Model):
    Adr_Stock = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.Adr_Stock}'

class Product(models.Model):
    Nom_produit = models.CharField(max_length=50)
    Type_produit = models.ForeignKey(Product_type, on_delete = models.CASCADE)
    
    #Attributs de l'association 'Stocker' et 'Destocker'
    Qte_stocker = models.IntegerField(default=0)
    Date_stocker = models.DateField(auto_now_add=True , null= True , editable=True)
    Prix_HT_Produit = models.IntegerField(default=0)
    Prix_Vente_Produit = models.IntegerField(default=0)
    Qte_destocker = models.IntegerField(default=0)
    Motif = models.CharField(max_length=50 , default="")

    factures = models.ManyToManyField('Facture' , through='Etablire_facture')
    commandes = models.ManyToManyField('Commande' , through='Commander')
    ventes = models.ManyToManyField('Vente' , through='Effectuer_vente')
    BLs = models.ManyToManyField('Bon_Livraison' , through='Etablire_BL')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE , related_name= "produitsBL" , blank=True, null=True)
    def __str__(self):
        return self.Nom_produit

class Fournisseur(models.Model):
    Nom_Fournisseur = models.CharField(max_length=50)
    Prenom_Fournisseur = models.CharField(max_length=50)
    Adr_Fournisseur = models.CharField(max_length=50)
    Tel_Fournisseur = models.IntegerField()
    Email_Fournisseur = models.CharField(max_length=30)
    Solde_Fournisseur = models.IntegerField(default=0)
    def __str__(self):
        return self.Nom_Fournisseur

class Facture(models.Model):
    Remise_Facture = models.IntegerField(default=0)
    Date_Facture = models.DateField(auto_now_add= True)                         
    TVA = models.IntegerField(default=19)
    Fournisseurs = models.ForeignKey(Fournisseur, on_delete = models.CASCADE)
    produits = models.ManyToManyField('Product' , through='Etablire_facture')
    facture_payé = models.BooleanField(default=True)

class Etablire_facture(models.Model):
    Produits = models.ForeignKey(Product, on_delete = models.CASCADE , related_name= "produitsFACTURE")
    Factures = models.ForeignKey(Facture, on_delete = models.CASCADE , related_name= "facture")
    Qte_Facture = models.IntegerField()
    Prix_HT_Facture = models.IntegerField()
    Prix_Vente_Facture = models.IntegerField()

class Bon_Livraison(models.Model):
    Remise_BL = models.IntegerField(default=0)
    Date_BL = models.DateField(auto_now_add= True)                              
    Fournisseurs = models.ForeignKey(Fournisseur, on_delete = models.CASCADE)
    produits = models.ManyToManyField('Product' , through='Etablire_BL')
    BL_payé = models.BooleanField(default=True)

class Etablire_BL(models.Model):
    Produits_BL = models.ForeignKey(Product, on_delete = models.CASCADE , related_name= "produitsBL" , blank=True, null=True)
    BLs = models.ForeignKey(Bon_Livraison, on_delete = models.CASCADE , related_name= "BL" , blank=True, null=True)
    Qte_BL = models.IntegerField()
    Prix_HT_BL = models.IntegerField()
    Prix_Vente_BL = models.IntegerField()

class Commande(models.Model):
    Date_BC = models.DateField(auto_now_add= True)                              
    Fournisseur = models.ForeignKey(Fournisseur, on_delete = models.CASCADE)
    Produits = models.ManyToManyField('Product' , through='Commander')

class Commander(models.Model):
    Produits_cmd = models.ForeignKey(Product, on_delete = models.CASCADE , related_name= "produitsCmd", blank=True, null=True)
    commandes = models.ForeignKey(Commande, on_delete = models.CASCADE , related_name= "Cmd" , blank=True, null=True)
    Qte_cmd = models.IntegerField()

class Client(models.Model):
    Nom_client = models.CharField(max_length=50)
    Prenom_client = models.CharField(max_length=50)
    Adr_client = models.CharField(max_length=50)
    Tel_client = models.IntegerField()
    Credit = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.Nom_client} {self.Prenom_client}'

class Vente(models.Model):
    Montant = models.IntegerField(default=0)
    Date_Vente = models.DateField(auto_now_add=True)
    Client = models.ForeignKey(Client, on_delete = models.CASCADE)
    Produits = models.ManyToManyField('Product' , through='Effectuer_vente')

class Effectuer_vente(models.Model):
    Produits_vente = models.ForeignKey(Product, on_delete = models.CASCADE , related_name= "produit" , blank=True, null=True)
    Ventes = models.ForeignKey(Vente, on_delete = models.CASCADE , related_name= "vente" , blank=True, null=True)
    Qte_vente = models.IntegerField()




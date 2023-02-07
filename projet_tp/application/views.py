import csv , io
from django.shortcuts import render , redirect
from django.http import HttpResponse , FileResponse
from .forms import ProductForm ,ProductStockForm ,ClientForm , TypeForm , FournisseurForm , StockeForm , FactureForm , CommandeForm , BLForm , EtablireCommandeForm , EtablireBLForm , EtablireFactureForm , VenteForm , EffectuerVenteForm
from .models import Product , Fournisseur , Client , Stock , Vente , Product_type , Bon_Livraison , Commande , Facture , Etablire_BL , Etablire_facture , Commander , Effectuer_vente
from reportlab.pdfgen import canvas 
from reportlab.lib.pagesizes import letter 
from reportlab.lib.units import inch
from .filters import ProductFilter , ClientFilter, ProductStockFilter, FactureFilter , BLFilter , CommandeFilter , FournisseurFilter
from django.contrib import messages


def homepage(request):                                                                                   #Vers la page d'acceuil
    return render(request,'index.html')

def achat(request):                                                                                      #Vers la page des achats
    return render(request,'Achat.html')

def vente(request):   
    ventes = Vente.objects.all()      
    for vente in ventes:
        prod = []
        produits = Effectuer_vente.objects.all().filter(Ventes=vente)
        for produit in produits : 
            prod.append(produit.Produits_vente)
        if prod == []: 
            vente.delete()                                                              
    return render(request,'Vente.html' , {"ventes":ventes})

def stock(request):                                                                                      #Vers la page des stock
    stocks = Stock.objects.all()
    return render(request,'Stock.html',{"stocks":stocks})

#-------------------------------------------------------------Charts-------------------------------------------------------------

def evolution_benefice(request):                                                                            #Pour chaque jour on calcule le taux de bénifices
    ventes = Vente.objects.all()                                                                            #"Le total des bénifices des ventes établis le meme jour" 
    dates = []
    benifices = []
    for vente in ventes:
        produits = Effectuer_vente.objects.all().filter(Ventes = vente)
        totalV=0
        totalA=0
        for produit in produits:
            totalA += produit.Produits_vente.Prix_HT_Produit * produit.Qte_vente
            totalV += produit.Produits_vente.Prix_Vente_Produit * produit.Qte_vente
        benifice = totalV-totalA
        if dates.__contains__(vente.Date_Vente) == False:                                                   
            dates.append(vente.Date_Vente)
            benifices.append(benifice)
        else:
            if benifices:                                                                                   #si la bénifice déja calculé on la mis à jour
                benifice += benifices.pop(len(benifices)-1)
                benifices.append(benifice)
            else:
                benifices.append(benifice)
                benifice += benifices.pop(len(benifices)-1)
                benifices.append(benifice)
    return render(request, 'EvolutionBenefice.html' , {"Dates":dates , "Benifices":benifices})

def evolution_achat(request):
    factures = Facture.objects.all()                                                                            #"Le total des bénifices des facture établis le meme jour" 
    dates = []
    achats = []
    for facture in factures:
        produits = Etablire_facture.objects.all().filter(Factures = facture)
        totalA=0
        for produit in produits:
            totalA += produit.Prix_HT_Facture * produit.Qte_Facture
        if dates.__contains__(facture.Date_Facture) == False:                                                   
            dates.append(facture.Date_Facture)
            achats.append(totalA)
        else:
            if achats:                                                                                   #si la bénifice déja calculé on la mis à jour
                totalA += achats.pop(len(achats)-1)
                achats.append(totalA)
            else:
                achats.append(totalA)
                totalA += achats.pop(len(achats)-1)
                achats.append(totalA)
    return render(request, 'EvolutionAchat.html' , {"Dates":dates , "Achats":achats})

def evolution_valeur(request):
    ventes = Vente.objects.all()                                                                            #"Le total des bénifices des facture établis le meme jour" 
    dates = []
    totalVendu = []
    for vente in ventes:
        produits = Effectuer_vente.objects.all().filter(Ventes = vente)
        totalV=0
        for produit in produits:
            totalV += produit.Produits_vente.Prix_Vente_Produit * produit.Qte_vente
        if dates.__contains__(vente.Date_Vente) == False:                                                   
            dates.append(vente.Date_Vente)
            totalVendu.append(totalV)
        else:
            if totalVendu:                                                                                   #si la bénifice déja calculé on la mis à jour
                totalV += totalVendu.pop(len(totalVendu)-1)
                totalVendu.append(totalV)
            else:
                totalVendu.append(totalV)
                totalV += totalVendu.pop(len(totalVendu)-1)
                totalVendu.append(totalV)
    return render(request, 'EvolutionValeur.html' , {"Dates":dates , "Ventes":totalVendu})
    
def produit_plusAchete(request):
    produits = Product.objects.all()
    nbrAchat = []
    nomProduit = []
    for produit in produits:
        achats = Etablire_facture.objects.all().filter(Produits = produit)
        qte=0
        if achats:
            for achat in achats: qte += achat.Qte_Facture
            nbrAchat.append(qte)
            nomProduit.append(produit.Nom_produit)  
    return render(request, 'ProduitPlusAchte.html', {"Noms":nomProduit , "Nombre":nbrAchat})

def bestclients(request):   
    clients = Client.objects.all()
    nbrVentes = []
    nomClient = []
    for client in clients:
        ventes = Vente.objects.all().filter(Client = client)
        nbrVentes.append(len(ventes))
        nomClient.append(client.Nom_client)                                                                              
    return render(request,'BestClients.html' , {"Noms":nomClient , "Nombre":nbrVentes})

def bestproducts(request):  
    produits = Product.objects.all().filter(Prix_Vente_Produit__gt = 0)
    nbrVentes = []
    nomProduit = []
    for produit in produits:
        ventes = Effectuer_vente.objects.all().filter(Produits_vente = produit)
        qte=0
        for vente in ventes: qte += vente.Qte_vente
        nbrVentes.append(qte)
        nomProduit.append(produit.Nom_produit)                                                                                 
    return render(request,'BestProducts.html' , {"Noms":nomProduit , "Nombre":nbrVentes})

def bestfournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    nbrFactures = []
    nomFournisseur = []
    for fournisseur in fournisseurs:
        factures = Facture.objects.all().filter(Fournisseurs = fournisseur)
        nbrFactures.append(len(factures))
        nomFournisseur.append(fournisseur.Nom_Fournisseur)
    return render(request, 'BestFournisseurs.html' , {"Noms":nomFournisseur , "Nombre":nbrFactures})

#-----------------------------------------------------Affichage-------------------------------------------------------

def afficher_produits(request):                                                                          #Afficher les produits
    produits = Product.objects.all()
    filter = ProductFilter(request.GET , queryset = produits)
    return render(request,'liste_produits.html',{"products":filter})

def afficher_fournisseurs(request):                                                                      #Afficher les fournisseurs
    fournisseurs = Fournisseur.objects.all()
    return render(request,'liste_fournisseurs.html',{"fournisseurs":fournisseurs})

def afficher_clients(request):                                                                           #Afficher les clients
    clients = Client.objects.all()
    return render(request,'liste_clients.html',{"clients":clients})

def afficher_types(request):                                                                             #Afficher les types des produits
    types = Product_type.objects.all()
    return render(request,'liste_types.html',{"types":types})

def afficher_bon_commande(request):                                                                      #Afficher les commandes
    cmds = Commande.objects.all()
    filter = CommandeFilter(request.GET , queryset = cmds)
    request.session.clear()
    return render(request,'BonCommande.html',{"cmds":filter})

def afficher_bon_livraison(request):                                                                      #Afficher les bons des livraisons
    bls = Bon_Livraison.objects.all()
    filter = BLFilter(request.GET , queryset = bls)
    request.session.clear()
    return render(request,'BonLivraison.html',{"bons":filter})

def afficher_facture(request):                                                                            #Afficher les factures
    factures = Facture.objects.all()
    filter = FactureFilter(request.GET , queryset = factures)
    request.session.clear()
    return render(request,'Facture.html',{"factures":filter})

def afficher_contenu_BL(request , pk):                                                                    #Afficher le contenu d'un bon                                             
    BL = Bon_Livraison.objects.get(id=pk)   
    etablire = Etablire_BL.objects.all().filter(BLs = BL)   
    total_vente = 0
    total_achat = 0
    for produit in etablire :                       
        total_vente += (produit.Prix_Vente_BL * produit.Qte_BL)
        total_achat += (produit.Prix_HT_BL * produit.Qte_BL)
    prix_ttc = total_achat - total_achat * BL.Remise_BL/100  
    return render(request,'Afficher_BL_Facture_Cmd.html',{"BL":BL,"BL_etabli":etablire , "total_vente":total_vente , "total_achat":total_achat , "prix_ttc":prix_ttc})

def afficher_contenu_commande(request , pk): 
    commande = Commande.objects.get(id=pk)   
    etablire = Commander.objects.all().filter(commandes = commande)     
    return render(request,'Afficher_BL_Facture_Cmd.html',{"commande":commande,"commande_etabli":etablire})

def afficher_contenu_facture(request , pk): 
    facture = Facture.objects.get(id=pk)   
    etablire = Etablire_facture.objects.all().filter(Factures = facture)   
    total_vente = 0
    total_achat = 0
    for produit in etablire :                     
        total_vente += (produit.Prix_Vente_Facture * produit.Qte_Facture)
        total_achat += (produit.Prix_HT_Facture * produit.Qte_Facture)
    prix_ttc = total_achat + total_achat * facture.TVA /100 - total_achat * facture.Remise_Facture/100  
    return render(request,'Afficher_BL_Facture_Cmd.html',{"facture":facture,"facture_etabli":etablire , "total_vente":total_vente , "total_achat":total_achat , "prix_ttc":prix_ttc})

def afficher_vente(request , pk):
    vente = Vente.objects.get(id=pk) 
    vente_effectué = Effectuer_vente.objects.all().filter(Ventes = vente)
    total=0
    for p in vente_effectué :
        total += p.Produits_vente.Prix_Vente_Produit * p.Qte_vente
    return render(request , "AfficherVente.html" , {"vente":vente ,"list":vente_effectué , "total":total})

def afficher_vente_payer(request , pk):                                             #Afficher 'la vente' et gérer le payement
    vente = Vente.objects.get(id=pk) 
    vente_effectué = Effectuer_vente.objects.all().filter(Ventes = vente)
    total=0
    for p in vente_effectué :
        total += p.Produits_vente.Prix_Vente_Produit * p.Qte_vente  
    if request.method == "POST":
        montant = request.POST["montant"]
        vente.Montant = int(montant)
        for p in vente_effectué:
            p.Produits_vente.Qte_stocker -= p.Qte_vente                             #Actualiser le stock
            p.Produits_vente.save()
        if int(montant) < total:
            vente.Client.Credit += total - int(montant)
            vente.Client.save()
        vente.save()
        print(vente.Montant)
        return redirect("Vente")
    else: 
        return render(request , "AfficherVentePayer.html" , {"vente":vente ,"list":vente_effectué , "total":total})

def afficher_produits_stock(request , pk):                                                                  #Afficher les produits d'un stock particulier
    stk = Stock.objects.get(id=pk)   
    produits = Product.objects.all().filter(stock = stk)
    total_vente=0
    total_ht=0
    for produit in produits:
        total_ht += produit.Prix_HT_Produit * produit.Qte_stocker
        total_vente += produit.Prix_Vente_Produit * produit.Qte_stocker
    bénifice = total_vente - total_ht
    filter = ProductStockFilter(request.GET , queryset = produits)
    return render(request,'AfficherStock.html',{"produits":filter , "stock":stk , "total_ht":total_ht , "total_vente":total_vente , "benifice":bénifice})

#-----------------------------------------------------Ajout-------------------------------------------------------------

def ajout_produit(request):
    produit = True
    if request.method == 'POST':
        form = ProductForm(request.POST)                                                     #Récupérer les données de form
        if form.is_valid():                                                                  
            form.save()
            form = ProductForm()
            mssg="Produit ajouté avec succés!"                                                                   
            return render(request,"AjoutTables.html",{"form":form,"message":mssg , "produit":produit})        #Redirection vers la page d'ajout
    else:
        form = ProductForm()                                                                 #Créer une instance de formulaire vierge    --Premiére entrée dans la page (GET)--
        mssg =""
        return render(request,"AjoutTables.html",{"form":form,"message":mssg , "produit":produit})

def ajout_client(request):
    client = True
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            form = ClientForm()
            mssg="Client ajouté avec succés!"                                                                   
            return render(request,"AjoutTables.html",{"form":form,"message":mssg , "client":client})        
    else:
        form = ClientForm()                        
        mssg =""
        return render(request,"AjoutTables.html",{"form":form,"message":mssg , "client":client})

def ajout_type(request):
    type = True
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            form = TypeForm()
            mssg="Type produit ajouté avec succés!"                                                                   
            return render(request,"AjoutTables.html",{"form":form,"message":mssg , "type":type})        
    else:
        form = TypeForm()                        
        mssg = ""
        return render(request,"AjoutTables.html",{"form":form,"message":mssg , "type":type})

def ajout_fournisseur(request):
    fournisseur = True
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            form = FournisseurForm()
            mssg="Le fournisseur a été ajouté avec succés!"                                                                   
            return render(request,"AjoutTables.html",{"form":form,"message":mssg , "fournisseur":fournisseur})        
    else:
        form = FournisseurForm()                        
        mssg = ""
        return render(request,"AjoutTables.html",{"form":form,"message":mssg , "fournisseur":fournisseur})

def ajout_stock(request):
    stock = True
    if request.method == 'POST':
        form = StockeForm(request.POST)
        if form.is_valid():
            form.save()
            form = StockeForm()
            mssg="Le stock a été ajouté avec succés!"                                                                   
            return render(request,"AjoutTables.html",{"form":form,"message":mssg , "stock":stock})        
    else:
        form = StockeForm()                        
        mssg = ""
        return render(request,"AjoutTables.html",{"form":form,"message":mssg , "stock":stock})

def ajout_facture(request):
    if request.method == 'POST':
        form_facture = FactureForm(request.POST)
        if form_facture.is_valid():
            form_facture.save()
            form_facture = FactureForm()           
            factures = Facture.objects.latest('id')                     #Le dernier objet crée => l'objet crée dans le form      
            request.session['facture_id']= factures.id                  #Sauvegarder la clé de facture dans une session pour pouvoir l'utiliser après              
            return redirect("Etablire_facture")                         #Vers l'insertions des produits
    else:
        form_facture = FactureForm()                        
        return render(request,"AjouterFacture.html",{"formFacture":form_facture})

def etablire_facture(request):
    if request.method == 'POST':
        pk = request.session.get('facture_id')                          #récupérer la clé de facture concerné 
        form_facture = EtablireFactureForm(request.POST)
        if form_facture.is_valid():
            instance = form_facture.save(commit=False)                  #créer une instance sans l'ajouter dans la bdd (pour ajouter la facture)
            facture = Facture.objects.get(id = pk)
            total_achat = instance.Prix_HT_Facture * instance.Qte_Facture
            prix_ttc = total_achat + total_achat * facture.TVA /100 - total_achat * facture.Remise_Facture/100  
            if facture.facture_payé == False :                          #si la facture est non payée on ajoute le prix ttc au solde fournisseur
                fournisseur = Fournisseur.objects.get(id=facture.Fournisseurs.id)
                fournisseur.Solde_Fournisseur += prix_ttc
                fournisseur.save()
            instance.Factures = facture                                 #ajout de la facture
            form_facture.save()                                         #sauvegarder dans la bdd
            form_facture.save_m2m()                                     
            form_facture = EtablireFactureForm()
            msg = "Ajouté avec sucèss! Ajoutez un autre produit! "                                                       
            return render(request,"EtablireFacture.html",{"formFacture":form_facture , "msg":msg})        
    else:
        form_facture = EtablireFactureForm()   
        pk = request.session.get('facture_id')
        msg = "Veuillez remplir tous les champs!"        
        return render(request,"EtablireFacture.html",{"formFacture":form_facture , "msg":msg})

def ajout_commande(request):
    if request.method == 'POST':
        form_commande = CommandeForm(request.POST)
        if form_commande.is_valid():
            form_commande.save()
            form_commande = CommandeForm()           
            commandes = Commande.objects.latest('id')                     #Le dernier objet crée => l'objet crée dans le form      
            request.session['commande_id']= commandes.id                  #Sauvegarder la clé de Commande dans une session pour pouvoir l'utiliser après              
            return redirect("Etablire_Commande")                          #Vers l'insertions des produits
    else:
        form_commande = CommandeForm()                        
        return render(request,"AjouterCommande.html",{"formCommande":form_commande})

def etablire_commande(request):
    if request.method == 'POST':
        pk = request.session.get('commande_id')                          #récupérer la clé de commande concerné 
        form_commande = EtablireCommandeForm(request.POST)
        if form_commande.is_valid():
            instance = form_commande.save(commit=False)                  #créer une instance sans l'ajouter dans la bdd (pour ajouter la commande)
            commande = Commande.objects.get(id = pk)  
            instance.commandes = commande                                #ajout de la commande
            form_commande.save()                                         #sauvegarder dans la bdd
            form_commande.save_m2m()
            form_commande = EtablireCommandeForm()
            msg = "Ajouté avec sucèss! Ajoutez un autre produit! "                                                       
            return render(request,"EtablireCommande.html",{"formCommande":form_commande , "msg":msg})        
    else:
        form_commande = EtablireCommandeForm()   
        pk = request.session.get('commande_id')
        msg = "Veuillez remplir tous les champs!"                     
        return render(request,"EtablireCommande.html",{"formCommande":form_commande , "msg":msg})

def ajout_BL(request):
    if request.method == 'POST':
        form_BL = BLForm(request.POST)
        if form_BL.is_valid():
            form_BL.save()
            form_BL = BLForm()           
            BLs = Bon_Livraison.objects.latest('id')                       #Le dernier objet crée => l'objet crée dans le form      
            request.session['BL_id']= BLs.id                               #Sauvegarder la clé de BL dans une session pour pouvoir l'utiliser après              
            return redirect("Etablire_BL")                                 #Vers l'insertions des produits
    else:
        form_BL = BLForm()                        
        return render(request,"AjouterBL.html",{"formBL":form_BL})

def etablire_BL(request):
    if request.method == 'POST':
        pk = request.session.get('BL_id')                                  #récupérer la clé de BL concerné 
        form_BL = EtablireBLForm(request.POST)
        if form_BL.is_valid():
            instance = form_BL.save(commit=False)                          #créer une instance sans l'ajouter dans la bdd (pour ajouter la facture)
            bl = Bon_Livraison.objects.get(id = pk)
            total_achat = instance.Prix_HT_BL * instance.Qte_BL
            prix_ttc = total_achat - total_achat * bl.Remise_BL/100  
            if bl.BL_payé == False :                                       #si le bon est non payée on ajoute le prix ttc au solde fournisseur
                fournisseur = Fournisseur.objects.get(id=bl.Fournisseurs.id)
                fournisseur.Solde_Fournisseur += prix_ttc
                fournisseur.save()  
            instance.BLs = bl                                              #ajout de la BL
            form_BL.save()                                                 #sauvegarder dans la bdd
            form_BL.save_m2m()
            form_BL = EtablireBLForm()
            msg = "Ajouté avec sucèss! Ajoutez un autre produit! "                                                       
            return render(request,"EtablireBL.html",{"formBL":form_BL , "msg":msg})        
    else:
        form_BL = EtablireBLForm()   
        msg = "Veuillez remplir tous les champs!"                     
        return render(request,"EtablireBL.html",{"formBL":form_BL , "msg":msg})

def ajout_vente(request):
    if request.method == 'POST':
        form_vente = VenteForm(request.POST)
        if form_vente.is_valid():
            form_vente.save()
            form_vente = VenteForm()           
            ventes = Vente.objects.latest('id')                     #Le dernier objet crée => l'objet crée dans le form      
            request.session['vente_id']= ventes.id                  #Sauvegarder la clé de vente dans une session pour pouvoir l'utiliser après              
            return redirect("Chercher_vente")                      #Vers l'insertions des produits
    else:
        form_vente = VenteForm()                        
        return render(request,"AjouterVente.html",{"formvente":form_vente})

def chercher_produit_vente(request):
    if request.method == 'POST':
        produit_chercher = request.POST["produit_chercher"]
        qte = request.POST.get("quantite")
        request.session['qte']= qte
        produits = Product.objects.filter(Nom_produit__contains = produit_chercher )
        return render(request , "RechercheVente.html" , {"produits":produits})
    return render(request , "RechercheVente.html")

def ajouter_produit_vente(request , pk):                                #Ajouter un produits à la liste des produits à acheter
    if request.method == 'GET':
        qte = request.session.get('qte')                                  
        vente_id = request.session.get('vente_id')
        vente = Vente.objects.get(id = vente_id) 
        produit = Product.objects.get(id=pk)
        if produit.Qte_stocker >= int(qte):
            vente_effectué = Effectuer_vente()
            vente_effectué.Produits_vente = produit
            vente_effectué.Ventes = vente
            vente_effectué.Qte_vente = qte
            vente_effectué.save()
            total = 0
            produits = Effectuer_vente.objects.all().filter(Ventes = vente)
            for p in produits :
                total = p.Produits_vente.Prix_Vente_Produit * int(qte)
            msg ="Produit "+produit.Nom_produit+" ajouté avec sucèss! Prix: "+ str(produit.Prix_Vente_Produit * int(qte))+"DA || Total :"+str(total)+"DA"
            messages.success(request , msg)
            messages.add_message(request , 20 , 'Payer')
            return render(request ,'RechercheVente2.html' , {'pk':vente.id})   
        else:
            msg = "Quantité insuffisante!!"
            messages.error(request , msg)
        print(msg)                                                
        return render(request ,'RechercheVente2.html' , {'pk':vente.id}) 
    else :
        return chercher_produit_vente(request)  


def stocker(request , pk):
    if request.method == 'GET':                                                     #Stocker un produit -> Ajouter le prix et la Qte 
        produit = Product.objects.get(id = pk)
        request.session['produit_id']= produit.id
        factures = Etablire_facture.objects.all().filter(Produits = produit)        #Récupérer le prix d'après les factures
        produit.Prix_HT_Produit = factures.first().Prix_HT_Facture
        produit.Prix_Vente_Produit = factures.first().Prix_Vente_Facture
        if factures.__len__() >= 1 :                                                #Si plusieurs prix on fait plusieurs inserstions
            list = []
            for facture in factures :
                if facture.Prix_HT_Facture != produit.Prix_HT_Produit & facture.Prix_Vente_Facture != produit.Prix_Vente_Produit:
                    list.append(facture)
            return render(request ,"Stocker.html" , {"list":list})

def stocker_qte(request , pk):
    facture = Etablire_facture.objects.get(id=pk)
    if request.method == 'POST':
        id_p = request.session.get('produit_id')
        id_s = request.session.get('stock_id')
        produit = Product.objects.get(id = id_p)
        qte = int(request.POST["qte"])
        prix_ht = facture.Prix_HT_Facture
        prix_vente = facture.Prix_Vente_Facture
        stock_p = Stock.objects.get(id = id_s)
        try:
            produit_stocker = Product.objects.get(Nom_produit=produit.Nom_produit ,Prix_HT_Produit=prix_ht,Prix_Vente_Produit=prix_vente)
        except Product.DoesNotExist:
            produit_stocker = None
        if produit_stocker:         #Produit éxistant avec les memes propriétés
            temp = produit_stocker
            temp.Qte_stocker += qte
            temp.stock = stock_p
            temp.save()
        else:
            produit_stocker = Product(Nom_produit=produit.Nom_produit,Type_produit = produit.Type_produit ,Prix_HT_Produit=prix_ht,Prix_Vente_Produit=prix_vente)
            produit_stocker.Qte_stocker += qte
            produit_stocker.stock = stock_p
            produit_stocker.save()
        request.session.clear()
        return redirect("Stock")
    else:
        return render(request , "StockerQte.html")    

#-----------------------------------------------------Edit--------------------------------------------------------------

def edit_produit(request , pk):
    produit = True
    prod = Product.objects.get(id=pk)                                   #récupérer l'instance de produit
    if request.method=='POST':
        form =ProductForm(request.POST, instance = prod)
        if form.is_valid():
            form.save()
        return redirect("ProdList")                                     #rediriger vers l’url: prodList.
    else:
        form=ProductForm(instance=prod)                                 #fournir une instance pré-remplie de formulaire
        return render(request,'Edit.html',{"form":form , "produit":produit})

def edit_produit_stock(request , pk):
    produit = Product.objects.get(id=pk)
    if request.method=='POST':
        form =ProductStockForm(request.POST, instance = produit)
        if form.is_valid():
            form.save()
        return redirect("Stock")                                  
    else:
        form=ProductStockForm(instance=produit)                        
        return render(request,'Edit.html',{"form":form})


def edit_fournisseur(request , pk):
    fr = True
    fournisseur = Fournisseur.objects.get(id=pk)                          
    if request.method=='POST':
        form = FournisseurForm(request.POST, instance = fournisseur)
        if form.is_valid():
            form.save()
        return redirect("FournisseursList")                            
    else:
        form= FournisseurForm(instance = fournisseur)                    
        return render(request,'Edit.html',{"form":form , "fournisseur":fr})

def edit_client(request , pk):
    cl = True
    client = Client.objects.get(id=pk)                          
    if request.method=='POST':
        form = ClientForm(request.POST, instance = client)
        if form.is_valid():
            form.save()
        return redirect("ClientList")                            
    else:
        form= ClientForm(instance = client)                    
        return render(request,'Edit.html',{"form":form , "client":cl})

def edit_type(request , pk):
    ty = True
    type = Product_type.objects.get(id=pk)                          
    if request.method=='POST':
        form = TypeForm(request.POST, instance = type)
        if form.is_valid():
            form.save()
        return redirect("TypeList")                            
    else:
        form= TypeForm(instance = type)                    
        return render(request,'Edit.html',{"form":form , "type":ty})

def edit_stock(request , pk):
    stk = True
    stock = Stock.objects.get(id=pk)                          
    if request.method=='POST':
        form = StockeForm(request.POST, instance = stock)
        if form.is_valid():
            form.save()
        return redirect("Stock")                            
    else:
        form= StockeForm(instance = stock)                    
        return render(request,'Edit.html',{"form":form , "stock":stk})

def edit_facture(request , pk):
    facture = Facture.objects.get(id=pk)                          
    if request.method=='POST':
        form = FactureForm(request.POST, instance = facture)
        if form.is_valid():
            form.save()
        return redirect("Facture")                            
    else:
        form= FactureForm(instance = facture)                    
        return render(request,'Edit.html',{"form":form})

def edit_commande(request , pk):
    commande = Commande.objects.get(id=pk)                          
    if request.method=='POST':
        form = CommandeForm(request.POST, instance = commande)
        if form.is_valid():
            form.save()
        return redirect("Bon_commande")                            
    else:
        form= CommandeForm(instance = commande)                    
        return render(request,'Edit.html',{"form":form})

def edit_BL(request , pk):
    bon_livraison = Bon_Livraison.objects.get(id=pk)                          
    if request.method=='POST':
        form = BLForm(request.POST, instance = bon_livraison)
        if form.is_valid():
            form.save()
        return redirect("Bon_livraison")                            
    else:
        form= BLForm(instance = bon_livraison)                    
        return render(request,'Edit.html',{"form":form})

#-----------------------------------------------------Suppression----------------------------------------------------------

def supp_produit(request , pk):
    produitBool = True
    produit = Product.objects.get(id=pk)                              #récupérer l'instance de produit concerné
    if request.method=='POST':
        produit.delete()                                              #Si l'utilisateur clique sur le bouton on supprime le produit
        return redirect("ProdList")                                #Retour vers la liste des produits
    else:                  
        return render(request,'Supprimer.html',{"produit":produitBool})

def supp_fournisseur(request , pk):
    fournisseurBool = True
    fournisseur = Fournisseur.objects.get(id=pk)                   
    if request.method=='POST':
        fournisseur.delete()
        return redirect("FournisseursList")
    else:                  
        return render(request,'Supprimer.html', {"fournisseur":fournisseurBool})

def supp_stock(request , pk):
    stockBool= True
    stock = Stock.objects.get(id=pk)                   
    if request.method=='POST':
        stock.delete()
        return redirect("Stock")
    else:                  
        return render(request,'Supprimer.html',{"stock":stockBool})

def supp_type(request , pk):
    typeBool = True
    type = Product_type.objects.get(id=pk)                         
    if request.method=='POST':  
        type.delete()
        return redirect("TypeList")
    else:                  
        return render(request,'Supprimer.html',{"type":typeBool})

def supp_client(request , pk):
    clientBool= True
    client = Client.objects.get(id=pk)                         
    if request.method=='POST':
        client.delete()
        return redirect("ClientList")
    else:                  
        return render(request,'Supprimer.html',{"client":clientBool})

def supp_facture(request , pk):
    factureBool = True
    facture = Facture.objects.get(id=pk)                         
    if request.method=='POST':
        facture.delete()
        return redirect("Facture")
    else:                  
        return render(request,'Supprimer.html',{"facture": factureBool})

def supp_BL(request , pk):
    blBool = True
    BL = Bon_Livraison.objects.get(id=pk)                         
    if request.method=='POST':
        BL.delete()
        return redirect("Bon_livraison")
    else:                  
        return render(request,'Supprimer.html',{"BL":blBool})

def supp_commande(request , pk):
    commandeBool = True
    commande = Commande.objects.get(id=pk)                         
    if request.method=='POST':
        commande.delete()
        return redirect("Bon_commande")
    else:                  
        return render(request,'Supprimer.html',{"commande":commandeBool})

def destocker(request , pk):
    produit = Product.objects.get(id=pk)                            #Récupérer la Qte à déstocker et la motif et modifier le produit
    if request.method == 'POST':
        qte = int(request.POST["qte"])
        motif = request.POST["motif"]
        produit.Qte_destocker = qte
        produit.Qte_stocker -= qte
        produit.Motif = motif
        if produit.Qte_stocker <= 0:
            produit.delete()
        else:
            produit.save()
        return redirect("Stock")
    else:
        return render(request , 'Destocker.html')

def destocker(request , pk):
    produit = Product.objects.get(id=pk)                            #Récupérer la Qte à déstocker et la motif et modifier le produit
    if request.method == 'POST':
        qte = int(request.POST["qte"])
        motif = request.POST["motif"]
        produit.Qte_destocker = qte
        produit.Qte_stocker -= qte
        produit.Motif = motif
        if produit.Qte_stocker <= 0:
            produit.delete()
        else:
            produit.save()
        return redirect("Stock")
    else:
        return render(request , 'Destocker.html')

#-----------------------------------------------------Réglements-----------------------------------------------------------

def réglements_achat(request):          #Pour afficher les fournisseurs qui ont des soldes
    fournisseurs = Fournisseur.objects.all().filter(Solde_Fournisseur__gt = 0)
    filter = FournisseurFilter(request.GET , queryset = fournisseurs)
    return render(request, 'Réglements.html' , {"fournisseurs":filter})

def réglements_vente(request):          #Pour afficher les clients qui ont des crédits
    clients = Client.objects.all().filter(Credit__gt = 0)
    filter = ClientFilter(request.GET , queryset = clients)
    return render(request, 'RéglementsVente.html' , {"clients":filter})

def régler_achat(request , pk):         #Pour afficher les factures et BLs non payées d'un fournisseur
    fournisseur = Fournisseur.objects.get(id=pk)
    factures = Facture.objects.all().filter(Fournisseurs = fournisseur)
    factures.filter(facture_payé=False)
    print(factures.all)
    bls = Bon_Livraison.objects.all().filter(Fournisseurs = fournisseur)
    bls.filter(BL_payé=False)
    print(bls.all)
    return render(request, 'Régler.html' , {"factures":factures ,"bls":bls})

def régler_vente(request , pk):         #Pour afficher les factures et BLs non payées d'un fournisseur
    client = Client.objects.get(id=pk)
    ventes = Vente.objects.all().filter(Client = client)
    list = []
    for vente in ventes:
        vente_effectué = Effectuer_vente.objects.all().filter(Ventes = vente)
        total=0
        for p in vente_effectué :
            total += p.Produits_vente.Prix_Vente_Produit * p.Qte_vente  
        if total > vente.Montant : 
            list.append(vente)
    return render(request, 'RéglerVente.html' , {"ventes":list})

def payer_credit(request , pk):
    vente = Vente.objects.get(id=pk)
    vente_effectué = Effectuer_vente.objects.all().filter(Ventes = vente)
    total=0
    for p in vente_effectué :
        total += p.Produits_vente.Prix_Vente_Produit * p.Qte_vente
    credit = total - vente.Montant
    if request.method == 'POST':
        payement = int(request.POST["payement"])
        vente.Montant += payement
        vente.Client.Credit -= payement
        vente.save()
        vente.Client.save()
        return redirect('Vente')
    else:   
        return render(request , "PayerCredit.html" , {"credit":credit}) 

def régler_facture(request , pk):
    facture = Facture.objects.get(id=pk)
    etabli = Etablire_facture.objects.all().filter(Factures = facture)
    fournisseur = facture.Fournisseurs
    total = 0
    for item in etabli : total += item.Prix_HT_Facture * item.Qte_Facture
    total = total + total * facture.TVA/100 - total * facture.Remise_Facture/100
    fournisseur.Solde_Fournisseur -= total
    facture.facture_payé = True
    facture.save()
    fournisseur.save()
    return redirect("Réglements_achat")

def régler_BL(request , pk):
    bl = Bon_Livraison.objects.get(id=pk)
    etabli = Etablire_BL.objects.all().filter(BLs = bl)
    fournisseur = bl.Fournisseurs
    total = 0
    for item in etabli : total += item.Prix_HT_BL * item.Qte_BL
    total = total - total * bl.Remise_BL/100
    fournisseur.Solde_Fournisseur -= total
    bl.BL_payé = True
    bl.save()
    fournisseur.save()
    return redirect("Réglements_achat")

#-----------------------------------------------------Recherche------------------------------------------------------------

def chercher_produit(request):
    if request.method == 'POST':
        produit_chercher = request.POST["produit_chercher"]
        produits = Product.objects.filter(Nom_produit__contains = produit_chercher )
        
        return render(request , "RechercherProduit.html" , {"produit_chercher":produit_chercher , "produits":produits})
    return render(request , "RechercherProduit.html")

def chercher_produit_stocker(request , pk):
    if request.method == 'POST':
        produit_chercher = request.POST["produit_chercher"]
        produits = Product.objects.filter(Nom_produit__contains = produit_chercher )
        request.session['stock_id']= pk 
        list = []
        for produit in produits:
           if Etablire_facture.objects.all().filter(Produits = produit) :
                list.append(produit)
                return render(request , "RechercheStocker.html" , {"produit_chercher":produit_chercher , "produits":list})
    return render(request , "RechercheStocker.html")

def chercher_fournisseur(request):
    if request.method == 'POST':
        fournisseur_chercher = request.POST["fournisseur_chercher"]
        fournisseurs = Fournisseur.objects.filter(Nom_Fournisseur__contains = fournisseur_chercher )
        
        return render(request , "RechercherFournisseur.html" , {"fournisseur_chercher":fournisseur_chercher , "fournisseurs":fournisseurs})
    return render(request , "RechercherFournisseur.html")

def chercher_client(request):
    if request.method == 'POST':
        client_chercher = request.POST["client_chercher"]
        clients = Client.objects.filter(Nom_client__contains = client_chercher )
        
        return render(request , "Rechercherclient.html" , {"client_chercher":client_chercher , "clients":clients})
    return render(request , "Rechercherclient.html")

def chercher_facture(request):
    if request.method == 'POST':
        facture_chercher = request.POST["facture_chercher"]
        if Facture.objects.filter(id=facture_chercher).exists() == False:
            return render(request , "ErrorNotFound.html")
        else:
            factures = Facture.objects.get(id=facture_chercher)
            return render(request , "RechercherFacture.html" , {"facture_chercher":facture_chercher , "factures":factures})
    return render(request , "RechercherFacture.html")

def chercher_BL(request):
    if request.method == 'POST':
        BL_chercher = request.POST["BL_chercher"]
        if Bon_Livraison.objects.filter(id=BL_chercher).exists() == False:
            return render(request , "ErrorNotFound.html")
        else :
            BLs = Bon_Livraison.objects.get(id=BL_chercher)
            return render(request , "RechercherBL.html" , {"BL_chercher":BL_chercher , "BLs":BLs})
    return render(request , "RechercherBL.html")

def chercher_commande(request):
    if request.method == 'POST':
        commande_chercher = request.POST["commande_chercher"]
        if Commande.objects.filter(id=commande_chercher).exists() == False:
            return render(request , "ErrorNotFound.html")
        else:
            commandes = Commande.objects.get(id=commande_chercher)
            return render(request , "RechercherCommande.html" , {"commande_chercher":commande_chercher , "commandes":commandes})
    return render(request , "RechercherCommande.html")

#-----------------------------------------------------Export(CSV)----------------------------------------------------------

def export_produits_csv(request):
    response = HttpResponse(content_type='text/csv')                                          #créer une réponse (type fichier .csv)
    writer = csv.writer(response)
    writer.writerow(['Nom produit' , 'Type'])                                                          #La première ligne

    for produit in Product.objects.all().values_list('Nom_produit' , 'Type_produit'):                          #Ecrire tous les produits dans le fichier
        writer.writerow(produit)

    response['Content-Disposition'] = 'attachement; filename = "Liste_Produits.csv"'          #Les informations de fichier
    return response

def export_clients_csv(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Nom de client' , 'Prenom de client', 'Adresse de client' , 'Telephone de client'])

    for client in Client.objects.all().values_list('Nom_client' , 'Prenom_client' , 'Adr_client' , 'Tel_client'):
        writer.writerow(client)

    response['Content-Disposition'] = 'attachement; filename = "Liste_Clients.csv"'
    return response

def export_fournisseurs_csv(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Nom de fournisseur' , 'Prenom de fournisseur' , 'Adresse de fournisseur' , 'Telephone de fournisseur' , 'Email de fournisseur'])

    for fournisseur in Fournisseur.objects.all().values_list('Nom_Fournisseur' , 'Prenom_Fournisseur' , 'Adr_Fournisseur' , 'Tel_Fournisseur' , 'Email_Fournisseur'):
        writer.writerow(fournisseur)

    response['Content-Disposition'] = 'attachement; filename = "Liste_Fournisseurs.csv"'
    return response

def export_types_csv(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Nom de types produit'])

    for type in Product_type.objects.all().values_list('Nom_type'):
        writer.writerow(type)

    response['Content-Disposition'] = 'attachement; filename = "Liste_types.csv"'
    return response

def export_stock_csv(request , pk):
    stk = Stock.objects.get(id=pk)
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Nom produit' , 'Num stock' , 'Type' , 'QTE Stocké' , 'QTE Déstocké' , 'Prix achat' , 'Prix vente'])  
    products = Product.objects.all().filter(stock=stk)                                                  
    for produit in products.values_list('Nom_produit' , 'stock_id' , 'Type_produit' , 'Qte_stocker' , 'Qte_destocker' , 'Prix_HT_Produit' , 'Prix_Vente_Produit'):                          #Ecrire tous les produits dans le fichier
        writer.writerow(produit)

    response['Content-Disposition'] = 'attachement; filename = "Produits_Stock.csv'
    return response

#-----------------------------------------------------Export(PDF)----------------------------------------------------

def export_facture(request , pk):
    facture = Facture.objects.get(id=pk)
    etablire = Etablire_facture.objects.all().filter(Factures = facture)
    buf = io.BytesIO()
    cv = canvas.Canvas(buf , pagesize= letter , bottomup=0)
    text = cv.beginText()
    text.setTextOrigin(3.5*inch , inch)
    text.textLine("Facture N° "+str(pk))
    text.setTextOrigin(inch , 2*inch)

    lines = ["Date de la facture : "+facture.Date_Facture.__str__() , "Nom de fournisseur : "+facture.Fournisseurs.Nom_Fournisseur.capitalize()]
    for line in lines :
        text.textLine(line)
    lines.clear()
    total_vente=0 
    total_achat=0
    for produit in etablire :
        lines.append("** "+produit.Produits.Nom_produit+"      Prix vente : "+str(produit.Prix_Vente_Facture) +"DA       Prix achat :"+ str(produit.Prix_HT_Facture) +"DA        Quantité : "+str(produit.Qte_Facture)  )  
        total_vente += (produit.Prix_Vente_Facture * produit.Qte_Facture)
        total_achat += (produit.Prix_HT_Facture * produit.Qte_Facture)
    prix_ttc = total_achat + total_achat * facture.TVA/100 - total_achat * facture.Remise_Facture/100 
    lines.append("")
    lines.append("Total achat : "+str(total_achat))
    lines.append("Total vente : "+str(total_vente))
    lines.append("Remise : "+str(facture.Remise_Facture)+"%")
    lines.append("TVA : "+str(facture.TVA)+"%")
    lines.append("Total TTC : "+str(prix_ttc))
    for line in lines :
        text.textLine(line)
    cv.drawText(text)
    cv.showPage()
    cv.save()
    buf.seek(0)
    return FileResponse(buf , as_attachment=True , filename="Facture "+str(pk)+".pdf") 

def export_commande(request , pk):
    cmd = Commande.objects.get(id=pk)
    etablire = Commander.objects.all().filter(commandes =cmd)
    buf = io.BytesIO()
    cv = canvas.Canvas(buf , pagesize= letter , bottomup=0)
    text = cv.beginText()
    text.setTextOrigin(3.5*inch , inch)
    text.textLine("Commmande N° "+ str(pk))
    text.setTextOrigin(inch , 2*inch)
    lines = ["Date de la commande : "+cmd.Date_BC.__str__(), "Nom de fournisseur : "+cmd.Fournisseur.Nom_Fournisseur.capitalize()]
    for line in lines :
        text.textLine(line)
    lines.clear()
    for produit in etablire :
        lines.append("** "+produit.Produits_cmd.Nom_produit+"      Quantité : "+str(produit.Qte_cmd)  )  

    for line in lines :
        text.textLine(line)
    cv.drawText(text)
    cv.showPage()
    cv.save()
    buf.seek(0)
    return FileResponse(buf , as_attachment=True , filename="Bon commande "+str(pk)+".pdf") 

def export_bl(request , pk):
    bl = Bon_Livraison.objects.get(id=pk)
    etablire = Etablire_BL.objects.all().filter(BLs =bl)
    buf = io.BytesIO()
    cv = canvas.Canvas(buf , pagesize= letter , bottomup=0)
    text = cv.beginText()
    text.setTextOrigin(3.5*inch , inch)
    text.textLine("Bon de livraison N° "+str(pk))
    text.setTextOrigin(inch , 2*inch)
    lines = ["Date de bon : "+bl.Date_BL.__str__() , "Nom de fournisseur : "+bl.Fournisseur.Nom_Fournisseur.capitalize(), ""]
    for line in lines :
        text.textLine(line)
    lines.clear()
    total_vente=0 
    total_achat=0
    for produit in etablire :
        lines.append("** "+produit.Produits_BL.Nom_produit+"      Prix vente : "+str(produit.Prix_Vente_BL) +"DA       Prix achat :"+ str(produit.Prix_HT_BL) +"DA        Quantité : "+str(produit.Qte_BL)  )  
        total_vente += (produit.Prix_Vente_BL * produit.Qte_BL)
        total_achat += (produit.Prix_HT_BL * produit.Qte_BL)
    prix_ttc = total_achat - total_achat * bl.Remise_BL/100 
    lines.append("")
    lines.append("Total achat : "+str(total_achat))
    lines.append("Total vente : "+str(total_vente))
    lines.append("Remise : "+str(bl.Remise_BL)+"%")
    lines.append("Total TTC : "+str(prix_ttc))
    for line in lines :
        text.textLine(line)

    cv.drawText(text)
    cv.showPage()
    cv.save()
    buf.seek(0)
    return FileResponse(buf , as_attachment=True , filename="Bon livraison "+str(pk)+".pdf") 

def export_vente(request , pk):
    vente = Vente.objects.get(id=pk)
    etablire = Effectuer_vente.objects.all().filter(Ventes = vente)
    buf = io.BytesIO()
    cv = canvas.Canvas(buf , pagesize= letter , bottomup=0)
    text = cv.beginText()
    text.setTextOrigin(3.5*inch , inch)
    text.textLine("Vente N° "+str(pk))
    text.setTextOrigin(inch , 2*inch)
    lines = ["Date de vente : "+vente.Date_Vente.__str__() , "Client : "+vente.Client.Nom_client.capitalize()+" "+vente.Client.Prenom_client.capitalize(), ""]
    for line in lines :
        text.textLine(line)
    lines.clear()
    total_vente=0 
    for produit in etablire :
        lines.append("** "+produit.Produits_vente.Nom_produit+"      Prix vente : "+str(produit.Produits_vente.Prix_Vente_Produit) +"DA               Quantité : "+str(produit.Qte_vente)  )  
        total_vente += (produit.Produits_vente.Prix_Vente_Produit * produit.Qte_vente)

    lines.append("")
    lines.append("Total vente : "+str(total_vente)+"DA")
    lines.append("Montant payé : "+str(vente.Montant)+"DA")
    for line in lines :
        text.textLine(line)

    cv.drawText(text)
    cv.showPage()
    cv.save()
    buf.seek(0)
    return FileResponse(buf , as_attachment=True , filename="Vente N°"+str(pk)+".pdf") 
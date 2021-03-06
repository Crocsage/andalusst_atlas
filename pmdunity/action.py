# -*- coding: utf-8 -*-
from common import *

def ability(request, inv_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the item
    item = get_object_or_404(Inventory, pk=inv_id)
    
    # Confirm it's yours
    if (item.team.user_id != request.session.get("userID")):
        return redirect("/")
    
    # Update ability
    if request.POST.get("action") == "ability":
        pokemon_id = request.POST.get("pokemon_id")
        ability = request.POST.get("ability")
        
        # Verify you own the pokemon
        target = get_object_or_404(Pokemon, pk=pokemon_id, team__user__id=request.session.get("userID"))
        
        try:
            target.ability = ability
            target.save()
            
            # Remove the item
            item.delete()
            log(request, "[ABILITY CHANGE] " + target.name + "("+str(target.id)+") changed abilities to - " + target.ability)
            return redirect("/team/view/"+str(target.team.id))
        except:
            log(request, "[ABILITY CHANGE] FAILURE - " + target.name + "("+str(target.id)+") DID NOT change abilities to - "+ target.ability +"\n" + str(e))
            raise Http404
    
    team_id = item.team.id
    data["item"] = item
    data["pokemon"] = Pokemon.objects.filter(team_id=team_id).order_by("name")
    
    return render_to_response("action/ability.html", data, context_instance=RequestContext(request))

def equip(request, team_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    team = Team.objects.get(pk=team_id)
    if request.session.get("userID"):
        if team.user.id == request.session["userID"] or request.session["admin"]:
            data["yours"] = True
            
    if not data["yours"]:
        return redirect("/")
        
    # Get team
    data["pokemon"] = Pokemon.objects.filter(team_id=team_id)
    # Get inventory
    data["inventory"] = Inventory.objects.filter(team_id=team_id)
        
    return render_to_response("action/equip.html", data, context_instance=RequestContext(request))

def evolve(request, inv_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the item
    item = get_object_or_404(Inventory, pk=inv_id)
    
    # Confirm it's yours
    if (item.team.user_id != request.session.get("userID")):
        return redirect("/")
    
    # Check if you're evolving
    if request.POST.get("action") == "evolve":
        # Load the pokemon
        stats = request.POST.getlist("stat")
        
        target = get_object_or_404(Pokemon, pk=request.POST.get("pokemon_id"), team__user__id=request.session.get("userID"))
        target.ability              = request.POST.get("ability")
        target.species              = request.POST.get("to_species")
        target.strength             = stats[0]
        target.intelligence         = stats[2]
        target.agility              = stats[4]
        target.charisma             = stats[6]
        target.bonus_strength       = stats[1]
        target.bonus_intelligence   = stats[3]
        target.bonus_agility        = stats[5]
        target.bonus_charisma       = stats[7]
        
        target.move1          = request.POST.get("move1", "-")
        target.move2          = request.POST.get("move2", "-")
        target.move3          = request.POST.get("move3", "-")
        target.move4          = request.POST.get("move4", "-")
        
        if target.move1 == "":
            target.move1 = "-"
        if target.move2 == "":
            target.move2 = "-"
        if target.move3 == "":
            target.move3 = "-"
        if target.move4 == "":
            target.move4 = "-"
        
        # Clean up move dashes
        if target.move1 != "-" and target.move1[0] == "-":
            target.move1 = target.move1[1:]
        if target.move2 != "-" and target.move2[0] == "-":
            target.move2 = target.move2[1:]
        if target.move3 != "-" and target.move3[0] == "-":
            target.move3 = target.move3[1:]
        if target.move4 != "-" and target.move4[0] == "-":
            target.move4 = target.move4[1:]
        
        try:
            target.full_clean(exclude=["comments"])
            target.save()
            item.delete()
            log(request, "[EVOLUTION] " + target.name + "("+str(target.id)+") evolved from " + request.POST.get("from_species") + " to " + request.POST.get("to_species"))
            return redirect("/team/view/"+str(target.team.id))
        except ValidationError as e:
            log(request, "[EVOLUTION] FAILURE - " + target.name + "("+str(target.id)+") DID NOT evolve from " + request.POST.get("from_species") + " to " + request.POST.get("to_species") + "\n" + str(e))
            raise Http404
    
    team_id = item.team.id
    team_name = item.team.name
    data["item"] = item
    data["evolutions"] = {1:[2], 2:[3], 4:[5], 5:[6], 7:[8], 8:[9], 10:[11], 11:[12], 13:[14], 14:[15], 16:[17], 17:[18], 19:[20], 21:[22], 23:[24], 172:[25], 25:[26], 27:[28], 29:[30], 30:[31], 32:[33], 33:[34], 173:[35], 35:[36], 37:[38], 174:[39], 39:[40], 41:[42], 42:[169], 43:[44], 44:[45,182], 46:[47], 48:[49], 50:[51], 52:[53], 54:[55], 56:[57], 58:[59], 60:[61], 61:[62,186], 63:[64], 64:[65], 66:[67], 67:[68], 69:[70], 70:[71], 72:[73], 74:[75], 75:[76], 77:[78], 79:[80,199], 81:[82], 82:[462], 84:[85], 86:[87], 88:[89], 90:[91], 92:[93], 93:[94], 95:[208], 96:[97], 98:[99], 100:[101], 102:[103], 104:[105], 236:[106,107,237], 108:[463], 109:[110], 111:[112], 112:[464], 440:[113], 113:[242], 114:[465], 116:[117], 117:[230], 118:[119], 120:[121], 439:[122], 123:[212], 238:[124], 239:[125], 125:[466], 240:[126], 126:[467], 129:[130], 133:[134,135,136,196,197,470,471,700], 137:[233], 233:[474], 138:[139], 140:[141], 446:[143], 147:[148], 148:[149], 152:[153], 153:[154], 155:[156], 156:[157], 158:[159], 159:[160], 161:[162], 163:[164], 165:[166], 167:[168], 170:[171], 175:[176], 176:[468], 177:[178], 179:[180], 180:[181], 298:[183], 183:[184], 438:[185], 187:[188], 188:[189], 190:[424], 191:[192], 193:[469], 194:[195], 198:[430], 200:[429], 360:[202], 204:[205], 207:[472], 209:[210], 215:[461], 216:[217], 218:[219], 220:[221], 221:[473], 223:[224], 458:[226], 228:[229], 231:[232], 246:[247], 247:[248], 252:[253], 253:[254], 255:[256], 256:[257], 258:[259], 259:[260], 261:[262], 263:[264], 266:[267], 265:[266,268], 268:[269], 270:[271], 271:[272], 273:[274], 274:[275], 276:[277], 278:[279], 280:[281], 281:[282,475], 283:[284], 285:[286], 287:[288], 288:[289], 290:[291,292], 293:[294], 294:[295], 296:[297], 299:[476], 300:[301], 304:[305], 305:[306], 307:[308], 309:[310], 406:[315], 315:[407], 316:[317], 318:[319], 320:[321], 322:[323], 325:[326], 328:[329], 329:[330], 331:[332], 333:[334], 339:[340], 341:[342], 343:[344], 345:[346], 347:[348], 349:[350], 353:[354], 355:[356], 356:[477], 433:[358], 361:[362,478], 363:[364], 364:[365], 366:[367,368], 371:[372], 372:[373], 374:[375], 375:[376], 387:[388], 388:[389], 390:[391], 391:[392], 393:[394], 394:[395], 396:[397], 397:[398], 399:[400], 401:[402], 403:[404], 404:[405], 408:[409], 410:[411], 412:[413,414], 415:[416], 418:[419], 420:[421], 422:[423], 425:[426], 427:[428], 431:[432], 434:[435], 436:[437], 443:[444], 444:[445], 447:[448], 449:[450], 451:[452], 453:[454], 456:[457], 459:[460], 495:[496], 496:[497], 498:[499], 499:[500], 501:[502], 502:[503], 504:[505], 506:[507], 507:[508], 509:[510], 511:[512], 513:[514], 515:[516], 517:[518], 519:[520], 520:[521], 522:[523], 524:[525], 525:[526], 527:[528], 529:[530], 532:[533], 533:[534], 535:[536], 536:[537], 540:[541], 541:[542], 543:[544], 544:[545], 546:[547], 548:[549], 551:[552], 552:[553], 554:[555], 557:[558], 559:[560], 562:[563], 564:[565], 566:[567], 568:[569], 570:[571], 572:[573], 574:[575], 575:[576], 577:[578], 578:[579], 580:[581], 582:[583], 583:[584], 585:[586], 588:[589], 590:[591], 592:[593], 595:[596], 597:[598], 599:[600], 600:[601], 602:[603], 603:[604], 605:[606], 607:[608], 608:[609], 610:[611], 611:[612], 613:[614], 616:[617], 619:[620], 622:[623], 624:[625], 627:[628], 629:[630], 633:[634], 634:[635], 636:[637], 650:[651], 651:[652], 653:[654], 654:[655], 656:[657], 657:[658], 659:[660], 661:[662], 662:[663], 664:[665], 665:[666], 667:[668], 669:[670], 670:[671], 672:[673], 674:[675], 677:[678], 679:[680], 680:[681], 682:[683], 684:[685], 686:[687], 688:[689], 690:[691], 692:[693], 694:[695], 696:[697], 698:[699], 704:[705], 705:[706], 708:[709], 710:[711], 712:[713], 714:[715]}
    data["pokemon"] = Pokemon.objects.filter(team_id=team_id, species__in=data["evolutions"].keys()).order_by("name")
    #data["names"] = POKEMON
    return render_to_response("action/evolve.html", data, context_instance=RequestContext(request))

def open_item(request, inv_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the item
    item = get_object_or_404(Inventory, pk=inv_id)
    
    # Confirm it's yours
    if (item.team.user_id != request.session.get("userID")):
        return redirect("/")
    
    team_id = item.team.id
    team_name = item.team.name
    data["item"] = item
    
    # Determine possible rewards
    rewards = {
        37:[{"item":15, "qty":1}, {"item":11, "qty":2}, {"item":16, "qty":1}], 
        38:[{"item":35, "qty":1}, {"item":36, "qty":1}], 
        39:[{"item":17, "qty":1}, {"item":18, "qty":1}],
        40:[{"item":19, "qty":1}, {"item":20, "qty":1}], 
        41:[{"item":23, "qty":1}, {"item":24, "qty":1}], 
        42:[{"item":25, "qty":1}, {"item":26, "qty":1}], 
        43:[{"item":27, "qty":1}, {"item":28, "qty":1}], 
        44:[{"item":29, "qty":1}, {"item":30, "qty":1}], 
        45:[{"item":31, "qty":1}, {"item":32, "qty":1}],
        66:[{"item":62, "qty":1}, {"item":63, "qty":1}],
        65:[{"item":56, "qty":1}, {"item":54, "qty":3}, {"item":55, "qty":1}]
    }
    
    choices = rewards[item.item.id]
    del rewards
    
    if (request.POST.get("action") != "open"):
        # Parse possible rewards
        for choice in choices:
            if (choice != -1):
                choice["item"] = Item.objects.get(pk=choice["item"])
            else:
                # Handle starcoin reward here
                None
        data["choices"] = choices
        #print choices
        # Render
        return render_to_response("action/open.html", data, context_instance=RequestContext(request))
    else:
        try:
            choice = int(request.POST.get("choice"))
            reward = choices[choice]
            # Give the new item
            for x in xrange(0, reward["qty"]):
                inv = Inventory(team_id=team_id, item_id=reward["item"])
                # Save
                inv.save()
                
            package = Inventory.objects.get(pk=inv_id)
            
            
            # Remove the old item
            package.delete()
            
            
            log(request, "[OPEN] " + team_name + " chose reward #"+str(choice)+" from their " + package.item.name)
        except:
            return redirect("/")
        return redirect("/team/inventory/"+str(team_id)+"/")
        
def recruit_teammate(request, inv_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the item
    item = get_object_or_404(Inventory, pk=inv_id)
    
    # Confirm it's yours
    if (item.team.user_id != request.session.get("userID")):
        return redirect("/")
        
    # Confirm it's a recruitment slip
    if (item.item.id != 53):
        return redirect("/")
    
    # Confirm you have no more than 4 teammates already
    if (item.team.pkmn1_id and item.team.pkmn2_id and item.team.pkmn3_id and item.team.pkmn4_id):
        return redirect("/error/too-many-teammates")
    
    # Create a blank teammate
    team_id = item.team.id
    tomorrow = datetime.now() + timedelta(days=1)
    recruit = Pokemon(team=item.team, species=-1, lock_time=tomorrow)
    recruit.save()
    
    if not item.team.pkmn1_id:
        item.team.pkmn1 = recruit
    elif not item.team.pkmn2_id:
        item.team.pkmn2 = recruit
    elif not item.team.pkmn3_id:
        item.team.pkmn3 = recruit
    elif not item.team.pkmn4_id:
        item.team.pkmn4 = recruit
        
    # Give a voucher
    guild = item.team.guild
    if guild == "Explorers":
        item_id = 12
    elif guild == "Hunters":
        item_id = 13
    elif guild == "Researchers":
        item_id = 14
    
    voucher = Inventory(team_id=item.team_id, item_id=item_id)
    voucher.save()
        
    # Remove the item
    try:
        item.team.save()
        item.delete()
        log(request, "[NEW RECRUIT] PKMN ID: " + str(recruit.id) + " ON TEAM ID: " + str(recruit.team.id))
        return redirect("/team/"+str(recruit.team.id))
    except:
        log(request, "[NEW RECRUIT] FAILURE FOR TEAM " + str(team_id))
        raise Http404

def set_stats(request, pokemon_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the pokemon
    target = get_object_or_404(Pokemon, pk=pokemon_id, team__user__id=request.session.get("userID"))
    
    # Check if you're evolving
    if request.POST.get("action") == "set_stats":
        # Set the pokemon info
        stats = request.POST.getlist("stat")
        
        target.strength             = stats[0]
        target.intelligence         = stats[2]
        target.agility              = stats[4]
        target.charisma             = stats[6]
        target.bonus_strength       = stats[1]
        target.bonus_intelligence   = stats[3]
        target.bonus_agility        = stats[5]
        target.bonus_charisma       = stats[7]
        
        try:
            target.full_clean(exclude=["comments", "lock_time"])
            target.save()
            log(request, "[SET_STATS] " + target.name + "("+str(target.id)+") has set their stats.")
            return redirect("/team/view/"+str(target.team.id))
        except ValidationError as e:
            print e
            log(request, "[SET_STATS] FAILURE - " + target.name + "("+str(target.id)+") DID NOT properly set their stats.\n" + str(e))
            raise Http404
    
    data["pokemon"] = target
    #data["names"] = POKEMON
    return render_to_response("action/set_stats.html", data, context_instance=RequestContext(request))
    
def tm(request):
    return HttpResponse("TM")
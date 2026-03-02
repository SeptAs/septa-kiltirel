import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "kle_sekre_channmas"

# 1. Lis Kesyon yo (18 kesyon total)
kesyon_yo = [
    {"id": 1, "tèks": "Ki vil yo rele Vil tonton nòl la?", "opsyon": ["Pòtoprens", "Okap", "Jakmèl", "Gonayiv"], "repons": "Okap"},
    {"id": 2, "tèks": "Nan ki ane batay Vètyè te fèt?", "opsyon": ["1801", "1802", "1803", "1804"], "repons": "1803"},
    {"id": 3, "tèks": "Ki non mòn ki pi wo nan peyi a?", "opsyon": ["Mòn Kabrit", "Pik Lasèl", "Pik Makaya", "Mòn Boutilye"], "repons": "Pik Lasèl"},
    {"id": 4, "tèks": "Ki enstriman ki pi enpòtan nan Rara?", "opsyon": ["Gita", "Vaksin", "Pyano", "Tanbou"], "repons": "Vaksin"},
    {"id": 5, "tèks": "Ki wa ki te konstwi Sitadèl Laferyè a?", "opsyon" : ["Jean-Jacques Dessalines","Henry Christophe", "Alexandre Pétion", "Toussaint Louverture"], "repons": "Henry Christophe"},
    {"id": 6, "tèks": "Nan ki depatman n ap jwenn 'Basen Ble'?", "opsyon": ["Nò", "Lwès", "Sidès", "Latibonit"], "repons": "Sidès"},
    {"id": 7, "tèks": "Ki non dans tradisyonèl ki fèt pandan fèt Gede?", "opsyon": ["Yanvalou", "Djouba", "Bèlè", "Gede"], "repons": "Gede"},
    {"id": 8, "tèks": "Ki non festival mizik ki fèt chak ane nan Pòtoprens?", "opsyon": ["Festival Mizik Pòtoprens", "Festival Jazz Pòtoprens", "Festival Rara Pòtoprens", "Festival Kiltirèl Pòtoprens"], "repons": "Festival Mizik Pòtoprens"},
    {"id": 9, "tèks": "Ki zwazo ki senbòl nasyonal peyi a?", "opsyon": ["Kolibri", "Jako", "Kalson wouj Pilawo", "Papayè"], "repons": "Kalson wouj Pilawo"},
    {"id": 10, "tèks": "Ki gwo fò nan nò a?", "opsyon": ["Fò Jak", "Sitadèl Laferyè", "Fò Alix", "Fò Pikole"], "repons": "Sitadèl Laferyè"},
    {"id": 11, "tèks": "Ki kote seremoni Bwa Kayiman te fèt?", "opsyon": ["Bwa Kayiman", "Nan Lakou", "Plenn di Nò", "Mòn Kabrit"], "repons": "Bwa Kayiman"},
    {"id": 12, "tèks": "Nan ki depatman vil Jakmèl ye?", "opsyon": ["Lwès", "Sidès", "Nòp", "Grandans"], "repons": "Sidès"},
    {"id": 13, "tèks": "Kilès ki te di 'Boulèt se pousyè'?", "opsyon": ["Capois-La-Mort", "Boukman", "Peralte", "Makandal"], "repons": "Capois-La-Mort"},
    {"id": 14, "tèks": "Ki non lajan peyi Ayiti?", "opsyon": ["Dola", "Goud", "Peso", "Euro"], "repons": "Goud"},
    {"id": 15, "tèks": "Ki flè nasyonal peyi a?", "opsyon": ["Woz", "Bwa Kayiman", "Ibis (Choublack)", "Flanbwayan"], "repons": "Ibis (Choublack)"},
    {"id": 16, "tèks": "Ki vil yo rele 'Vil nan Syèl la'?", "opsyon": ["Kenscoff", "Ferye", "Pion", "Kenskòf"], "repons": "Kenskòf"},
    {"id": 17, "tèks": "Kilès ki te ekri 'La Dessalinienne'?", "opsyon": ["Justin Lhérisson", "Nicolas Geffrard", "Oswald Durand", "Massillon Coicou"], "repons": "Justin Lhérisson"},
    {"id": 18, "tèks": "Ki kote Pik Makaya ye?", "opsyon": ["Sid", "Nò", "Sidès", "Nip"], "repons": "Sid"}
]

LIMIT_KESYON = 10 

# 2. Paj Akeyi
@app.route('/')
def home():
    session['pwen'] = 0
    session['kontè'] = 0
    # Chwazi 10 id o aza pou jwèt la
    tout_id = [q['id'] for q in kesyon_yo]
    random.shuffle(tout_id)
    session['lis_id'] = tout_id[:LIMIT_KESYON]
    return render_template('index.html')

# 3. Paj kote jwèt la ap woule
@app.route('/jwe')
def jwe():
    kontè = session.get('kontè', 0)
    
    # Si nou rive nan limit la, ale nan game_over
    if kontè >= LIMIT_KESYON:
        return redirect(url_for('game_over'))
    
    # Jwenn kesyon an nan lis nou te prepare a
    id_aktyèl = session['lis_id'][kontè]
    k = next(q for q in kesyon_yo if q['id'] == id_aktyèl)
    
    return render_template('jwèt.html', 
                           k=k, 
                           pwen=session.get('pwen', 0), 
                           kote_nou_ye=kontè + 1)

# 4. Verifikasyon
@app.route('/tcheke', methods=['POST'])
def tcheke():
    id_k = request.form.get('id_kesyon')
    repons_moun = request.form.get('repons_itilizatè') 
    
    if not id_k:
        return redirect(url_for('jwe'))

    kesyon_aktyèl = next(q for q in kesyon_yo if q['id'] == int(id_k))
    
    bon_repons = False
    if repons_moun and repons_moun == kesyon_aktyèl['repons']:
        session['pwen'] = session.get('pwen', 0) + 10
        bon_repons = True
    
    # Nou ogmante kontè a ISIT LA
    session['kontè'] = session.get('kontè', 0) + 1
    
    # Tcheke si jwèt la fini pou nou di HTML la
    fini = session['kontè'] >= LIMIT_KESYON
    
    return render_template('rezilta.html', 
                           bon=bon_repons, 
                           repons=kesyon_aktyèl['repons'], 
                           pwen=session['pwen'],
                           tan_fini=(not repons_moun),
                           jwèt_fini=fini) # Sa ap anpeche erè a

# 5. Paj Finisman
@app.route('/game_over')
def game_over():
    pwen = session.get('pwen', 0)
    # Tit yo dapre nivo a
    if pwen <= 30: tit = "Ti Ayisyen 👶"
    elif pwen <= 70: tit = "Sitwayen Angaje 🇭🇹"
    else: tit = "Anperè Kiltirèl 👑"
        
    return render_template('game_over.html', pwen=pwen, tit=tit)

if __name__ == '__main__':
    app.run(debug=True)
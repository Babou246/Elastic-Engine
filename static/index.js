const p = require('puppeteer')
const csv = require("csv-writer")


// IMPORTER UN FICHIER CSV
function getCSV(data){
    let readerCSV = csv.createObjectCsvWriter
    let csvWriter = readerCSV({
        path:"data_alibaba.csv",
        header : [
            {id:'image',Titre:'image'},
            {id:'description',Titre:'description'},
            {id:'final',Titre:'final'}
        ]
    })
    csvWriter.writeRecords(data)
    .then( () => console.log('crée'))
}

const getData = async ()=>{
    const browser = await p.launch({headless:false})
    const page = await browser.newPage()

    // Naviguer jusqu'a l'URL cible
    n = 2
    await page.goto('https://french.alibaba.com/premium/babies_diapers.html?src=sem_ggl&from=sem_ggl&cmpgn=10367696577&adgrp=102914223293&fditm=&tgt=kwd-921825581461&locintrst=9067846&locphyscl=9067846&mtchtyp=p&ntwrk=g&device=c&dvcmdl=&creative=444062284719&plcmnt=&plcmntcat=&p1=&p2=&aceid=&position=&localKeyword=couches%20pour%20b%C3%A9b%C3%A9s&gclid=EAIaIQobChMIzryPzYKl-AIVRvhRCh2C-wf1EAAYASAAEgLITvD_BwE'+'2')
    
    await page.setViewport({ width: 1500, height: 1500 })
    let products = await page.evaluate(function(){
        let data = new Array()
        const div = document.querySelector('.app-ppc-list')
        const Items = div.querySelectorAll('.organic-offer-wrapper.organic-gallery-offer-inner.m-gallery-product-item-v2.img-switcher-parent')
        console.log(Items)
        Items.forEach(item => {
            d = {}
            image_produits = item.querySelector('a>div>div.seb-img-switcher__imgs >img.J-img-switcher-item')
            title_produits = item.querySelector('.elements-title-normal__content.medium').innerText
            prix_produits = item.querySelector('.elements-offer-price-normal.medium').innerText
            image = item.querySelector('div.seb-img-switcher.J-img-switcher > div.seb-img-switcher__imgs > img').getAttribute('src')
            console.log(image)

            prix = prix_produits.split('/')[0]
            // Sépartion de l'intervalle des prix
            // 1 er prix
            first_price  = prix.split('-')[0]
            firt = first_price.split('$US')[0]
            prix_debut = parseFloat(firt)*616,75000

            // 2eme Prix
            second_price = prix.split('-')[1]
            undefined != second_price ? final_price = second_price.replace('$US','CFA') : console.log('erreur')
            console.log('=============================')
            str = final_price.replace('CFA','').replace(/\s/g,'').replace(/,/g,'')
            console.log(final_price)
            prix_final = parseFloat(str)*616,75000
            d = {

                'image':image,
                'description':title_produits,
                'final':prix_final
            }
            data.push(d)
            console.log(data)

            
            
        })
        return data


    })
    

    console.log(products)
    
    
    browser.close()
    getCSV(products)

}
// getData()

const getProducts = async function () {
    try {
      let response = await fetch('http://127.0.0.1:5000/api/jumia')
      if (response.ok) {
        let data = await response.json()
        console.log(data)
      } else {
        console.error('Retour du serveur : ', response.status)
      }
    } catch (e) {
      console.log(e)
    }
}
getProducts()
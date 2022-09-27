import scrapy
import pandas as pd
#TO DO
# verificar exceções de evolucvao, como a eve #133

class PokemonScrapper(scrapy.Spider):
  name = 'pokemon_scrapper'
  #domain = 'https://bulbapedia.bulbagarden.net'
  domain = 'https://www.serebii.net'
  #para pegar os tipos do pokemon: pegar a href, fazendo um regex
  start_urls = ['https://www.serebii.net/pokedex/001.shtml']
  
  def get_atribbute_from_link(self, link):
    comeco = link.rfind("/") +1
    fim = link.rfind(".")
    return link[comeco:fim]
  
  def parse(self, response):
    count = 0

    response.follow(self.start_urls[0],self.pokemon_parse)

    count += 1
    #150
    while count <= 5:  
      count += 1
      yield response.follow(self.domain +"/pokedex/"+ f"{count:03}" + ".shtml" , self.pokemon_parse)

  def pokemon_parse(self,response):
    id =  (response.css("td.fooinfo::text").getall()[3]).replace("#", '')
    tipos = response.css("td.footype").xpath(".//a/@href").getall()
    dano = response.css("td.footype::text").getall()[-15:]
    tipos_pokemon = response.css("td.cen").xpath(".//a/@href").getall()
    id_evolucao = ''

    for index, value in enumerate(dano):
      dano[index] = float(value.replace("*",""))

    for i in range(len(tipos_pokemon)):
      link = tipos_pokemon[i]
      tipos_pokemon[i] = self.get_atribbute_from_link(link)

    tipagem = []
    for i in range(len(tipos)):
      link = tipos[i]
      tipagem.append(self.get_atribbute_from_link(link)) 

    dano_recebido = {}
    for i in range(len(tipos)):
      dano_recebido[tipagem[i]] = dano[i]

    if id == '133':
      evolucoes = response.xpath("*//td[@class='pkmn']/a/@href").getall()[-3:] 
      for i in range(len(evolucoes)):
        link = evolucoes[i]
        id_evolucao += self.get_atribbute_from_link(link)+' '

    elif id in ['134','135','136']:
      id_evolucao = ''
    else:
      evolucoes = response.css("table.evochain").xpath(".//a/@href").getall()  
      for i in range(len(evolucoes)):
        link = evolucoes[i]
        evolucoes[i] = self.get_atribbute_from_link(link)
      valor = evolucoes.index(id)
      try:
        prox = evolucoes[valor+1]
        id_evolucao = prox
      except:
        pass

      self.nexturl = response.xpath("//td[@align='center']/a/@href").getall()[-1]
      funnypoke = {"id":id, "nome": response.css("td.fooinfo::text").getall()[2],"altura" :       (response.css("td.fooinfo::text").getall()[6]).strip(),"peso" : (response.css("td.fooinfo::text").getall()[8]).strip(),"tipos": tipos_pokemon,"dano_recebido":dano_recebido,"id_evolucao":id_evolucao}
      df = pd.DataFrame.from_dict(funnypoke, orient="index")
      df.to_csv("poke_file.csv")
      print(df)
      yield funnypoke
      #yield  self.nexturl
      


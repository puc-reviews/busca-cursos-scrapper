import requests
import lxml.html as lh
import json

SCHOOL_IDS_PATH = 'schools.json' # Utiliza este json para establecer nombres y buscar por escuela

def obtener_porcentaje(dividendo,total):
  return int((dividendo/total)*100)
def get_school_courses(name, id, year, semester):

  URL = 'http://buscacursos.uc.cl/?cxml_semestre={}-{}&cxml_sigla=&cxml_nrc=&cxml_nombre=&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus=TODOS&cxml_unidad_academica={}&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS#resultados'.format(year, semester, id)
  page = requests.get(URL)
  doc = lh.fromstring(page.content)
  tr_elements = doc.xpath('//tr')


  ramos = []
  for row in tr_elements:
    if len(row) ==18:
      ramo= {
        'Sigla': row[1].text_content(),
        'Nombre': row[9].text_content(),
        'Prof': row[10].text_content(),
        'Campus': row[11].text_content(),
        'Creditos': row[12].text_content(),
      }
      ramos.append(ramo)
  return { name: ramos }

year = int(input('year: '))
semester = int(input('Semester: '))
count = 0

resultados = []
print("iniciando ...")
with open(SCHOOL_IDS_PATH, encoding="utf8") as data:
  schools = json.load(data)
  for school in schools:
    school_name = school['name']
    print("Obteniendo:", school_name, "-- {}%".format(obtener_porcentaje(count, len(schools))))
    school_id = school['id']
    info = get_school_courses(school_name, school_id, year, semester)
    resultados.append(info)
    count += 1

# Exporta todo los resultados a un json en formato 'AÑO_SEMESTRE.json'

with open('{}_{}.json'.format(year, semester), 'w') as json_file:
    json.dump(resultados, json_file, indent = 4)
##### Graph stuff
import os
import rdflib
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME
# Prefixes
name_space = "https://kastle-lab.org/"
pfs = {
"kl-res": Namespace(f"{name_space}lod/resource/"),
"kl-ont": Namespace(f"{name_space}lod/ontology/"),
"geo": Namespace("http://www.opengis.net/ont/geosparql#"),
"geof": Namespace("http://www.opengis.net/def/function/geosparql/"),
"sf": Namespace("http://www.opengis.net/ont/sf#"),
"wd": Namespace("http://www.wikidata.org/entity/"),
"wdt": Namespace("http://www.wikidata.org/prop/direct/"),
"dbo": Namespace("http://dbpedia.org/ontology/"),
"time": Namespace("http://www.w3.org/2006/time#"),
"ssn": Namespace("http://www.w3.org/ns/ssn/"),
"sosa": Namespace("http://www.w3.org/ns/sosa/"),
"cdt": Namespace("http://w3id.org/lindt/custom_datatypes#"),
"ex": Namespace("https://example.com/"),
"rdf": RDF,
"rdfs": RDFS,
"xsd": XSD,
"owl": OWL,
"time": TIME
}
# Initialization shortcut
def init_kg(prefixes=pfs):
    kg = Graph()
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])
    return kg
# rdf:type shortcut
a = pfs["rdf"]["type"]

# Initialize an empty graph
graph = init_kg()

# Initialize from a file
# filename = "path/to/file"
# with open(filename, "w") as f:
#     graph.parse(f)

filedir = "../data"
filename = "2024-air-kg-data.csv"

with open(os.path.join(filedir, filename), "r") as f:
    lines = [ lines for lines in f.readlines() ]

# print(lines[0:4])
header = lines[0]

authors = set()

# gets unique author names
for line in lines[1:]:
    split = line.split(",")
    name = f"{split[0].strip()} {split[1].strip()}"
    authors.add(name)
    # print(name)

author_dict = {}

author_count = 0

# uniquely add authors to kg
for author in authors:
    # minting author uri
    author_uri = pfs["ex"][f"Author{author_count}"]
    author_count += 1

    # binding author uri to kg
    graph.add( (author_uri, a, pfs["ex"]["Author"]) )
    graph.add( (author_uri, pfs["ex"]["hasName"], Literal(author, datatype=XSD.string)) )

    author_dict[author] = author_uri

publication_count = 0

# associate publications with authors
for line in lines[1:]:
    split = line.split(",")
    split_length = len(split)
    name = f"{split[0].strip()} {split[1].strip()}"
    author_uri = author_dict[name]

    title = split[2].strip()
    topics = split[3:split_length-1]
    year = split[-1].strip()

    # minting publication uri
    publication_uri = pfs["ex"][f"Publication{publication_count}"]
    publication_count += 1
    # binding publication uri to kg
    graph.add( (publication_uri, pfs["ex"]["hasTitle"], Literal(title, datatype=XSD.string)) )
    graph.add( (publication_uri, pfs["ex"]["hasYear"], Literal(year, datatype=XSD.gYear)) )
    
    # associate topics with publication
    for topic in topics:
        topic = topic.replace("\"", "")
        graph.add( (publication_uri, pfs["ex"]["hasTopic"], Literal(topic.strip(), datatype=XSD.string)) )
    
    # associate authors and publications with one another
    graph.add( (author_uri, pfs["ex"]["published"], publication_uri) )
    graph.add( (publication_uri, pfs["ex"]["publishedBy"], author_uri) )

output_file = "output.ttl"
temp = graph.serialize(format="turtle", encoding="utf-8", destination=output_file)
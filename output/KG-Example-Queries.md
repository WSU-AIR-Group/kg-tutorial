# Knowledge Graph Tutorial

### SPARQL Queries

```
PREFIX ex: <https://example.com/>

SELECT ?authorName ?title
WHERE {
  ?author a ex:Author ;
          ex:hasName ?authorName ;
          ex:published ?publication .
  ?publication ex:hasTitle ?title .
}
```

```
PREFIX ex: <https://example.com/>

SELECT ?title ?year
WHERE {
  ?author ex:hasName "Alexis Ellis" ;
          ex:published ?publication .
  ?publication ex:hasTitle ?title ;
               ex:hasYear ?year .
}
```

```
PREFIX ex: <https://example.com/>

SELECT ?authorName (COUNT(?publication) AS ?pubCount)
WHERE {
  ?author a ex:Author ;
          ex:hasName ?authorName ;
          ex:published ?publication .
}
GROUP BY ?authorName 
HAVING (COUNT(?publication) > 1)
```

settings = {
    "analysis": {
        "filter": {
            "english_stop": {
                "type": "stop",
                "stopwords": "_english_"
            },
            "russian_stop": {
                "type": "stop",
                "stopwords": "_russian_"
            },
            "english_stemmer": {
                "type": "stemmer",
                "language": "english"
            },
            "russian_stemmer": {
                "type": "stemmer",
                "language": "russian"
            }
        },
        "analyzer": {
            "multilingual_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "russian_stop",
                    "russian_stemmer"
                ]
            }
        }
    }
}

index_settings = {
    "product": {
        "settings": settings,
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "multilingual_analyzer"
                },
                "description": {
                    "type": "text",
                    "analyzer": "multilingual_analyzer"
                }
            }
        }
    }
}

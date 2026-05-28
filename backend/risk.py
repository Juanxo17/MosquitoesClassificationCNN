RISK_CONFIG = {
    'aedes': {
        'level': 'ALTO',
        'diseases': ['Dengue', 'Zika', 'Chikungunya'],
        'recommendation': 'Notificar a la autoridad sanitaria local de inmediato.'
    },
    'anopheles': {
        'level': 'ALTO',
        'diseases': ['Malaria'],
        'recommendation': 'Notificar a la autoridad sanitaria local de inmediato.'
    },
    'culex': {
        'level': 'MEDIO',
        'diseases': ['Virus del Nilo Occidental'],
        'recommendation': 'Monitorear la zona y reportar si la presencia aumenta.'
    }
}


CONFIDENCE_TRESHOLD = 0.80


def evaluate_risk(species: str, confidence: float) -> dict:
    if confidence < CONFIDENCE_TRESHOLD:
        return {
            'species': 'desconocida',
            'confidence': confidence,
            'risk_level': 'INDETERMINADO',
            'diseases': [],
            'recommendation': 'No se pudo identificar la especie con certeza. Verifique la calidad de la imagen.    '
        }
    
    config = RISK_CONFIG[species]
    return {
        'species': species,
        'confidence': confidence,
        'risk_level': config['level'],
        'diseases': config['diseases'],
        'recommendation': config['recommendation']
    }

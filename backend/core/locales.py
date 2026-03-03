LOCALES = {
    "en": {
        "summary": "Professional Summary",
        "contact": "Contact",
        "education": "Education",
        "experience": "Experience",
        "skills": "Skills",
        "certifications": "Certifications",
        "languages": "Languages",
        "software_engineer": "Software Engineer",
        "project_experience": "Project Experience",
        "references": "References"
    },
    "es": {
        "summary": "Resumen Profesional",
        "contact": "Contacto",
        "education": "Educación",
        "experience": "Experiencia",
        "skills": "Habilidades",
        "certifications": "Certificaciones",
        "languages": "Idiomas",
        "software_engineer": "Ingeniero de Software",
        "project_experience": "Experiencia en Proyectos",
        "references": "Referencias"
    }
}

def get_labels(lang: str = "en") -> dict:
    """Returns the set of labels for the given language."""
    return LOCALES.get(lang.lower()[:2], LOCALES["en"])

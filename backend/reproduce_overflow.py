import os
import sys
from core.generator import generate_pdf
import jinja2

# Mock data similar to MARTIN_SANCHEZ_URREGO
data = {
    "language": "es",
    "basic_info": {
        "name": "MARTIN SANCHEZ URREGO",
        "title": "Ingeniero de Software",
        "phone": "+57 304 2621096",
        "email": "martinsanchez2704@gmail.com",
        "portfolio_url": "https://nitram2704.github.io/CV/CV.html",
        "linkedin_url": "https://www.linkedin.com/in/martin-sanchez-urrego-3b14133a4/",
        "github_url": "https://github.com/Nitram2704"
    },
    "summary": "Ingeniero de Software disciplinado con una gran capacidad de razonamiento lógico para la resolución de problemas y la optimización de soluciones. Experto en el aprovechamiento de un conjunto de habilidades de pila completa para ofrecer soluciones de alto impacto, incluidas herramientas de automatización impulsadas por **IA** y aplicaciones móviles escalables. Experiencia en tecnologías como **.NET**, **React** y plataformas en la nube como **Azure**. Habilidad demostrada para automatizar procesos complejos, demostrada por una reducción del **90%** en el esfuerzo manual en la adaptación de **CV** y una reducción del **70%** en el tiempo de mantenimiento de las pruebas.",
    "education": [
        {"degree": "Tecnico en asistente en desarrollo de software", "institution": "Cesde", "year": "2020-2021"},
        {"degree": "Ingenieria en desarrollo de software", "institution": "IU Pascual Bravo", "year": "2022-Presente"}
    ],
    "certifications": [
        {"name": "Microsoft Azure Fundamentals (AZ-900)", "issuer": "Microsoft", "year": "2026"}
    ],
    "skills": {
        "backend": [".NET (C#)", ".NET Core API", "Node.js (Express)", "Java", "Spring Boot", "Python", "FastAPI"],
        "frontend": ["TypeScript", "Vue.js 3", "React", "Angular", "React Native", "Expo", "JavaScript", "Tailwind CSS"],
        "databases": ["SQL Server", "PostgreSQL", "MySQL", "Firebase", "Supabase"],
        "cloud": ["Azure", "Supabase", "Firebase"]
    },
    "languages": [
        {"language": "Español", "level": "Nativo"},
        {"language": "Inglés", "level": "B2"}
    ],
    "experience": [
        {
            "role": "Ingeniero de Software",
            "company": "Smart-Adapt CV",
            "duration": "Ene 2023 - Actual",
            "highlights": [
                "Situación: Se necesitaba agilizar y automatizar el proceso de adaptación de **CV** para vacantes de empleo específicas.",
                "Tarea: Construir un motor de optimización de carrera impulsado por **IA** que adapte los **CV** a las descripciones de los puestos de trabajo utilizando **LLM** locales.",
                "Acción: Desarrollé Smart-Adapt **CV** utilizando **Python** y **FastAPI** para el backend, **React** para el frontend y **Ollama** con **GLM-4.7 LLM**, integrado con una base de datos **PostgreSQL**.",
                "Resultado: Se automatizó el proceso de adaptación de **CV**, reduciendo el esfuerzo manual en un **90%**, lo que mejoró la eficiencia de las aplicaciones."
            ]
        },
        {
            "role": "Desarrollador de Aplicaciones Móviles",
            "company": "App Fitness",
            "duration": "Ene 2022 - Dic 2022",
            "highlights": [
                "Situación: Se requería una aplicación móvil fácil de usar centrada en el seguimiento de la salud, las rutinas de ejercicios y el seguimiento del progreso físico.",
                "Tarea: Diseñar e implementar una aplicación móvil para mejorar la participación del usuario y promover hábitos saludables.",
                "Acción: Diseñé una aplicación móvil multiplataforma utilizando **React Native** y **Expo**, aprovechando **Firebase** para los servicios de backend.",
                "Resultado: Se aumentó la participación de los usuarios a través de desafíos de fitness gamificados y una experiencia de usuario optimizada."
            ]
        },
        {
            "role": "Desarrollador de Software",
            "company": "Sistema POS",
            "duration": "Ene 2021 - Dic 2021",
            "highlights": [
                "Situación: Se necesitaba un sistema de punto de venta para la gestión minorista, totalmente integrado con **WooCommerce** para sincronizar el inventario y las ventas con un sitio web de comercio electrónico en vivo.",
                "Tarea: Desarrollar un sistema de punto de venta robusto y escalable.",
                "Acción: Implementé el sistema utilizando **Java**, **Spring Boot** y **MySQL**, integrando la **API** de **WooCommerce** y servicios **REST**.",
                "Resultado: Se procesaron más de **1.000** transacciones diarias con un tiempo de actividad del **99,9%**."
            ]
        }
    ],
    "labels": {
        "contact": "Contacto",
        "education": "Educación",
        "certifications": "Certificaciones",
        "skills": "Habilidades",
        "languages": "Idiomas",
        "summary": "Resumen Profesional",
        "project_experience": "Experiencia en Proyectos",
        "references": "Referencias"
    }
}

from core.generator import render_cv_html, generate_pdf

# ... (data remains the same)

print("Rendering HTML...")
html_content = render_cv_html(data)

with open("outputs/debug_overflow.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generating PDF...")
generate_pdf(html_content, "outputs/debug_overflow.pdf")
print("PDF generated: outputs/debug_overflow.pdf")

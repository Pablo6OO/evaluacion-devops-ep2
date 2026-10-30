# Evaluación Parcial 2 - Pipeline CI/CD DevSecOps

**Asignatura:** Ingeniería DevOps (`DOY0101`)  
**Institución:** Duoc UC  
**Proyecto:** Multi-servicio CI/CD con Gobernanza y Seguridad  
**Repositorio:** `evaluacion-devops-ep2`

---

## Visión General del Proyecto

Este proyecto implementa una solución automatizada de Integración y Entrega Continua (CI/CD) bajo principios DevSecOps. Utiliza **GitHub Actions** para orquestar la compilación, pruebas unitarias automatizadas, análisis estático de código (SAST), escaneo de vulnerabilidades en dependencias (SCA) y la construcción de imágenes de contenedor orquestadas mediante **Docker Compose**.

---

## Arquitectura de Microservicios

El sistema está dividido en dos microservicios independientes, cada uno implementado con diferentes tecnologías y estrategias de prueba:

### 1. Microservicio Python (`microservicio-python`)
* **Stack:** Python 3.11
* **Framework de Pruebas:** `pytest` y `pytest-cov`
* **Función:** Módulo de validación de entradas de usuario (formatos de correo electrónico y normalización de cadenas).
* **Contenerización:** Imagen liviana basada en `python:3.11-slim`.

### 2. Microservicio Java (`microservicio-java`)
* **Stack:** Java 17 (Eclipse Temurin) + Apache Maven
* **Framework de Pruebas:** JUnit 5 y `jacoco-maven-plugin`
* **Función:** Módulo de cálculo y operaciones matemáticas.
* **Contenerización:** Construcción multietapa (*Multi-stage build*) empaquetada con Maven y ejecutada sobre `eclipse-temurin:17-jre-alpine`.

---

## Pipeline CI/CD y Calidad (GitHub Actions)

El workflow está definido en `.github/workflows/main.yml` y se activa automáticamente ante eventos `push` o `pull_request` en la rama principal `main`.

### Etapas del Pipeline:
1. **Checkout del Código:** Descarga del repositorio con historial de commits para la trazabilidad de análisis.
2. **Pruebas Automatizadas Python:** Instalación de dependencias y ejecución de `pytest` generando reportes de cobertura XML (`coverage.xml`).
3. **Pruebas Automatizadas Java:** Compilación y ejecución de pruebas de JUnit con generación de reporte de cobertura de código mediante **JaCoCo**.
4. **Análisis de Seguridad SAST (SonarCloud):** Inspección estática de código para detectar *code smells*, errores de lógica y vulnerabilidades en ambos lenguajes.
5. **Análisis de Seguridad SCA (Snyk):** Escaneo de vulnerabilidades conocidas en las dependencias de los proyectos.
6. **Verificación de Contenedores:** Construcción y validación de las imágenes a través de `docker compose build`.

---

## Orquestación y Límites de Recursos (`docker-compose.yml`)

Para cumplir con los requisitos de gobernanza, estabilidad y desempeño, la orquestación define límites estrictos de hardware por contenedor:

```yaml
services:
  app-python:
    build:
      context: ./microservicio-python
    container_name: ms-python-app
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: "0.5"

  app-java:
    build:
      context: ./microservicio-java
    container_name: ms-java-app
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
```

### Ejecución Local:
```bash
# Levantar el entorno orquestado
docker compose up -d --build

# Verificar estado de los contenedores
docker compose ps
```

---

## Trazabilidad y Seguridad

* **Gobernanza de Secrets:** Las credenciales sensibles (`SONAR_TOKEN` y `SNYK_TOKEN`) están resguardadas como *Repository Secrets* en GitHub, impidiendo su exposición en el código fuente.
* **Trazabilidad:** Cada cambio subido al repositorio activa un ciclo de validación cuya respuesta técnica (éxito o fallo) queda registrada en la pestaña **Actions** de GitHub y reflejada en los paneles de SonarCloud y Snyk.

---

## Declaración del Uso Ético de Inteligencia Artificial

En conformidad con las políticas institucionales de Duoc UC respecto al uso de herramientas de Inteligencia Artificial en evaluaciones:

* **Herramientas empleadas:** Asistente conversacional de Inteligencia Artificial (Gemini).
* **Alcance de la colaboración:** La herramienta de IA fue utilizada como tutor técnico de apoyo, orientando en la navegación de las plataformas externas (configuración de proyectos y generación de tokens en SonarCloud y Snyk), asistiendo en la estructuración sintáctica de archivos de configuración (`.yml`, `sonar-project.properties`, `pom.xml`) y apoyando activamente en la redacción, orden y formato técnico de este documento `README.md`.
* **Validación y Autoría:** La instalación de dependencias, ejecución de comandos en la terminal local, depuración de errores, pruebas unitarias, construcción local de contenedores Docker y el envío de cambios (`push`) al repositorio de GitHub fueron ejecutados, probados y verificados manualmente por el estudiante.
```
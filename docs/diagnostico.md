# Linea base de ejecucion

# 1.1. Los cuatro defectos

## 1. publicar se ejecuta aunque falle validar

No existe "needs" dentro de validar, en el archivo pipeline.yml (debería ir por las líneas 42-44, junto a name y runs-on). Por ello, a pesar de que validar falle, publicar se ejecuta, permitiendo que se publique el artefacto aunque este esté fallido. 

## 2. El pipeline ignora el lockfile y usa rangos abiertos

Los jobs instalan dependencias desde requirements.txt (líneas 26 y 56 de pipeline.yml), con rangos abiertos, ignorando el lockfile. Esto rompe su propósito, haciendo que no haya garantía de que validar y publicar usen las mismas versiones entre sí.

## 3. No se cachean las dependencias

Se repite el código Preparar Python para vaidar y para publicar (18-21, 48-51 en pipeline.yml). Como consecuencia, cada paso reinstala las dependencias desde cero, lo cual es un error de eficiencia, y es una razón de la demora del pipeline.

## 4. El artifact publicado no incluye la versión en el nombre

En ninguna parte de pipeline.yml se verifica o actualiza la versión, por lo que se borra el artefacto de la ejecución anterior. Además, unido al defecto 1, se publica aunque haya fallado la validación. Se pierde la garantía de versionar correctamente el software.

# 1.2. El defecto que explica la duración

El defecto que explica el tiempo registrado es el número 3, ya que debido a este se tienen que instalar todas las dependencias dos veces, lo cual es innecesario y resulta en el desperdicio de tiempo.

# 1.3. El vínculo con su caso

El defecto que ataca la restricción del caso es el 3, ya que este aumenta innecesariamente el lead time, similar a como era en el caso en que mucho tiempo se perdía en esperas innecesarias.

# 1.4. La métrica DORA

Se espera mover la métrica "Lead time para cambios", ya que a partir de este cambio, se reduce el cambio ocurrido desde que se integra el cambio (commit) hasta que corra en producción.

# 1.5. El proxy

Se va a medir el promedio de las duraciones registradas en linea-base.md, considerando este como el lead time.
# Forense · USB Perdido

| | |
|---|---|
| **Categoría** | Forense |
| **Dificultad** | medio |
| **Puntaje base** | 275 (dinámico) |
| **Despliegue** | estático (archivo de entrega) |
| **Flag** | `CITT{nada_se_borra_del_todo}` |

## Enunciado (para el jugador)

Encontramos un pendrive 'vacío'. La imagen de disco dice otra cosa. Recupera lo que borraron.

## Pista (configurable en CTFd)

> Borrar no es lo mismo que destruir. Prueba foremost o photorec sobre la imagen.

## Solución (writeup — NO publicar)

`foremost usb.img` o `photorec` recuperan un archivo borrado (imagen/txt) con la flag. También `strings usb.img | grep CITT` puede funcionar si no se sobrescribió.

## Construcción del reto

Generador crea una imagen FAT, escribe un archivo con la flag, lo 'borra' y deja el contenido recuperable. Ver entrega/build.sh.

**Archivos de entrega:** `entrega/usb.img`


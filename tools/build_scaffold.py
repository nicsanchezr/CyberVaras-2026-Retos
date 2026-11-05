#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_scaffold.py — Genera el árbol de retos de CyberVaras 2026.
Crea, por cada reto: challenge.yml (ctfcli), flag.txt y README.md (enunciado +
writeup + receta de build), más la carpeta entrega/.

Uso:  python3 tools/build_scaffold.py
Idempotente: regenera challenge.yml / flag.txt / README.md. NO pisa código fuente
de apps web ni generadores (esos viven aparte y no los toca este script).
"""
import os, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHOR = "Track Ciberseguridad · CITT Antonio Varas"
DECAY = 25
CAT_LABEL = {
    "warmup": "Warmup", "web": "Web", "crypto": "Crypto",
    "forense": "Forense", "redes": "Redes", "osint": "OSINT",
    "reversing": "Reversing",
}

# Plan B: los 6 web corren como instancias fijas en el droplet de retos,
# publicadas por Caddy en un subdominio cada una. Mapa slug -> subdominio.
WEB_HOST = "retos.cybervaras.xyz"
WEB_SUBDOMAIN = {
    "login_injectado": "login",
    "robots_traviesos": "robots",
    "cambia_el_id":     "idor",
    "galleta_falsa":    "cookie",
    "token_quebrado":   "jwt",
    "incluyeme":        "lfi",
}
def web_url(slug):
    return f"https://{WEB_SUBDOMAIN[slug]}.{WEB_HOST}"

# cada reto: slug, cat, title, diff, points, flag, deploy, hint, files, enunciado, solucion, build
C = []
def add(**k): C.append(k)

# ---------------------------------------------------------------- WARMUP
add(slug="insert_coin", cat="warmup", title="insert_coin", diff="fácil", points=50,
    flag="CITT{bienvenido_a_cybervaras_2026}", deploy="static", hint=None, files=[],
    enunciado="Toda buena partida empieza metiendo una ficha. La flag está escondida a plena vista en la propia web del campeonato (https://2026.cybervaras.xyz). Mira donde nadie mira.",
    solucion="En el pie de la página aparece el texto `insert_coin_to_continue_`. La flag está como comentario HTML / atributo data cerca de ese elemento (o en el CSS `::after`). Ver código fuente con Ctrl+U o DevTools.",
    build="Sembrar la flag como comentario HTML en el footer del repo de la web pública (nicsanchezr/CyberVaras-2026), p. ej. `<!-- CITT{...} -->` junto a insert_coin_to_continue_.")

add(slug="terminal_basica", cat="warmup", title="Terminal Básica", diff="fácil", points=75,
    flag="CITT{grep_es_tu_amigo}", deploy="static", hint=None, files=["pistas.tar.gz"],
    enunciado="Te dejamos un montón de archivos en un .tar.gz. En uno de ellos, en alguna línea perdida, está la flag. Descomprime y busca con las herramientas de siempre.",
    solucion="`tar xzf pistas.tar.gz` y luego `grep -rao 'CITT{[^}]*}' .` (recursivo, texto). La flag está dentro de uno de ~200 archivos de ruido.",
    build="Generador crea 200 archivos .txt de basura y mete la flag en una línea de uno. Empaqueta en pistas.tar.gz. Ver build/build.sh.")

add(slug="capas", cat="warmup", title="Capas", diff="fácil", points=100,
    flag="CITT{capa_tras_capa_tras_capa}", deploy="static", hint=None, files=["capas.txt"],
    enunciado="La flag está envuelta en varias capas de codificación (base64, hexadecimal y un corrimiento de letras). Ve pelando una a una hasta llegar al centro.",
    solucion="Cadena exacta: base64 → hex → base64 → rot13. Resolver con CyberChef 'Magic' (recursivo), o a mano: `base64 -d`, `xxd -r -p`, `base64 -d`, y finalmente rot13.",
    build="Generador aplica base64(hex(base64(rot13(flag)))) y guarda en capas.txt. Ver build/build.py.")

# ---------------------------------------------------------------- WEB (whale)
add(slug="login_injectado", cat="web", title="Login Injectado", diff="fácil", points=100,
    flag="CITT{sql_injection_101}", deploy="whale", hint=None, files=[],
    enunciado="Un panel de login de lo más normal. ¿Seguro que valida bien lo que escribes? Entra como administrador.",
    solucion="Inyección SQL clásica de autenticación: usuario `admin' -- ` o `' OR '1'='1' -- `. La consulta concatena sin parametrizar. Al autenticarse como admin se muestra la flag.",
    build="App Flask + SQLite en app/. Query vulnerable por f-string. Whale: imagen por equipo. Ver app/ y docker-compose.yml.")

add(slug="robots_traviesos", cat="web", title="Robots Traviesos", diff="fácil", points=125,
    flag="CITT{nunca_confies_en_robots_txt}", deploy="whale", hint=None, files=[],
    enunciado="El administrador creyó que esconder rutas en robots.txt bastaba. Spoiler: no basta.",
    solucion="Leer `/robots.txt` → lista rutas 'Disallow' como `/panel-oculto/` y `/backup/`. En `/backup/app.py.bak` (o `/.git/`) queda expuesto el código con la flag, o un endpoint oculto la devuelve.",
    build="App Flask sirve robots.txt con Disallow a /backup/. En /backup/ hay un .bak con la flag. Ver app/.")

add(slug="cambia_el_id", cat="web", title="Cambia el ID", diff="medio", points=200,
    flag="CITT{idor_acceso_horizontal}", deploy="whale", hint=None, files=[],
    enunciado="Inicia sesión con la cuenta de prueba que te damos y revisa tu perfil. La URL tiene un número... ¿qué pasa si lo cambias? Encuentra el perfil del administrador.",
    solucion="IDOR: tras login, el perfil está en `/profile?id=1002`. Cambiando a `/profile?id=1` (o iterando) se accede al perfil admin sin control de autorización. La flag está en el perfil admin.",
    build="App Flask, usuarios en SQLite, endpoint /profile?id= sin verificar propiedad. Credenciales de prueba fijas. Ver app/.")

add(slug="galleta_falsa", cat="web", title="Galleta Falsa", diff="medio", points=250,
    flag="CITT{cookies_no_son_para_confiar}", deploy="whale", hint=None, files=[],
    enunciado="La aplicación recuerda quién eres con una cookie. Pero la cookie dice más de lo que debería... y nadie comprueba que no la toques.",
    solucion="La cookie `role=user` (o un valor base64 `{'user':'guest','role':'user'}`) no está firmada. Cambiarla a `role=admin` (re-codificando el base64) da acceso al panel admin con la flag.",
    build="App Flask setea cookie de sesión casera (base64 JSON, sin firmar). /admin exige role=admin. Ver app/.")

add(slug="token_quebrado", cat="web", title="Token Quebrado", diff="difícil", points=350,
    flag="CITT{jwt_alg_none_es_peligroso}", deploy="whale",
    hint="El header de un JWT dice qué algoritmo usar para verificarlo. ¿Qué pasa si el servidor le cree al header?", files=[],
    enunciado="La API entrega un JWT al iniciar sesión. El endpoint /admin exige un token de administrador. Falsifica uno.",
    solucion="El verificador acepta `alg: none` (o una clave HS256 débil de diccionario). Forjar un JWT con payload `{'user':'admin','role':'admin'}` y alg none (firma vacía), o crackear el secreto con jwt_tool/hashcat y re-firmar. /admin devuelve la flag.",
    build="App Flask, verificación JWT mal configurada (acepta none / secreto 'secret'). Ver app/.")

add(slug="incluyeme", cat="web", title="Inclúyeme", diff="difícil", points=400,
    flag="CITT{lfi_hasta_la_raiz}", deploy="whale",
    hint="El parámetro de idioma termina siendo una ruta de archivo. ¿Hasta dónde puedes subir?", files=[],
    enunciado="La página carga 'vistas' según un parámetro. Parece inofensivo, pero el servidor incluye el archivo que le pidas. Lee la flag del sistema.",
    solucion="LFI en `/?page=home`. Path traversal `?page=../../../../etc/passwd` confirma. La flag está en un archivo fuera del webroot, p. ej. `?page=../../../../flag.txt` o vía filtros php/wrappers. Para el reto, la flag vive en /flag.txt dentro del contenedor.",
    build="App Flask incluye plantillas por nombre sin sanitizar (open(path).read()). flag.txt en / del contenedor. Ver app/.")

# ---------------------------------------------------------------- CRYPTO (static)
add(slug="cesar_recargado", cat="crypto", title="César Recargado", diff="fácil", points=100,
    flag="CITT{el_cesar_no_protege_nada}", deploy="static", hint=None, files=["mensaje.txt"],
    enunciado="Un mensaje cifrado con un método que tiene 2000 años. Rómpelo.",
    solucion="Cifrado César con desplazamiento fijo. Probar los 25 corrimientos (brute force) o análisis de frecuencia. El prefijo `CITT{` ayuda a encontrar el shift.",
    build="Generador cifra la flag (y un texto señuelo) con César shift fijo. Ver build/build.py.")

add(slug="xor_de_bolsillo", cat="crypto", title="XOR de Bolsillo", diff="fácil", points=125,
    flag="CITT{xor_un_byte_es_trivial}", deploy="static", hint=None, files=["cipher.hex"],
    enunciado="Cifrado XOR con una clave de un solo byte. 256 posibilidades. Tú puedes.",
    solucion="Fuerza bruta de los 256 bytes de clave; el candidato legible (empieza con `CITT{`) es la flag. CyberChef 'XOR Brute Force' o script en Python.",
    build="Generador XOR de la flag con un byte fijo, salida en hex. Ver build/build.py.")

add(slug="hash_expuesto", cat="crypto", title="Hash Expuesto", diff="medio", points=200,
    flag="CITT{rockyou_lo_tenia}", deploy="static", hint=None, files=["hashes.txt"],
    enunciado="Filtramos una tabla de hashes. Varios son contraseñas comunes. Crackéalas: la flag se arma con las contraseñas recuperadas.",
    solucion="Identificar tipo (MD5/SHA1) con hashid. Crackear con `john`/`hashcat` + rockyou. Las palabras recuperadas, concatenadas con `_`, forman el contenido de la flag.",
    build="Generador toma palabras débiles (de rockyou), las hashea, y define la flag como su unión. Ver build/build.py.")

add(slug="xor_reciclado", cat="crypto", title="XOR Reciclado", diff="medio", points=275,
    flag="CITT{clave_repetida_mala_idea}", deploy="static", hint=None, files=["cipher.bin"],
    enunciado="Reusaron una clave corta para cifrar un texto largo con XOR. Ese es su error.",
    solucion="XOR de clave repetida (Vigenère binario). Estimar longitud de clave (Kasiski/Hamming), luego resolver byte a byte por frecuencia. xortool: `xortool cipher.bin`. La flag va embebida en el texto plano.",
    build="Generador XOR de un texto largo (que contiene la flag) con clave de ~5-7 bytes repetida. Ver build/build.py.")

add(slug="rsa_fragil", cat="crypto", title="RSA Frágil", diff="medio", points=250,
    flag="CITT{primos_pequenos_rsa_roto}", deploy="static",
    hint="n es pequeño. ¿Qué pasa si lo factorizas? Prueba factordb.", files=["rsa.txt"],
    enunciado="Te damos n, e y c de un cifrado RSA. El problema: eligieron primos demasiado pequeños.",
    solucion="Factorizar n (pequeño) con factordb o sympy.factorint → p,q. Calcular φ=(p-1)(q-1), d=inverse(e,φ), m=c^d mod n. Convertir m a bytes → flag.",
    build="Generador crea RSA con p,q pequeños, cifra la flag. Guarda n,e,c. Ver build/build.py.")

# ---------------------------------------------------------------- FORENSE (static)
add(slug="metadatos_delatores", cat="forense", title="Metadatos Delatores", diff="fácil", points=100,
    flag="CITT{los_metadatos_hablan}", deploy="static", hint=None, files=["foto.jpg"],
    enunciado="Una foto de lo más común. Pero las fotos guardan más de lo que muestran. Revisa sus metadatos.",
    solucion="`exiftool foto.jpg`. La flag está en un campo EXIF (Comment / Artist / UserComment).",
    build="Generador crea un JPG y escribe la flag en EXIF UserComment (piexif/exiftool). Ver build/build.py.")

add(slug="pixel_oculto", cat="forense", title="Píxel Oculto", diff="fácil", points=150,
    flag="CITT{el_bit_menos_significativo}", deploy="static", hint=None, files=["secreto.png"],
    enunciado="Esta imagen esconde texto en sus bits menos significativos. Extráelo.",
    solucion="Esteganografía LSB. Usar zsteg (`zsteg secreto.png`) o stegsolve, o script que lee el LSB del canal R. También probar `strings`/`binwalk` primero.",
    build="Generador incrusta la flag en el LSB del canal rojo de un PNG. Ver build/build.py.")

add(slug="zip_terco", cat="forense", title="ZIP Terco", diff="medio", points=225,
    flag="CITT{binwalk_siempre_gana}", deploy="static", hint=None, files=["portada.png"],
    enunciado="Una imagen inocente... que pesa demasiado. Algo trae pegado detrás.",
    solucion="`binwalk portada.png` revela un ZIP anexado. `binwalk -e` o `unzip` lo extrae. El ZIP pide contraseña; la pista está en un comentario del PNG o en los metadatos. Dentro, la flag.",
    build="Generador concatena un ZIP (con flag.txt, protegido) al final de un PNG; pone la pass en un chunk tEXt. Ver build/build.py.")

add(slug="sonido_sospechoso", cat="forense", title="Sonido Sospechoso", diff="medio", points=250,
    flag="CITT{escucha_el_espectrograma}", deploy="static",
    hint="No se escucha, se ve. Abre el espectrograma en Audacity o Sonic Visualiser.", files=["senal.wav"],
    enunciado="Un audio con un pitido raro. La flag no está en lo que oyes, sino en lo que ves.",
    solucion="Abrir el WAV en Audacity/Sonic Visualiser y ver el espectrograma: la flag está 'dibujada' en las frecuencias.",
    build="Generador sintetiza un WAV cuyo espectrograma dibuja el texto de la flag. Ver build/build.py (requiere numpy).")

add(slug="bitacora_rota", cat="forense", title="Bitácora Rota", diff="medio", points=250,
    flag="CITT{el_log_delata_al_atacante}", deploy="static", hint=None, files=["access.log"],
    enunciado="Alguien atacó este servidor web. Entre miles de líneas de log hay una serie de peticiones sospechosas. Reconstruye el ataque y encuentra la flag.",
    solucion="Filtrar el access.log: una IP hace fuzzing (muchos 404) y luego 200 en una ruta rara. Esa IP, en una petición, exfiltra la flag codificada en base64 dentro de un parámetro/User-Agent. Decodificar.",
    build="Generador crea un access.log realista con ruido + la secuencia del atacante; la flag va en base64 en un parámetro. Ver build/build.py.")

add(slug="usb_perdido", cat="forense", title="USB Perdido", diff="medio", points=275,
    flag="CITT{nada_se_borra_del_todo}", deploy="static",
    hint="Borrar no es lo mismo que destruir. Prueba foremost o photorec sobre la imagen.", files=["usb.img"],
    enunciado="Encontramos un pendrive 'vacío'. La imagen de disco dice otra cosa. Recupera lo que borraron.",
    solucion="`foremost usb.img` o `photorec` recuperan un archivo borrado (imagen/txt) con la flag. También `strings usb.img | grep CITT` puede funcionar si no se sobrescribió.",
    build="Generador crea una imagen FAT, escribe un archivo con la flag, lo 'borra' y deja el contenido recuperable. Ver build/build.sh.")

# ---------------------------------------------------------------- REDES (static)
add(slug="credenciales_al_aire", cat="redes", title="Credenciales al Aire", diff="fácil", points=150,
    flag="CITT{http_en_texto_claro}", deploy="static", hint=None, files=["captura.pcap"],
    enunciado="Capturamos tráfico de una red. Alguien inició sesión por HTTP (sin HTTPS). Sus credenciales viajaron en claro... y una de ellas es la flag.",
    solucion="Abrir en Wireshark, seguir el stream HTTP del POST de login, o `tshark -r captura.pcap -Y http.request.method==POST`. La contraseña enviada es la flag.",
    build="Generador (scapy) arma un pcap con un POST HTTP cuyo campo password es la flag. Ver build/build.py.")

add(slug="telnet_indiscreto", cat="redes", title="Telnet Indiscreto", diff="fácil", points=150,
    flag="CITT{telnet_es_inseguro}", deploy="static", hint=None, files=["telnet.pcap"],
    enunciado="Telnet no cifra nada. Reconstruye la sesión de este pcap y lee lo que el usuario escribió.",
    solucion="Seguir el TCP stream del puerto 23. El usuario escribe un comando (p. ej. `echo CITT{...}`) visible carácter a carácter en el stream.",
    build="Generador (scapy) simula sesión Telnet con la flag tecleada. Ver build/build.py.")

add(slug="transferencia_ftp", cat="redes", title="Transferencia FTP", diff="medio", points=225,
    flag="CITT{ftp_export_objects}", deploy="static", hint=None, files=["ftp.pcap"],
    enunciado="En esta captura alguien transfirió un archivo por FTP. Recupéralo: dentro está la flag.",
    solucion="Identificar el canal de datos FTP (puerto negociado por PASV). En Wireshark: Follow TCP Stream del canal de datos → guardar bytes como archivo. O `tshark` export. El archivo contiene la flag.",
    build="Generador (scapy) simula control FTP + canal de datos transfiriendo un .txt con la flag. Ver build/build.py.")

add(slug="dns_curioso", cat="redes", title="DNS Curioso", diff="medio", points=300,
    flag="CITT{exfiltracion_por_dns}", deploy="static",
    hint="Mira los subdominios consultados. ¿Por qué son tan largos y raros? Pruébalos como base32/hex.", files=["dns.pcap"],
    enunciado="Un host hace un montón de consultas DNS a un dominio sospechoso, con subdominios larguísimos. Están exfiltrando datos. Recupéralos.",
    solucion="Extraer los qname de las consultas (`tshark -r dns.pcap -Y dns -T fields -e dns.qry.name`). Los subdominios son trozos hex/base32 que, concatenados y decodificados, dan la flag.",
    build="Generador (scapy) crea consultas DNS cuyos subdominios son la flag troceada en hex. Ver build/build.py.")

# ---------------------------------------------------------------- OSINT (static)
add(slug="donde_estoy", cat="osint", title="¿Dónde Estoy?", diff="fácil", points=150,
    flag="CITT{definir_ciudad_lugar}", deploy="static",
    hint=None, files=["lugar.jpg", "pista.txt"],
    enunciado="Esta foto NO tiene metadatos de ubicación. Pero se reconoce el lugar. Identifícalo: la flag es el nombre del lugar en el formato que indica la pista.",
    solucion="Reconocer el hito visible (edificio/monumento reconocible). Búsqueda inversa de imagen (Google Lens/Yandex). La flag se arma con el nombre del lugar normalizado según pista.txt: CITT{ciudad_lugar}.",
    build="MANUAL (OBLIGATORIO antes de publicar): 1) reemplazar lugar.jpg (hoy es un placeholder de prueba, NO geolocalizable) por una foto real de un lugar reconocible SIN EXIF de GPS; 2) fijar la flag en flag.txt al formato CITT{ciudad_lugar} de ESE lugar (reemplaza el placeholder CITT{definir_ciudad_lugar}). El enunciado y pista.txt ya prometen ese formato. Verificar que la flag coincide con lo que da una búsqueda inversa.")

add(slug="rastro_social", cat="osint", title="Rastro Social", diff="medio", points=250,
    flag="CITT{un_alias_los_une_a_todos}", deploy="static",
    hint=None, files=["dossier.txt"],
    enunciado="Te damos el nombre de un personaje ficticio que creamos para el campeonato. Usa el mismo alias en varias plataformas. Síguele el rastro hasta donde dejó la flag.",
    solucion="A partir del alias, buscar con sherlock/whatsmyname el perfil en varias redes (todas controladas por la organización). En la bio/último post de una de ellas está la flag.",
    build="MANUAL (OBLIGATORIO antes de publicar): crear un perfil ficticio con un alias único en 2-3 plataformas (o páginas propias) y dejar la flag de este reto (ver fila Flag arriba) en una de las bios. Luego escribir ese alias real en dossier.txt (hoy va en blanco). IMPORTANTE: la flag NO debe aparecer en dossier.txt ni en ningún archivo entregado al jugador; solo en el perfil sembrado.")

add(slug="el_repo_olvidado", cat="osint", title="El Repo Olvidado", diff="medio", points=225,
    flag="CITT{git_log_recuerda_todo}", deploy="static",
    hint=None, files=["pista.txt"],
    enunciado="Un desarrollador 'borró' una credencial de su repositorio público. Pero git nunca olvida. Encuentra la flag en el historial.",
    solucion="Clonar el repo sembrado. La flag se 'eliminó' en un commit posterior pero sigue en el historial: `git log -p`, `git show <commit>` del archivo borrado, o buscar en todos los objetos.",
    build="MANUAL (OBLIGATORIO antes de publicar): crear un repo público (org del track): un commit agrega un archivo con la flag de este reto (ver fila Flag arriba) y un commit posterior la 'borra'. Luego escribir la URL real del repo en pista.txt (hoy va en blanco). IMPORTANTE: la flag NO debe aparecer en pista.txt ni en archivos entregados; solo en el historial del repo.")

# ---------------------------------------------------------------- REVERSING (static)
add(slug="clave_a_la_vista", cat="reversing", title="Clave a la Vista", diff="medio", points=200,
    flag="CITT{strings_revela_la_clave}", deploy="static", hint=None, files=["crackme"],
    enunciado="Un binario te pide una contraseña. Si aciertas, te da la flag. La contraseña está más a la vista de lo que crees.",
    solucion="`strings crackme | less` muestra la contraseña comparada en claro. Ingresarla devuelve la flag. También se ve en Ghidra en la comparación strcmp.",
    build="Fuente C compara input con password en claro; si coincide imprime la flag. Compilar con tools. Ver src/ y build.sh.")

add(slug="script_enredado", cat="reversing", title="Script Enredado", diff="medio", points=250,
    flag="CITT{ofuscar_no_es_cifrar}", deploy="static", hint=None, files=["reto.py"],
    enunciado="Un script de Python ofuscado que, al ejecutarse, valida una flag. Pero ofuscar no es cifrar: desenrédalo.",
    solucion="El script tiene la flag como base64/rot/marshal anidado. En vez de ejecutarlo a ciegas, reemplazar el `exec/eval` final por `print`, o ir decodificando las capas a mano, para revelar la flag.",
    build="Generador produce reto.py con la flag ofuscada en varias capas (base64 + marshal). Ver src/build.py.")

add(slug="xor_en_binario", cat="reversing", title="XOR en Binario", diff="difícil", points=400,
    flag="CITT{xor_en_tiempo_de_ejecucion}", deploy="static",
    hint="La flag no está en strings: se construye en memoria. Pon un breakpoint después del bucle XOR.", files=["xorme"],
    enunciado="La flag no aparece con strings porque el binario la arma en tiempo de ejecución, byte a byte, con XOR. Tienes que analizarlo.",
    solucion="En Ghidra se ve un arreglo de bytes XOR-eados con una clave y un bucle que reconstruye la flag. Opciones: replicar el XOR en Python con los bytes y la clave del binario, o en gdb poner breakpoint tras el bucle y leer memoria.",
    build="Fuente C guarda la flag XOR-eada y la descifra en runtime (no la imprime directo). Compilar. Ver src/ y build.sh.")

# ---------------------------------------------------------------- escritura
def yml_escape_block(text):
    return "\n".join("  " + line for line in text.split("\n"))

def write_challenge(ch):
    cat = ch["cat"]; slug = ch["slug"]
    d = os.path.join(ROOT, cat, slug)
    os.makedirs(os.path.join(d, "entrega"), exist_ok=True)
    # Plan B: puntaje FIJO para todos los retos -> minimum == initial (decay inerte).
    minimum = ch["points"]
    is_web = ch["deploy"] == "whale"   # 6 retos web: instancia fija externa (Caddy)
    ctype = "dynamic"                  # todos dynamic; los web NO son dynamic_docker

    # descripción: a los web se les anexa la URL del objetivo
    descripcion = ch["enunciado"]
    if is_web:
        descripcion = descripcion + f"\n\nObjetivo en: {web_url(slug)}"

    # challenge.yml
    y = []
    y.append(f'name: "{ch["title"]}"')
    y.append(f'author: "{AUTHOR}"')
    y.append(f'category: {CAT_LABEL[cat]}')
    y.append('description: |')
    y.append(yml_escape_block(descripcion))
    y.append(f'type: {ctype}')
    y.append(f'value: {ch["points"]}')
    y.append('extra:')
    y.append(f'  initial: {ch["points"]}')
    y.append(f'  decay: {DECAY}')
    y.append(f'  minimum: {minimum}        # == initial -> puntaje fijo')
    if is_web:
        y.append(f'  # instancia fija en {web_url(slug)} (droplet retos, vía Caddy)')
    y.append('flags:')
    y.append(f'  - {ch["flag"]}')
    y.append('tags:')
    y.append(f'  - {ch["diff"]}')
    if ch["files"]:
        y.append('files:')
        for f in ch["files"]:
            y.append(f'  - entrega/{f}')
    y.append('state: hidden')
    y.append('version: "0.1"')
    with open(os.path.join(d, "challenge.yml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(y) + "\n")

    # flag.txt
    with open(os.path.join(d, "flag.txt"), "w", encoding="utf-8") as fh:
        fh.write(ch["flag"] + "\n")

    # README.md
    r = []
    r.append(f'# {CAT_LABEL[cat]} · {ch["title"]}')
    r.append('')
    r.append(f'| | |')
    r.append(f'|---|---|')
    r.append(f'| **Categoría** | {CAT_LABEL[cat]} |')
    r.append(f'| **Dificultad** | {ch["diff"]} |')
    r.append(f'| **Puntaje** | {ch["points"]} (fijo: minimum == initial) |')
    r.append(f'| **Despliegue** | {("instancia web fija · " + web_url(slug) + " (droplet retos, vía Caddy)") if is_web else "estático (archivo de entrega)"} |')
    r.append(f'| **Flag** | `{ch["flag"]}` |')
    r.append('')
    r.append('## Enunciado (para el jugador)')
    r.append('')
    r.append(descripcion)
    r.append('')
    if ch["hint"]:
        r.append('## Pista (configurable en CTFd)')
        r.append('')
        r.append(f'> {ch["hint"]}')
        r.append('')
    r.append('## Solución (writeup — NO publicar)')
    r.append('')
    r.append(ch["solucion"])
    r.append('')
    r.append('## Construcción del reto')
    r.append('')
    r.append(ch["build"])
    r.append('')
    if ch["files"]:
        r.append('**Archivos de entrega:** ' + ", ".join(f'`entrega/{f}`' for f in ch["files"]))
        r.append('')
    with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(r) + "\n")

def main():
    for ch in C:
        write_challenge(ch)
    print(f"OK: {len(C)} retos generados.")
    # resumen por categoría
    from collections import Counter
    cc = Counter(ch["cat"] for ch in C)
    for k in ["warmup","web","crypto","forense","redes","osint","reversing"]:
        print(f"  {CAT_LABEL[k]:10s} {cc[k]}")
    # validaciones
    slugs = [c["slug"] for c in C]
    assert len(slugs) == len(set(slugs)), "slugs duplicados!"
    for c in C:
        assert c["flag"].startswith("CITT{") and c["flag"].endswith("}"), c["slug"]
    print("Validación flags/slugs: OK")

if __name__ == "__main__":
    main()

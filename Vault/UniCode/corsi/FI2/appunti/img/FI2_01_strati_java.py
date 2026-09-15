"""Genera FI2_01_strati_java.png — gli strati dell'infrastruttura Java (appunti FI2 01).

Contenuto tratto solo dalle fonti del corso: 01 sl. 80, 84–85 · 02 · 03 · S00 · S01 · S02 sl. 4 · 08 · 37.
Rigenerare con: python3 FI2_01_strati_java.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(12.5, 8.6), dpi=130)
ax.set_xlim(0, 121); ax.set_ylim(0, 83); ax.axis("off")


def box(x, y, w, h, fc, ec, lw=1.6, ls="-", r=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, ls=ls))


def t(x, y, s, size=10, w="normal", c="#1a1a1a", ha="center", va="center", style="normal"):
    ax.text(x, y, s, fontsize=size, fontweight=w, color=c, ha=ha, va=va, style=style)


box(4, 2, 88, 6, "#d9d9e8", "#555577"); t(48, 5, "Macchina hardware", 11, "bold")
box(4, 9.5, 88, 6, "#e6e6f2", "#555577"); t(48, 12.5, "Sistema operativo  (Windows · Linux · macOS)", 11, "bold")

# JDK
box(4, 17.5, 88, 50, "#fff3d6", "#b07800", lw=2.2)
t(48, 22.3, "JDK — Java Development Kit", 13, "bold", "#7a5200")
t(48, 19.4, "serve per SVILUPPARE · è ciò che installi: cartella jdk-21…, con la sottocartella bin nel PATH", 8.8, c="#7a5200")

# JRE
box(7, 25, 52, 39.5, "#dff0dc", "#2e7d32", lw=2.2)
t(15, 61.5, "JRE — Java Runtime Environment", 12, "bold", "#1b5e20", ha="left")
t(15, 58.5, "serve per ESEGUIRE · «lo strato infrastrutturale di Java»", 8.6, c="#1b5e20", ha="left")
box(14, 42, 43, 13, "#c5e6c0", "#2e7d32")
t(35.5, 51.8, "«JRE vero e proprio»", 10, "bold", "#1b5e20")
t(35.5, 48.6, "le librerie dell'infrastruttura: classi pronte", 8.5, c="#1b5e20")
t(35.5, 46.3, "su ogni installazione (System, Math, String…)", 8.5, c="#1b5e20")
t(35.5, 43.8, "in Eclipse: «JRE System Library»", 8, c="#1b5e20", style="italic")
box(14, 28, 43, 11.5, "#9fd39a", "#1b5e20", lw=2)
t(35.5, 36.2, "JVM — Java Virtual Machine", 11, "bold", "#0d3b10")
t(35.5, 33.1, "strato-ponte: l'interprete java esegue il bytecode", 8.5, c="#0d3b10")
t(35.5, 30.5, "l'unico strato dipendente dalla piattaforma", 8.5, c="#0d3b10", style="italic")

# strumenti: solo quelli che servono a SVILUPPARE (l'interprete java sta nel JRE)
box(62, 25, 27.5, 39.5, "#ffe3a3", "#b07800")
t(75.75, 61.5, "Strumenti di sviluppo", 10.5, "bold", "#7a5200")
t(75.75, 58.6, "presenti solo nel JDK", 8, c="#7a5200", style="italic")
tools = [("javac", "compilatore: .java → .class"),
         ("javadoc", "manuale HTML dai commenti /** */"),
         ("jar", "impacchetta i .class in un JAR"),
         ("jlink", "runtime ridotto (Java 9+)")]
for i, (n, d) in enumerate(tools):
    yy = 53 - i * 7.2
    t(64, yy + 1.0, n, 10.5, "bold", ha="left")
    t(64, yy - 1.5, d, 7.8, c="#444", ha="left")

# applicazione
box(22, 71, 50, 8.5, "#ffffff", "#333333")
t(47, 77, "La tua applicazione", 11, "bold")
t(47, 73.4, "file .class (bytecode) o archivio .jar — non autocontenuti", 8.8, c="#333")
ax.plot([10.5, 10.5], [74.5, 33.8], color="#1b5e20", lw=1.8, ls="--")
ax.plot([10.5, 22], [74.5, 74.5], color="#1b5e20", lw=1.8, ls="--")
ax.annotate("", xy=(14, 33.8), xytext=(10.4, 33.8),
            arrowprops=dict(arrowstyle="-|>", color="#1b5e20", lw=1.8))
t(1, 80.5, "eseguita da:\njava MyProg\njava -jar app.jar", 8.3, "bold", "#1b5e20", ha="left", va="top")
ax.annotate("", xy=(68, 70.8), xytext=(75.75, 64.7),
            arrowprops=dict(arrowstyle="-|>", color="#b07800", lw=1.6))
t(77.5, 69.5, "prodotta da\njavac e jar", 8.5, "bold", "#7a5200", ha="left")

# fuori dal JDK
box(96, 48, 24, 19.5, "#f2f2f2", "#777", ls="--")
t(108, 65, "FUORI dal JDK", 9.5, "bold", "#555")
t(108, 61.2, "Eclipse", 9.5, "bold"); t(108, 58.4, "usa un JDK/JRE esterno;\nha un suo compilatore", 7.6, c="#444")
t(108, 53.9, "JUnit", 9.5, "bold"); t(108, 51.1, "libreria (JAR) nel class\npath; gira sulla JVM", 7.6, c="#444")
box(96, 34, 24, 11.5, "#f2f2f2", "#777", ls="--")
t(108, 42.3, "JavaFX", 9.5, "bold"); t(108, 38.2, "inclusa fino a Java 10;\nda Java 11 si scarica\na parte (OpenJFX)", 7.6, c="#444")
t(108, 26.5, "JDK ⊃ JRE ⊃ JVM", 12, "bold", "#333")
t(108, 20.5, "installato solo il JDK,\njavac -version e\njava -version rispondono\nentrambi (S00)", 8, c="#444")

t(60, 0.2, "Fonti: FI2 01 sl. 80, 84–85 · 02 compilazione ed esecuzione · 03 formato JAR · S00 · S01 · S02 sl. 4 · 08 · 37 jlink",
  7.5, c="#666", va="bottom")
plt.savefig(Path(__file__).with_suffix(".png"), bbox_inches="tight", facecolor="white")

# Índex

1. [Simulació](#simulació)
   - [Raons per a la simulació](#raons-per-a-la-simulació)
   - [Raons per a l'estudi estàtic](#raons-per-a-lestudi-estàtic)
   
2. [Com executar la simulació Streamlit des de la terminal](#com-executar-la-simulació-streamlit-des-de-la-terminal)

3. [Guia d'Usuari: Navegar per l'Aplicació](#guia-dusuari-navegar-per-laplicació)
   - [Com Navegar Entre Pàgines](#com-navegar-entre-pàgines)
   - [Pàgines de l'Aplicació](#pàgines-de-laplicació)

---

## Simulació

Una simulació dels resultats, combinada amb un estudi estàtic, és essencial per a AGBAR perquè permet abordar de manera dinàmica i estratègica els reptes de la gestió hídrica. Aquí en detallem les raons principals:

### **Raons per a la simulació:**  
1. **Adaptació immediata a situacions canviants:**  
   La simulació permet reaccionar en temps real davant factors com un augment sobtat de turistes o condicions meteorològiques extremes, ajustant la distribució d’aigua segons les necessitats.  

2. **Projecció de futurs escenaris:**  
   Mitjançant simulacions, AGBAR pot anticipar diferents escenaris de consum i preparar-se per a pics de demanda o situacions d’escassetat, optimitzant recursos de manera proactiva.  

### **Raons per a l’estudi estàtic:**  
1. **Identificació de patrons a llarg termini:**  
   L’estudi estàtic ofereix una comprensió profunda de les tendències històriques i estructurals del consum d’aigua, ajudant a dissenyar polítiques sostenibles i ajustades a la realitat de cada zona.  

2. **Suport a la presa de decisions estratègiques:**  
   Amb dades estàtiques fiables, AGBAR pot justificar inversions en infraestructures i programes d’eficiència hídrica, basant-se en patrons comprovats i consistents.  

---

## Com executar la simulació Streamlit des de la terminal

---

### 1. **Obrir la terminal**
- Navega al directori display.
- Accedeix al terminal o consola del teu sistema operatiu.

---

### 2. **Executar Streamlit**
Utilitza la següent comanda per iniciar l’aplicació:

```bash
streamlit run main.py
```

---

### 3. **Accedir a l'aplicació**
- Quan executis la comanda, Streamlit obrirà automàticament l’aplicació al navegador web predeterminat.
- Per defecte, estarà disponible a l’adreça: [http://localhost:8501](http://localhost:8501).

---

### 4. **Aturar l’aplicació**
- Per aturar l’aplicació, torna a la terminal on s’està executant i prem **Ctrl+C**.

---

### 5. **Problemes comuns**
- Si la comanda `streamlit` no funciona, assegura’t que Streamlit està instal·lat correctament:
  ```bash
  pip install streamlit
  ```

---

## **Guia d'Usuari: Navegar per l'Aplicació**

Aquesta aplicació té diverses pàgines de visualització on podràs conèixer més sobre el projecte, veure els detalls i explorar la informació. Aquí tens una explicació de com funciona cada pàgina i com navegar-hi:

---

### **Com Navegar Entre Pàgines**

- El **menú de navegació** (ubicat lateral de la pàgina) et permet canviar fàcilment entre pàgines.
- Simplement fes clic a **“Sobre Nosaltres,” “Sobre el Projecte,”**, **“Estudi Estàtic”** o **“Predicció”** per anar a la pàgina desitjada.

---

### **Pàgines de l'Aplicació**

#### **1. Sobre Nosaltres**

Aquesta pàgina presenta l'equip darrere del projecte. Podràs conèixer qui ha desenvolupat l'aplicació i obtenir més informació sobre les seves funcions.

#### **2. Sobre el Projecte**

Aquesta pàgina explica el propòsit i els objectius del projecte. Detalla el que l'aplicació està dissenyada per fer i com pot ajudar als usuaris.

#### **3. Estudi Estàtic**

##### **Objectiu:**
Aquesta pàgina mostra dades estàtiques o resultats de recerca relacionats amb el projecte.

##### **Com fer servir:**
Aquí tens com funciona la selecció de períodes de temps per a tu com a usuari:

1. **Tria un any:**
   - Primer, veuràs un menú desplegable etiquetat **"Seleccionar any"**. Aquí pots triar entre:
     - **Tots els anys** – Aquesta opció et permet veure les dades agrupades per tots els anys disponibles al conjunt de dades.
     - **2021**, **2022**, **2023** – Pots triar un any específic si vols centrar-te en les dades d'aquest any en concret.

2. **Selecciona un mes (si cal):**
   - **Si seleccionas un any específic** (per exemple, **2021**, **2022**, **2023**), apareixerà un segon menú desplegable per seleccionar un mes. Aquest estarà etiquetat com **"Seleccionar mes"**, i podràs triar entre:
     - **Tots els mesos** – Aquesta opció et permet veure les dades agrupades per tots els mesos de l'any seleccionat.
     - **Gener**, **Febrer**, **Març**, etc. – Aquests són els mesos de l'any. Selecciona un mes per veure les dades d'aquest mes i any.

3. **Com esgrupen les dades segons les teves seleccions:**
   - Si seleccionas **"Tots els anys"**, les dades s'agrupen per **mes**, mostrant tendències a través de tots els anys.
   - Si selecciones un **any** específic i **"Tots els mesos"**, les dades s'agrupen per **setmana** per a l'any seleccionat.
   - Si seleccionas un **any** i **mes** específic, les dades s'agrupen per **dia** per a aquest mes i any.

  D'aquesta manera, oferim un més precisió a mesura que les dates són més específiques.

4. **Notes importants:**
   - Si no fas seleccions vàlides (per exemple, si no tries cap any o mes), veuràs una advertència que diu: **"Please make valid selections to generate the plots."** (Selecciona les opcions correctes per generar els gràfics.)

5. **Gràfics mostrats**
   
   1. *Consum d'Aigua per Tipus d'Ús:* Mostra el consum d'aigua per categories com residencial, comercial i industrial, ajudant a identificar les àrees de major consum per a estratègies de conservació específiques.
       
   2. *Consum d'Aigua per Districte:* Compara el consum d'aigua entre diferents districtes, ressaltant les àrees amb major consum per orientar estratègies de reducció del consum.
       
   3. *Consum d'Aigua per Districte i Tipus d'Ús:* Desglossa el consum per districtes i tipus d'ús per proporcionar una visió detallada de com es distribueix el consum a través de les diferents zones de la ciutat.
       
   4. *Consum d'Aigua vs. Allotjaments Turístics:* Examina la relació entre els allotjaments turístics i el consum d'aigua, mostrant com els turistes influeixen en la demanda d’aigua.
       
   5. *Consum d'Aigua vs. Precipitació:* Analitza com la precipitació afecta el consum d'aigua, destacant períodes de sequera i pluja intensa.
   
   6. *Consum d'Aigua vs. Temperatura:* Mostra com les temperatures extremes poden augmentar el consum d'aigua en les llars i les indústries.

---

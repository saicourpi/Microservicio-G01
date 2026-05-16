class MotorAgronomico:
    def __init__(self):
        print("📖 Inicializando Base de Conocimientos (Modo Accesible/Campesino)...")
        
        self.base_conocimiento = {
            # ================= CEREALES Y GRANOS =================
            "MAIZ": {"temp_ideal": "18°C a 30°C", "agua_minima": "Riego regular", "suelo": "Tierra suave, honda y que no haga charcos.", "tip_cuidado": "No dejes que la planta pase sed cuando empiece a botar la flor (espigar), o la mazorca saldrá chiquita."},
            "ARROZ": {"temp_ideal": "22°C a 32°C", "agua_minima": "Mucha agua (Piscina)", "suelo": "Tierra pesada o barrosa que aguante el agua.", "tip_cuidado": "Siempre debe tener su espejo de agua. Revisa las hojas: si ves manchas secas cuando hace mucho calor, échale remedio para hongos."},
            "QUINUA": {"temp_ideal": "10°C a 18°C", "agua_minima": "Poca agua", "suelo": "Tierra suelta y un poco arenosa.", "tip_cuidado": "Es guerrera y aguanta la sequía, pero si llueve fuerte cuando el grano ya está maduro, se te va a malograr en la misma planta."},
            "TRIGO": {"temp_ideal": "15°C a 20°C", "agua_minima": "Riego regular", "suelo": "Tierra honda.", "tip_cuidado": "Mucho ojo si el clima se pone muy húmedo, le puede caer la 'Roya' (un polvo amarillo en las hojas)."},
            "CEBADA": {"temp_ideal": "12°C a 18°C", "agua_minima": "Poca agua", "suelo": "Tierra suelta.", "tip_cuidado": "Aguanta más el frío que el trigo, pero se muere rápido si la tierra se inunda de agua."},
            "AVENA": {"temp_ideal": "10°C a 20°C", "agua_minima": "Riego regular", "suelo": "Crece en casi cualquier tierra.", "tip_cuidado": "Soporta bien el frío. Si la vas a usar para pasto de tus animales, córtala antes de que la semilla se ponga dura."},
            "SORGO": {"temp_ideal": "21°C a 30°C", "agua_minima": "Riego regular a poco", "suelo": "Se adapta a tierra dura o suave.", "tip_cuidado": "Excelente opción si en tu zona falta el agua, porque aguanta la sequía mucho mejor que el maíz."},
            "ACHITA": {"temp_ideal": "15°C a 25°C", "agua_minima": "Riego regular", "suelo": "Tierra suave y sin charcos.", "tip_cuidado": "Al principio crece muy lento, así que limpia bien la mala hierba para que no la ahogue."},
            "SOYA": {"temp_ideal": "20°C a 30°C", "agua_minima": "Riego regular", "suelo": "Tierra suave.", "tip_cuidado": "Dale buena agüita cuando las vainitas estén creciendo, para que el grano pese al venderlo."},

            # ================= TUBÉRCULOS Y RAÍCES =================
            "PAPA": {"temp_ideal": "15°C a 20°C", "agua_minima": "Riego regular", "suelo": "Tierra suelta y abonada para que la papa pueda engordar.", "tip_cuidado": "El hielo de madrugada la mata. No le eches demasiada agua porque la papa se pudre bajo tierra."},
            "YUCA": {"temp_ideal": "25°C a 29°C", "agua_minima": "Riego regular", "suelo": "Tierra muy suelta y honda.", "tip_cuidado": "Es valiente, pero si la siembras en tierra muy dura o se te inunda el campo, la raíz se pudre y no sacarás nada."},
            "CAMOTE": {"temp_ideal": "20°C a 30°C", "agua_minima": "Riego regular", "suelo": "Tierra suelta y arenosa.", "tip_cuidado": "No lo siembres en el mismo lugar todos los años, sino el 'Gorgojo' (gusanito) se comerá tu cosecha."},
            "OCA": {"temp_ideal": "5°C a 15°C", "agua_minima": "Riego regular", "suelo": "Tierra negra y con buen guano.", "tip_cuidado": "Después de sacarla de la tierra, déjala al sol unos diítas para que se ponga bien dulce."},
            "OLLUCO": {"temp_ideal": "10°C a 14°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra negra y suave.", "tip_cuidado": "Aguanta el frío mejor que la papa, pero sufre mucho si la dejas sin agüita por mucho tiempo."},
            "ZANAHORIA": {"temp_ideal": "15°C a 20°C", "agua_minima": "Riego regular", "suelo": "Tierra muy fina y sin nada de piedras.", "tip_cuidado": "Si tu tierra está dura o tiene piedras, la zanahoria crecerá chueca, torcida o con 'patas'."},
            "BETARRAGA": {"temp_ideal": "15°C a 20°C", "agua_minima": "Riego regular", "suelo": "Tierra suave y húmeda.", "tip_cuidado": "No dejes que se seque la tierra de golpe, porque la cabeza de la betarraga se raja y ya no te la compran."},
            "RABANO": {"temp_ideal": "15°C a 20°C", "agua_minima": "Riego poco a regular", "suelo": "Tierra ligera.", "tip_cuidado": "Sácalo rápido de la tierra en cuanto esté listo. Si lo dejas de más, se pone duro como palo y pica mucho."},

            # ================= LEGUMINOSAS (MENESTRAS Y VAINAS) =================
            "FRIJOL": {"temp_ideal": "18°C a 27°C", "agua_minima": "Riego poco", "suelo": "Tierra ligera, no le gusta el salitre.", "tip_cuidado": "Si le echas mucha agua, lo ahogas y la planta se pone amarilla. Riega solo lo necesario."},
            "PALLAR": {"temp_ideal": "18°C a 25°C", "agua_minima": "Riego poco", "suelo": "Tierra suelta y un poco arenosa.", "tip_cuidado": "Aguanta bien el solazo y la falta de agua, pero si lo encharcas, la raíz se enferma de hongos rápido."},
            "ARVEJA": {"temp_ideal": "13°C a 18°C", "agua_minima": "Riego poco", "suelo": "Tierra suave que no junte charcos.", "tip_cuidado": "Le gusta el clima fresquito. Si hace un calor muy fuerte, vas a ver que las flores se le caen y no da vaina."},
            "HABA": {"temp_ideal": "10°C a 15°C", "agua_minima": "Riego regular", "suelo": "Tierra pesada y con buen abono.", "tip_cuidado": "Revisa siempre las puntitas verdes de la planta; si le cae 'pulgón negro', lávala con jabón potásico o échale su remedio."},
            "LENTEJA": {"temp_ideal": "15°C a 22°C", "agua_minima": "Riego poco", "suelo": "Crece hasta en tierra pobre y con piedritas.", "tip_cuidado": "Odia la lluvia fuerte y el exceso de agua. Si se moja mucho, la planta entera se pudre."},
            "GARBANZO": {"temp_ideal": "20°C a 26°C", "agua_minima": "Poca agua", "suelo": "Tierra pesada o arenosa.", "tip_cuidado": "Es planta de secano, casi no necesita agua. Si lo riegas como a otras plantas, lo vas a matar."},
            "CHOCHO": {"temp_ideal": "10°C a 18°C", "agua_minima": "Riego regular", "suelo": "Tierra pobre de la sierra.", "tip_cuidado": "Es buenísimo para tu chacra porque le da vitaminas a la tierra. Aguanta muy bien las madrugadas frías."},
            "ZARANDAJA": {"temp_ideal": "20°C a 30°C", "agua_minima": "Riego regular", "suelo": "Crece en casi cualquier lado.", "tip_cuidado": "Soporta muy bien el calor fuerte. Es buenísima para sembrarla después de cosechar el arroz."},
            "NUNA": {"temp_ideal": "15°C a 22°C", "agua_minima": "Riego regular", "suelo": "Tierra de sierra sin charcos.", "tip_cuidado": "Una menestra muy fina. Cuídala mucho de las lluvias fuertes cuando ya la vayas a cosechar."},

            # ================= HORTALIZAS Y AJÍES =================
            "TOMATE": {"temp_ideal": "20°C a 24°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra bien abonada y sueltita.", "tip_cuidado": "Amárrale un palo para que la planta no toque el suelo, sino los tomates se pudren y se llenan de bichos."},
            "CEBOLLA": {"temp_ideal": "15°C a 22°C", "agua_minima": "Riego regular", "suelo": "Tierra suelta donde el agua pase rápido.", "tip_cuidado": "Corta el riego unos 15 días antes de sacarla. Así la cebolla seca bien y no se pudre cuando la guardes en sacos."},
            "AJO": {"temp_ideal": "12°C a 20°C", "agua_minima": "Riego poco", "suelo": "Tierra ligera y medio seca.", "tip_cuidado": "Igual que con la cebolla, no le eches ni una gota de agua en las últimas semanas antes de cosechar."},
            "LECHUGA": {"temp_ideal": "15°C a 20°C", "agua_minima": "Riego frecuente pero poquito", "suelo": "Tierra húmeda y con guano.", "tip_cuidado": "Échale poquita agua pero seguido. Si hace mucho calor, la lechuga crece como antena y sabe muy amarga."},
            "COL": {"temp_ideal": "15°C a 20°C", "agua_minima": "Riego regular", "suelo": "Tierra pesada o barrosa.", "tip_cuidado": "Si ves maripositas blancas volando por ahí, espántalas. Sus gusanitos se comen las hojas en un dos por tres."},
            "ZAPALLO": {"temp_ideal": "20°C a 30°C", "agua_minima": "Riego regular", "suelo": "Tierra abonada y suave.", "tip_cuidado": "Riega pegadito a la tierra. Si mojas las hojas por arriba, se van a llenar de un polvo blanco (hongo)."},
            "SANDIA": {"temp_ideal": "23°C a 28°C", "agua_minima": "Riego regular", "suelo": "Tierra muy arenosa y con abono.", "tip_cuidado": "Le fascina el solazo, pero necesita que le eches buena agua justo cuando la fruta está engordando."},
            "MELON": {"temp_ideal": "25°C a 32°C", "agua_minima": "Riego regular", "suelo": "Tierra suave y zona calurosa.", "tip_cuidado": "Se enferma muy rápido si el campo está muy húmedo. Trata de mantener la tierra limpia."},
            "PEPINO": {"temp_ideal": "20°C a 28°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra suave y con abono.", "tip_cuidado": "No aguanta el frío. Si te olvidas de regarlo, el pepino crecerá torcido y con sabor muy amargo."},
            "CAIGUA": {"temp_ideal": "18°C a 24°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra con mucha hojarasca o abono.", "tip_cuidado": "Como es enredadera, ármale un buen cerco o malla para que cuelgue y la fruta salga limpiecita."},
            "ESPARRAGO": {"temp_ideal": "18°C a 25°C", "agua_minima": "Mucha agua, pero sin charcos", "suelo": "Pura arena profunda.", "tip_cuidado": "La raíz vive muchos años. Si dejas que el agua se empoce, la planta entera se muere ahogada."},
            "ALCACHOFA": {"temp_ideal": "15°C a 22°C", "agua_minima": "Riego mucho", "suelo": "Tierra honda sin charcos.", "tip_cuidado": "Toma muchísima agua en verano. Córtala siempre antes de que las hojas de la cabeza se abran."},
            "AJI": {"temp_ideal": "20°C a 28°C", "agua_minima": "Riego regular", "suelo": "Tierra suave y bien abonada.", "tip_cuidado": "A la plaga 'Mosca Blanca' le encanta el ají. Levanta las hojitas siempre para ver que no haya bichos escondidos."},
            "ROCOTO": {"temp_ideal": "12°C a 20°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra húmeda y suelta.", "tip_cuidado": "A diferencia del ají, no le gusta el solazo directo; prefiere la frescura y un poquito de sombra."},
            "PIMIENTO": {"temp_ideal": "20°C a 25°C", "agua_minima": "Riego regular", "suelo": "Tierra con buen guano.", "tip_cuidado": "Es un poco 'engreído'. Si hace frío de golpe y luego mucho calor, las florecitas se le caen solas."},

            # ================= FRUTALES (COSTA Y SIERRA) =================
            "PALTA": {"temp_ideal": "15°C a 24°C", "agua_minima": "Riego mucho, pero controlado", "suelo": "Tierra que chupe el agua rápido. Odia el barro.", "tip_cuidado": "Su peor enemigo es el agua empozada. Si el campo hace charco un par de días, el árbol se enferma de la raíz y se seca."},
            "MANGO": {"temp_ideal": "24°C a 30°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra honda.", "tip_cuidado": "Para que el árbol bote buena flor, necesita asustarse un poquito: quítale el agua un tiempito antes de la campaña."},
            "LIMON": {"temp_ideal": "22°C a 28°C", "agua_minima": "Riego mucho", "suelo": "Tierra suave.", "tip_cuidado": "Corta las ramas del centro del arbolito para que entre el sol, así matas a los bichos y hongos escondidos."},
            "NARANJA": {"temp_ideal": "22°C a 28°C", "agua_minima": "Riego mucho", "suelo": "Tierra honda.", "tip_cuidado": "Dale agua seguida y abono con nitrógeno para que la planta esté bien verde y cargue fuerte."},
            "MANDARINA": {"temp_ideal": "22°C a 28°C", "agua_minima": "Riego mucho", "suelo": "Tierra suave a un poquito pesada.", "tip_cuidado": "Ponle sus botellitas con trampa para la mosca de la fruta ni bien veas que la mandarina empieza a pintar de color."},
            "TORONJA": {"temp_ideal": "25°C a 30°C", "agua_minima": "Riego mucho", "suelo": "Tierra arenosa y honda.", "tip_cuidado": "Es el cítrico que más calorazo necesita para que el jugo no salga tan amargo."},
            "MANZANA": {"temp_ideal": "10°C a 20°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra suelta y un poco arenosa.", "tip_cuidado": "El árbol necesita sentir harto frío en invierno para poder despertar con fuerza y botar hojas nuevas en primavera."},
            "MELOCOTON": {"temp_ideal": "15°C a 24°C", "agua_minima": "Riego regular", "suelo": "Tierra honda donde no se empoce el agua.", "tip_cuidado": "Hazle una buena poda cada año para sacar las ramas secas. Cuida la fruta de las moscas con bolsitas o trampas."},
            "MEMBRILLO": {"temp_ideal": "12°C a 22°C", "agua_minima": "Riego regular", "suelo": "Aguanta la tierra un poco pesada o barrosa.", "tip_cuidado": "Es pariente de la manzana, pero más fuerte con la tierra mala. Pódalo bien en los meses de frío."},
            "VID": {"temp_ideal": "20°C a 30°C", "agua_minima": "Riego medido (por goteo es mejor)", "suelo": "Le encanta la tierra pobre, arenosa y con piedras.", "tip_cuidado": "Si cae lluvia justo cuando vas a cosechar las uvas, se te van a podrir rapidito por los hongos."},
            "LUCUMA": {"temp_ideal": "15°C a 22°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra suave.", "tip_cuidado": "Es un árbol fuertísimo, pero si la tierra está muy aguachienta siempre, la fruta pierde su rico sabor."},
            "CHIRIMOYA": {"temp_ideal": "18°C a 25°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra suelta y con buen abono.", "tip_cuidado": "A veces hay que ayudar a la flor pasándole el polen a mano con un pincelito para que salgan buenas chirimoyas."},
            "GUANABANA": {"temp_ideal": "25°C a 30°C", "agua_minima": "Riego mucho", "suelo": "Tierra de clima caliente.", "tip_cuidado": "No aguanta nadita de frío, se hiela rápido. Sus frutas grandes pesan mucho, cuidado que rompan las ramas."},
            "PECANA": {"temp_ideal": "18°C a 30°C", "agua_minima": "Mucha agua", "suelo": "Tierra muy honda porque su raíz baja bastante.", "tip_cuidado": "El árbol es gigante. Necesita que le eches vitaminas a las hojas (Zinc) para que la nuez por dentro no salga vacía."},
            "HIGO": {"temp_ideal": "18°C a 35°C", "agua_minima": "Riego poco", "suelo": "Tierra seca y con piedras.", "tip_cuidado": "Cuando veas que el higo ya está engordando y madurando, quítale un poco el agua para que la fruta no se reviente sola."},
            "TUNA": {"temp_ideal": "15°C a 30°C", "agua_minima": "Muy poca agua", "suelo": "Crece hasta en los cerros pelados.", "tip_cuidado": "Cuidado con la plaga blanca (Cochinilla) que se le pega a las pencas y la debilita."},
            "GRANADA": {"temp_ideal": "20°C a 35°C", "agua_minima": "Riego poco a regular", "suelo": "Aguanta hasta tierra con un poco de salitre.", "tip_cuidado": "Cerca a la cosecha, no le eches agua de golpe si la tierra estaba seca, porque la granada se parte en dos."},

            # ================= CULTIVOS TROPICALES Y SELVA =================
            "CACAO": {"temp_ideal": "22°C a 30°C", "agua_minima": "Riego mucho o lluvia", "suelo": "Tierra honda de selva.", "tip_cuidado": "Si ves ramas o frutos negros y podridos, córtalos y quémalos lejitos para que el hongo no contagie a los demás."},
            "CAFE": {"temp_ideal": "18°C a 22°C", "agua_minima": "Riego mucho", "suelo": "Tierra un poquito ácida de montaña.", "tip_cuidado": "Ponle otros árboles más altos para que le den sombrita. Mucho ojo con el bicho que le hace hueco al grano (la Broca)."},
            "PLATANO": {"temp_ideal": "24°C a 32°C", "agua_minima": "Mucha agua", "suelo": "Tierra honda y siempre húmeda.", "tip_cuidado": "Sácale los hijuelos (plantitas bebés) que estén de más, deja solo uno o dos para que el racimo principal salga bien gordo."},
            "PAPAYA": {"temp_ideal": "22°C a 30°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra donde el agua pase rapidito.", "tip_cuidado": "Su raíz es de cristal. Si dejas el campo inundado por dos días, la planta se pone amarilla y se muere."},
            "PINA": {"temp_ideal": "22°C a 30°C", "agua_minima": "Riego regular", "suelo": "Tierra medio ácida y con arenita.", "tip_cuidado": "Odia la tierra barrosa. Ponle plástico o paja al suelo para que no crezca mala hierba alrededor."},

            # ================= INDUSTRIALES Y PASTOS =================
            "ALGODON": {"temp_ideal": "25°C a 30°C", "agua_minima": "Riego regular", "suelo": "Tierra pesada y honda.", "tip_cuidado": "Necesita que no llueva para nada al final, para que las motas blancas abran bonitas y limpias."},
            "ALFALFA": {"temp_ideal": "15°C a 25°C", "agua_minima": "Riego regular a mucho", "suelo": "Tierra honda y limpia.", "tip_cuidado": "Te puede durar muchísimos años. Cuando la cortes para tus animales, no la arranques muy al ras del piso."},
            "PASTO ELEFANTE": {"temp_ideal": "22°C a 30°C", "agua_minima": "Riego mucho", "suelo": "Tierra buena y húmeda.", "tip_cuidado": "Pasto altísimo. Córtalo cuando aún esté suave, porque si lo dejas envejecer, se pone como palo y la vaca no lo come."}
        }

    def obtener_ficha(self, cultivo: str):
        nombre_limpio = str(cultivo).replace("_", " ").upper().strip()
        
        # 1. Búsqueda Directa
        if nombre_limpio in self.base_conocimiento:
            return self.base_conocimiento[nombre_limpio]
            
        # 2. Búsqueda Inteligente
        palabras_cultivo = nombre_limpio.split()
        if palabras_cultivo and palabras_cultivo[0] in self.base_conocimiento:
            return self.base_conocimiento[palabras_cultivo[0]]
            
        for clave, ficha in self.base_conocimiento.items():
            if clave in nombre_limpio:
                return ficha

        # 3. Datos genéricos para campesinos
        return {
            "temp_ideal": "El clima de tu zona le sienta bien.",
            "agua_minima": "Riega como de costumbre, sin ahogar.",
            "suelo": "Tierra limpia, sueltita y sin piedras.",
            "tip_cuidado": "Guíate de cómo lo hacían los abuelos en esta zona, y si tienes dudas, acércate a la agencia agraria de tu municipio."
        }

motor_agronomico = MotorAgronomico()
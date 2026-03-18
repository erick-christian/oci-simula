import json
from app import app, db, Reactivo, Opcion, Area

def cargar_datos():
    print("🚀 Iniciando carga masiva de preguntas...")
    
    with app.app_context():
        # 1. Cargar el JSON
        try:
            with open('preguntas.json', 'r', encoding='utf-8') as f:
                preguntas = json.load(f)
        except FileNotFoundError:
            print("❌ Error: No encuentro el archivo 'preguntas.json'")
            return

        # 2. Asegurar que existan las Áreas
        areas_map = {}
        nombres_areas = [
            "Lenguajes", 
            "Saberes y Pensamiento Científico", 
            "Ética, Naturaleza y Sociedad", 
            "De lo Humano y lo Comunitario"
        ]
        
        for nombre in nombres_areas:
            area = Area.query.filter_by(nombre=nombre).first()
            if not area:
                area = Area(nombre=nombre, color_hex="#333333")
                db.session.add(area)
            areas_map[nombre] = area
        
        db.session.commit() # Guardar áreas

        # 3. Insertar Preguntas
        contador = 0
        for p in preguntas:
            # Buscar el área correspondiente
            area_obj = Area.query.filter(Area.nombre.ilike(f"%{p['area']}%")).first()
            if not area_obj:
                area_obj = areas_map["Lenguajes"]

            nuevo_reactivo = Reactivo(
                area_id=area_obj.id,
                identificador=p.get('identificador'),
                planteamiento=p['planteamiento'],
                retroalimentacion=p['retroalimentacion'],
                # Maneja si existe lectura o no
                lectura=p.get('lectura', None),
                referencia=p.get('referencia', None),
                pagina=p.get('pagina', None)
            )
            db.session.add(nuevo_reactivo)
            db.session.flush()

            # Insertar Opciones (Versión Inteligente)
            for op in p['opciones']:
                # Intenta leer 'texto_opcion' (nuevo) O 'texto' (viejo)
                texto = op.get('texto_opcion', op.get('texto'))
                # Intenta leer 'es_correcta' (nuevo) O 'correcta' (viejo)
                correcta = op.get('es_correcta', op.get('correcta'))

                nueva_opcion = Opcion(
                    reactivo_id=nuevo_reactivo.id,
                    texto_opcion=texto,
                    es_correcta=correcta
                )
                db.session.add(nueva_opcion)
            
            contador += 1
        
        db.session.commit()
        print(f"✅ ¡Éxito! Se importaron {contador} preguntas nuevas.")

if __name__ == '__main__':
    cargar_datos()
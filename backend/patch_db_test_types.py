import os
from app import app, db
from sqlalchemy import text

def patch_db():
    print("Iniciando parche de base de datos para Tipos de Test...")
    with app.app_context():
        # 1. Añadir modalidad_test a Resultados (si no existe)
        try:
            db.session.execute(text("ALTER TABLE resultados ADD COLUMN modalidad_test VARCHAR(100) DEFAULT 'Entrenamiento';"))
            print("Columna modalidad_test añadida a resultados.")
        except Exception as e:
            if "already exists" in str(e):
                print("La columna modalidad_test ya existe en resultados.")
            else:
                print(f"Error añadiendo modalidad_test a resultados: {e}")
        
        # 2. Reestructurar Configuracion
        try:
            # Añadir las 6 nuevas columnas de modalidad
            db.session.execute(text("ALTER TABLE configuracion ADD COLUMN entrenamiento_preguntas INTEGER DEFAULT 30;"))
            db.session.execute(text("ALTER TABLE configuracion ADD COLUMN entrenamiento_minutos INTEGER DEFAULT 30;"))
            
            db.session.execute(text("ALTER TABLE configuracion ADD COLUMN concentracion_preguntas INTEGER DEFAULT 45;"))
            db.session.execute(text("ALTER TABLE configuracion ADD COLUMN concentracion_minutos INTEGER DEFAULT 30;"))
            
            db.session.execute(text("ALTER TABLE configuracion ADD COLUMN maraton_preguntas INTEGER DEFAULT 100;"))
            db.session.execute(text("ALTER TABLE configuracion ADD COLUMN maraton_minutos INTEGER DEFAULT 120;"))
            print("Columnas de tipos de test añadidas a configuracion.")
        except Exception as e:
            if "already exists" in str(e):
                print("Las columnas de tipos de test ya existen en configuracion.")
            else:
                print(f"Error añadiendo columnas de configuracion: {e}")

        # Intentar migrar configuracion existente si se quiere (copiar preguntas_por_examen a entrenamiento_preguntas opcionalmente)
        try:
            db.session.execute(text("UPDATE configuracion SET entrenamiento_preguntas = preguntas_por_examen, entrenamiento_minutos = tiempo_minutos WHERE preguntas_por_examen IS NOT NULL;"))
            print("Migrados valores por defecto a entrenamiento.")
        except Exception as e:
            pass
            
        # Opcional: Eliminar las columnas viejas para mantener limpieza
        try:
            db.session.execute(text("ALTER TABLE configuracion DROP COLUMN preguntas_por_examen;"))
            db.session.execute(text("ALTER TABLE configuracion DROP COLUMN tiempo_minutos;"))
            print("Columnas viejas eliminadas de configuracion.")
        except Exception as e:
            print(f"Omitiendo limpieza de columnas viejas (quizás ya se eliminaron): {e}")

        db.session.commit()
        print("Parche aplicado exitosamente.")

if __name__ == '__main__':
    patch_db()

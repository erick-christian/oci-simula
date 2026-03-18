import json
from app import app, db, Reactivo

def update_data():
    with app.app_context():
        with open('preguntas.json', 'r', encoding='utf-8') as f:
            preguntas = json.load(f)

        count = 0
        for p in preguntas:
            reactivo = Reactivo.query.filter_by(identificador=p.get('identificador')).first()
            if reactivo:
                reactivo.referencia = p.get('referencia')
                reactivo.pagina = str(p.get('pagina')) if p.get('pagina') else None
                count += 1
        
        db.session.commit()
        print(f"Updated {count} reactivos!")

if __name__ == '__main__':
    update_data()

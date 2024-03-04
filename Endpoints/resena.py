from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from Models.models import Resena, get_db, Usuario


resena_bp = APIRouter()


@resena_bp.get("/resena/{juego_id}")
async def read_resena(juego_id: int, db: Session = Depends(get_db)):
    resenas = (
        db.query(Resena)
        .join(Usuario, Resena.id_usuario == Usuario.id)
        .options(joinedload(Resena.usuario))
        .filter(Resena.id_juego == juego_id)
        .all()
    )

    if not resenas:
        raise HTTPException(status_code=404, detail="Resenas not found for the specified juego_id")

    resenas_list = []
    for resena in resenas:
        usuario_nombre = resena.usuario.nombre if resena.usuario else None

        resena_info = {
            'id': resena.id,
            'id_juego': resena.id_juego,
            'id_usuario': resena.id_usuario,
            'nombre_usuario': usuario_nombre,
            'valoracion': resena.valoracion,
            'titulo': resena.resena,
            'comentario': resena.contenido
        }

        resenas_list.append(resena_info)

    return resenas_list
    
    
@resena_bp.get("/highest_valoracion/{juego_id}")
async def get_highest_valoracion(juego_id: int, db: Session = Depends(get_db)):
    highest_valoracion_resena = (
        db.query(Resena)
        .filter(Resena.id_juego == juego_id)
        .order_by(Resena.valoracion.desc())
        .first()
    )

    if highest_valoracion_resena is None:
        raise HTTPException(status_code=404, detail="No reviews found for the specified juego_id")

    usuario_nombre = highest_valoracion_resena.usuario.nombre if highest_valoracion_resena.usuario else None

    return {
        'id': highest_valoracion_resena.id,
        'id_juego': highest_valoracion_resena.id_juego,
        'id_usuario': highest_valoracion_resena.id_usuario,
        'nombre_usuario': usuario_nombre,
        'valoracion': highest_valoracion_resena.valoracion,
        'titulo': highest_valoracion_resena.resena,
        'comentario': highest_valoracion_resena.contenido
    }


@resena_bp.post("/resenas/", response_model=dict)
async def create_resena(resena_data: dict, db: Session = Depends(get_db)):
    
    new_resena = Resena(**resena_data)
    db.add(new_resena)
    db.commit()
    db.refresh(new_resena)

    created_resena_dict = {**new_resena.__dict__}
    created_resena_dict.pop('_sa_instance_state', None)

    return {"result": "Resena created successfully", "created_resena": created_resena_dict}


from fastapi import FastAPI, HTTPException
import smtplib
from email.message import EmailMessage

class Contacto(BaseModel):
    email: str
    title: str
    content: str


@resena_bp.post("/contacto")
async def create_resena(contacto: Contacto):
    destinatario = 'informazioa@donostipub.eus'
    msg = contacto.content

    email = EmailMessage()
    email['From'] = destinatario
    email['To'] = destinatario
    email['Subject'] = contacto.email
    email.set_content(msg)

    try:
        s = smtplib.SMTP_SSL('donostipub-eus.correoseguro.dinaserver.com')
        s.login("informazioa@donostipub.eus", "DawNaz@24")
        s.sendmail(destinatario, destinatario, email.as_string())
        s.quit()

        print("Email sended!!!")
    except smtplib.SMTPException as e:
        print(f"Exception: {e}")

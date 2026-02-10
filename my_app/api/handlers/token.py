from flask import abort
from api import app, basic_auth
from api.schemas.token import token_out

# ! Отлажено
@app.get('/auth/token')
@app.output(token_out)
@app.doc(
    summary="Получить токен аутентификации",
    description="Генерирует Bearer токен для аутентификации по имени пользователя и паролю (Basic Auth)",
    tags=["Authentication"]
)
@app.auth_required(basic_auth)
def get_auth_token():
    user = basic_auth.current_user()
    
    if not user:
        abort(401, description="Не авторизован")
    
    token = user.generate_auth_token()
    print(str(token))
    return {"access_token": token, "token_type": "bearer"}
from pydantic import EmailStr, ValidationError, validate_call

from utilitarios.excecoes.email import ExcecaoEmailInvalido


@validate_call
def _validar_email_pydantic(email: EmailStr):
    return email


def validar_email(email):
    try:
        return _validar_email_pydantic(email)
    except ValidationError:
        raise ExcecaoEmailInvalido()

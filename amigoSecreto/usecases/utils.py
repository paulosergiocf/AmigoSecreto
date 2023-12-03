
import zlib

def Login_usuario(request, usuario):
    request.session['user_id'] = usuario.id

def logout_usuario(request):
    if 'user_id' in request.session:
        del request.session['user_id']

def usuario_esta_autenticado(request):
    return 'user_id' in request.session


def compactarTextoURL(texto):
    dados_compactados = zlib.compress(texto.encode('utf-8'))
    return dados_compactados
    
def descompactarTextoURL(texto):
    dados_descompactados = zlib.decompress(texto).decode('utf-8')
    return dados_descompactados
    
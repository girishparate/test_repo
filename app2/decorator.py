from django.core.cache import cache

def cache_per_user(ttl=None, prefix=None, cache_post=False):
    '''Decorador que faz cache da view pra cada usuario
    * ttl - Tempo de vida do cache, não enviar esse parametro significa que o
      cache vai durar até que o servidor reinicie ou decida remove-lo 
    * prefix - Prefixo a ser usado para armazenar o response no cache. Caso nao
      seja informado sera usado 'view_cache_'+function.__name__
    * cache_post - Informa se eh pra fazer cache de requisicoes POST
    * O cache para usuarios anonimos é compartilhado com todos
    * A chave do cache será uma das possiveis opcoes:
        '%s_%s'%(prefix, user.id)
        '%s_anonymous'%(prefix)
        'view_cache_%s_%s'%(function.__name__, user.id)
        'view_cache_%s_anonymous'%(function.__name__)
    '''
    def decorator(function):
        def apply_cache(request, *args, **kwargs):
            # Gera a parte do usuario que ficara na chave do cache
            if request.user.is_anonymous:
                user = 'anonymous'
            else:
                user = request.user.id

            # Gera a chave do cache
            if prefix:
                CACHE_KEY = '%s_%s'%(prefix, user)
            else:
                CACHE_KEY = 'view_cache_%s_%s'%(function.__name__, user)       

            # Verifica se pode fazer o cache do request
            if not cache_post and request.method == 'POST':
                can_cache = False
            else:
                can_cache = True

            if can_cache:
                response = cache.get(CACHE_KEY, None)
            else:
                response = None
                
            if not response:
                response = function(request, *args, **kwargs)
                if can_cache:
                    cache.set(CACHE_KEY, response, ttl)
            return response
        return apply_cache
    return decorator
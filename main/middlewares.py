from .models import SubRubric

def bvito_context_processor(request):#обработчик контекста
    context = {}
    context['rubrics'] = SubRubric.objects.all()
    return context
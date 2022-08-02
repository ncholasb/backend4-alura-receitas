from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from transacoes.models import Receitas, Despesas

# Create your views here.


def receita(request):
    '''
    registra uma receita
    '''
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data = request.POST.get('data')
        receita = Receitas(descricao=descricao, valor=valor, data=data)
        # return render(request, 'receita.html')

        '''
        Validações de mesma data e descrição
        '''
        data_strip = data.strip().split('/')
        mes = data_strip[0]
        ano = data_strip[1]
        receitas = Receitas.objects.filter(
            data__month=mes).filter(data__year=ano)
        if receitas.descricao == descricao:
            return render('< h1 > erro, receita já cadastrada </ h1 >')
            # return render(request, 'receita.html', {'erro': 'Receita já cadastrada!'})

        else:
            receita.save()
            return render('< h1 > Receita cadastrada com sucesso!< /h1 >')
            # return render(request, 'receita.html', {'sucesso': 'Receita cadastrada com sucesso!'})

    elif request.method == 'GET':
        receitas = Receitas.objects.all()
        return JsonResponse(receitas, safe=False)


def detalha_receita(request, id):
    receita = get_object_or_404(Receitas, id=id)
    if request.method == 'GET':
        data = {'receita': receita.descricao,
                'valor': receita.valor, 'data': receita.data}
        return JsonResponse(data)


def despesa(request):
    '''
    registra uma despesa
    '''
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data = request.POST.get('data')
        despesa = Despesas(descricao=descricao, valor=valor, data=data)
        despesa.save()
        return render('< h1 > Despesa cadastrada com sucesso!< /h1 >')
        # return render(request, 'despesa.html')

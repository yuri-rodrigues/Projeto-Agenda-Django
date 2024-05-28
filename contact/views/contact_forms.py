from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from contact.forms import ContactForm
from contact.models import Contact

@login_required(login_url='contact:login')
def create(request):    
    form_action = reverse('contact:create')
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        context = {
            'site_title': 'Criar contato',
            'form': form,
            'form_action': form_action,
            }     
       
        if form.is_valid(): # Se o form estiver válido, vai entrar nesse if e já parar no return
            contact = form.save(commit=False)
            contact.owner = request.user
            contact = form.save()            
            return redirect('contact:update', contact_id=contact.id)
        
        #caso o form nao seja valido vai retornar o proprio form preenchido pra ajuste
        return render(
            request,
            'contact/create.html',
            context,
        )

    #caso o método nao seja post, vai apenas fazer o render da view normal
    context = {
        'site_title': 'Criar contato',        
        'form':  ContactForm(),
        'form_action': form_action,  
        } 

    return render(
        request,
        'contact/create.html',
        context,
    )

@login_required(login_url='contact:login')
def update(request, contact_id):    
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)
    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)

        context = {
            'site_title': f'Atualizar contato - {contact.first_name} {contact.first_name}',
            'form': form,
            'form_action': form_action,
            }     
       
        if form.is_valid(): # Se o form estiver válido, vai entrar nesse if e já parar no return
            contact = form.save()
            return redirect('contact:update', contact_id=contact.id)
        
        #caso o form nao seja valido vai retornar o proprio form preenchido pra ajuste
        return render(
            request,
            'contact/create.html',
            context,
        )

    #caso o método nao seja post, vai apenas fazer o render da view normal
    context = {
        'site_title': f'Atualizar contato - {contact.first_name} {contact.first_name}',       
        'form':  ContactForm(instance=contact),
        'form_action': form_action,  
        } 

    return render(
        request,
        'contact/create.html',
        context,
    )

@login_required(login_url='contact:login')
def delete(request, contact_id):    
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)    

    confirmation = request.POST.get('confirmation', 'no')    

    if confirmation == 'yes':  
        contact.delete()    
        return redirect('contact:index')

    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
            'site_title': f'Deletar - {contact.first_name} {contact.first_name}'
        }
    )

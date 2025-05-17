from re import A
from turtle import mode
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Agent, AgentRole, Map, AgentComment, User
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.models import User as AuthUser


def home(request):
    return render(request, 'main/home.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def agents(request):
    agent_roles = AgentRole.objects.all()
    return render(request, 'agents/agent_roles.html', {'agent_roles': agent_roles})

def agent_roles(request):
    agent_roles = AgentRole.objects.all()
    return render(request, 'agents/agent_roles.html', {'agent_roles': agent_roles})

def role_agents(request, role_id):
    agents = Agent.objects.filter(role__id=role_id)
    return render(request, 'agents/role_agents.html', {'agents': agents})

def agent_detail(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    comments = agent.comments.all()
    return render(request, 'agents/agent_details.html', {
        'agent': agent, 
        'comments': comments,
        'user_auth': request.user,
        })

@login_required
def add_agent_comment(request, agent_id):
    if request.method == 'POST':
        agent = get_object_or_404(Agent, id=agent_id)
        comment_text = request.POST.get('comment', '')
        
        if comment_text.strip():
            user = request.user
            
            AgentComment.objects.create(
                agent=agent,
                user=user,
                comment=comment_text
            )
            messages.success(request, "Comentario añadido con éxito")
        else:
            messages.error(request, "El comentario no puede estar vacío")
            
        return HttpResponseRedirect(reverse('agent_detail', args=[agent_id]))
    
    return redirect('agent_detail', agent_id=agent_id)

@login_required
def edit_agent_comment(request, comment_id):
    comment = get_object_or_404(AgentComment, id=comment_id)
    
    current_user = request.user
    
    if comment.user != current_user:
        messages.error(request, "No tienes permiso para editar este comentario")
        return HttpResponseRedirect(reverse('agent_detail', args=[comment.agent.id]))
    
    if request.method == 'POST':
        new_comment_text = request.POST.get('comment', '')
        
        if new_comment_text.strip():
            comment.comment = new_comment_text
            comment.save()
            messages.success(request, "Comentario actualizado con éxito")
        else:
            messages.error(request, "El comentario no puede estar vacío")
            
        return HttpResponseRedirect(reverse('agent_detail', args=[comment.agent.id]))
    
    return render(request, 'agents/edit_comment.html', {'comment': comment})

@login_required
def delete_agent_comment(request, comment_id):
    comment = get_object_or_404(AgentComment, id=comment_id)
    agent_id = comment.agent.id
    
    current_user = request.user
    
    if comment.user != current_user:
        messages.error(request, "No tienes permiso para eliminar este comentario")
        return HttpResponseRedirect(reverse('agent_detail', args=[agent_id]))
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comentario eliminado con éxito")
        
    return HttpResponseRedirect(reverse('agent_detail', args=[agent_id]))

def maps(request):
    maps = Map.objects.all()
    return render(request, 'maps/maps.html', {'maps': maps})

def map_detail(request, map_id):
    map = get_object_or_404(Map, id=map_id)
    return render(request, 'maps/detail.html', {'map': map})

@login_required
def add_map_comment(request, map_id):
    if request.method == 'POST':
        map = get_object_or_404(Map, id=map_id)
        comment_text = request.POST.get('comment', '')
        
        if comment_text.strip():
            user = request.user
            
            AgentComment.objects.create(
                map=map,
                user=user,
                comment=comment_text
            )
            messages.success(request, "Comentario añadido con éxito")
        else:
            messages.error(request, "El comentario no puede estar vacío")
            
        return HttpResponseRedirect(reverse('map_detail', args=[map_id]))
    
    return redirect('map_detail', map_id=map_id)

@login_required
def edit_map_comment(request, comment_id):
    comment = get_object_or_404(AgentComment, id=comment_id)
    map_id = comment.map.id
    current_user = request.user
    if comment.user != current_user:
        messages.error(request, "No tienes permiso para editar este comentario")
        return HttpResponseRedirect(reverse('map_detail', args=[map_id]))
    if request.method == 'POST':
        new_comment_text = request.POST.get('comment', '')
        
        if new_comment_text.strip():
            comment.comment = new_comment_text
            comment.save()
            messages.success(request, "Comentario actualizado con éxito")
        else:
            messages.error(request, "El comentario no puede estar vacío")
            
        return HttpResponseRedirect(reverse('map_detail', args=[map_id]))
    return render(request, 'maps/edit_comment.html', {'comment': comment})

@login_required
def delete_map_comment(request, comment_id):
    comment = get_object_or_404(AgentComment, id=comment_id)
    map_id = comment.map.id
    
    current_user = request.user
    
    if comment.user != current_user:
        messages.error(request, "No tienes permiso para eliminar este comentario")
        return HttpResponseRedirect(reverse('map_detail', args=[map_id]))
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comentario eliminado con éxito")
        
    return HttpResponseRedirect(reverse('map_detail', args=[map_id]))
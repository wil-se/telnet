from .models import Note
from .forms import NoteForm
import datetime
from tickets.forms import SearchForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from authentication.models import User
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta

@login_required(login_url='/accounts/login/')
def note_list(request):
    if request.user.role < 3:

        notes = Note.objects.all()
        form_fields = {}
        form_fields['text'] = ''
        form_fields['user'] = ''
        start_date = datetime.now() - timedelta(60)
        end_date = datetime.now() + timedelta(60)

        for note in notes:
            print(note.plain_text)

        form = SearchForm(request.GET or None, request.FILES or None, initial=form_fields)
        return render(request, 'note_list.html', {
            'title':'Lista note',
            'subtext': 'Note',
            'notes': notes,
            'form': form,
            'start_date': start_date.strftime('%d/%m/%Y'),
            'end_date': end_date.strftime('%d/%m/%Y')
            })
    return HttpResponseRedirect('/dashboard')

@login_required(login_url='/accounts/login/')
def save_note(request):
    if request.user.role < 3:
        assigned_to = request.POST.get('assigned_to', '')
        txt = request.POST.get('note', '')
        user_created_by = request.POST.get('user', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')

        note = Note()
        first_name = assigned_to.split()[0]
        last_name = assigned_to.split()[1]
        user_assigned = User.objects.get(first_name=first_name, last_name=last_name)
        note.assigned_to = user_assigned
        note.note = txt
        note.created_by = User.objects.get(pk=user_created_by)
        note.start_date = datetime.strptime(start_date, '%d/%m/%Y')
        note.end_date = datetime.strptime(end_date, '%d/%m/%Y')
        note.save()

        return JsonResponse({'success': True})
    return HttpResponseRedirect('/dashboard')

@login_required(login_url='/accounts/login/')
def note(request, id):
    if request.user.role < 3:
        note = Note.objects.get(pk=id)
        return render(request, 'note.html', {'title':'Nota', 'subtext': 'Anteprima nota', 'note':note,})
    return HttpResponseRedirect('/dashboard')

@login_required(login_url='/accounts/login/')
def note_edit(request, id):
    if request.user.role < 3:
        note = Note.objects.get(pk=id)
        form_fields = {}
        form_fields['assigned_to'] = note.assigned_to
        form_fields['note'] = note.note
        form_fields['created_by'] = note.created_by
        form_fields['start_date'] = note.start_date
        form_fields['end_date'] = note.end_date

        form = NoteForm(request.POST or None, request.FILES or None, initial=form_fields)
        if form.is_valid():
            form.save()

        return render(request, 'note_edit.html', {'title':'Modifica nota', 'subtext': 'Modifica nota','form': form, 'note': note, 'start_date': note.start_date.strftime('%d/%m/%Y'), 'end_date': note.end_date.strftime('%d/%m/%Y')})
    return HttpResponseRedirect('/dashboard')


@login_required(login_url='/accounts/login/')
def save_mod_note(request):
    if request.user.role < 3:
        assigned_to = request.POST.get('assigned_to', '')
        txt = request.POST.get('note', '')
        user_created_by_pk = request.POST.get('created_by', '')
        id = request.POST.get('id', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')

        user_assigned = User.objects.get(pk=assigned_to)
        user_created_by = User.objects.get(pk=user_created_by_pk)

        note = Note.objects.get(pk=id)
        note.assigned_to = user_assigned
        note.note = txt
        note.created_by = user_created_by
        note.start_date = datetime.strptime(start_date, '%d/%m/%Y')
        note.end_date = datetime.strptime(end_date, '%d/%m/%Y')
        note.save()

        return JsonResponse({'success': True})
    return HttpResponseRedirect('/dashboard')


@login_required(login_url='/accounts/login/')
def delete_note(request):
    if request.user.role < 3:
        id = request.POST.get('pk', '')

        note = Note.objects.get(pk=id)
        note.delete()

        return JsonResponse({'success': True})
    return HttpResponseRedirect('/dashboard')


@login_required(login_url='/accounts/login/')
def search_notes(request):
    text = request.GET.get('text','')
    userpk = request.GET.get('user', '')
    date = request.GET.get('date', '')
    
    form_fields = {}
    form_fields['text'] = ''
    form_fields['user'] = ''
    form = SearchForm(request.GET or None, request.FILES or None, initial=form_fields)
    
    notequeryset = Q()

    if text:
        notequeryset &= (Q(note__icontains=text))

    if userpk:
        user = User.objects.get(pk=userpk)
        notequeryset &= (Q(assigned_to=user))

    if date:
        start_date = datetime.strptime(date.split(' - ')[0], '%d/%m/%Y')
        end_date = datetime.strptime(date.split(' - ')[1], '%d/%m/%Y')
        notequeryset &= (
        Q(start_date__gte=start_date)&
        Q(start_date__lte=end_date)
        )

    start_date = datetime.strptime(date.split(' - ')[0], '%d/%m/%Y')
    end_date = datetime.strptime(date.split(' - ')[1], '%d/%m/%Y')

    notes = Note.objects.filter(notequeryset).distinct()

    return render(request, 'note_list.html', {'title':'Lista note', 'notes': notes, 'form': form, 'start_date': start_date.strftime('%d/%m/%Y'), 'end_date': end_date.strftime('%d/%m/%Y')})

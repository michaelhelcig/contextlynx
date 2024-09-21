import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from ..services import NoteService
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def note(request):
    try:
        data_input = request.POST.get('data_input')  # Get 'data_raw' from form submission

        if not data_input:
            messages.error(request, 'Content is required')
            return redirect(reverse('create_note'))  # Redirect back to the form page

        # Create note using the authenticated user
        new_note = NoteService().create_note(request.user, data_input)

        # Add success message
        messages.success(request, 'Note saved successfully!')
        # Redirect to the detail view of the newly created note
        return redirect(reverse('notes_detail_related', kwargs={'slug': new_note.uuid}))

    except Exception as e:
        # Capture and print the stack trace
        stack_trace = traceback.format_exc()
        print(stack_trace)

        # Optionally, you can log the stack trace to a file or a logging system
        # import logging
        # logger = logging.getLogger(__name__)
        # logger.error("An error occurred while saving the note:\n%s", stack_trace)

        messages.error(request, "An error occurred while saving the note. Please check the server logs for details.")
        return redirect(reverse('create_note'))  # Redirect back to the form page

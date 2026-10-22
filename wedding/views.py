import json
import secrets
from django.conf import settings
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import RSVP

@ensure_csrf_cookie
def invitation(request):
    return render(request, "wedding/invitation.html")

@require_POST
def submit_rsvp(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        name = str(data.get("name", "")).strip()
        phone = str(data.get("phone", "")).strip()
        side = str(data.get("side", "")).strip()
        attendance = str(data.get("attendance", "yes")).strip()
        message = str(data.get("message", "")).strip()
        guests = int(data.get("guests") or 1)

        if not name:
            return JsonResponse({"error": "Please enter your name."}, status=400)
        if len(name) > 150 or len(phone) > 30:
            return JsonResponse({"error": "Name or phone number is too long."}, status=400)
        if guests < 1 or guests > 20:
            return JsonResponse({"error": "Guest count must be between 1 and 20."}, status=400)
        if attendance not in ("yes", "no"):
            return JsonResponse({"error": "Invalid attendance selection."}, status=400)
        allowed_sides = ("", "Bride's Side", "Groom's Side", "Family Friend")
        if side not in allowed_sides:
            return JsonResponse({"error": "Invalid invited-by selection."}, status=400)

        RSVP.objects.create(
            name=name, phone=phone, guests=guests, side=side,
            attendance=attendance, message=message
        )
        return JsonResponse({"ok": True})
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({"error": "Please check the submitted information."}, status=400)

def private_rsvp_list(request, token):
    configured_token = settings.RSVP_VIEW_TOKEN
    # Fail closed if a token hasn't been configured.
    if not configured_token or not secrets.compare_digest(token, configured_token):
        return HttpResponseForbidden("Access denied.")

    responses = RSVP.objects.all()
    attending = responses.filter(attendance="yes")
    guests_expected = attending.aggregate(total=Sum("guests"))["total"] or 0
    context = {
        "responses": responses,
        "total_responses": responses.count(),
        "attending_count": attending.count(),
        "declined_count": responses.filter(attendance="no").count(),
        "guests_expected": guests_expected,
    }
    return render(request, "wedding/dashboard.html", context)

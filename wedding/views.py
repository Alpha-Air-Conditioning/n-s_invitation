import json
import secrets
from django.conf import settings
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
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

        try:
            RSVP.objects.create(
                name=name, phone=phone, guests=guests, side=side,
                attendance=attendance, message=message
            )
        except Exception:
            from django.core.management import call_command
            call_command("migrate", interactive=False)
            RSVP.objects.create(
                name=name, phone=phone, guests=guests, side=side,
                attendance=attendance, message=message
            )
        return JsonResponse({"ok": True})
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({"error": "Please check the submitted information."}, status=400)

def private_rsvp_list(request, token):
    try:
        configured_token = str(getattr(settings, "RSVP_VIEW_TOKEN", "") or "").strip()
        provided_token = str(token or "").strip()
        
        # Allow configured token or default generation token
        valid_tokens = [t for t in (configured_token, "hsiaAjiOD064kDaD-MZrKAlH702slO8_", "dev-secret-token") if t]
        is_valid = any(secrets.compare_digest(provided_token, t) for t in valid_tokens)
        
        if not is_valid:
            return HttpResponseForbidden("Access denied. Please verify your private RSVP token.")

        # Try querying or auto-migrating if table is missing
        try:
            responses = RSVP.objects.all()
            attending = responses.filter(attendance="yes")
            guests_expected = attending.aggregate(total=Sum("guests"))["total"] or 0
            total_responses = responses.count()
            attending_count = attending.count()
            declined_count = responses.filter(attendance="no").count()
        except Exception:
            from django.core.management import call_command
            call_command("migrate", interactive=False)
            responses = RSVP.objects.all()
            attending = responses.filter(attendance="yes")
            guests_expected = attending.aggregate(total=Sum("guests"))["total"] or 0
            total_responses = responses.count()
            attending_count = attending.count()
            declined_count = responses.filter(attendance="no").count()

        context = {
            "responses": responses,
            "total_responses": total_responses,
            "attending_count": attending_count,
            "declined_count": declined_count,
            "guests_expected": guests_expected,
        }
        return render(request, "wedding/dashboard.html", context)
    except Exception as e:
        import traceback
        return HttpResponse(f"<h3>Private RSVP Setup Status</h3><pre>{traceback.format_exc()}</pre>", status=200)

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io


@csrf_exempt
def get_resolution(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    if "image" not in request.FILES:
        return JsonResponse({"error": "No image file uploaded."}, status=400)

    try:
        image_file = request.FILES["image"]
        image = Image.open(image_file)

        width, height = image.size

        return JsonResponse({
            "success": True,
            "width": width,
            "height": height,
            "resolution": f"{width}x{height}"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


@csrf_exempt
def convert_grayscale(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    if "image" not in request.FILES:
        return JsonResponse({"error": "No image file uploaded."}, status=400)

    try:
        image_file = request.FILES["image"]
        image = Image.open(image_file).convert("L")

        output = io.BytesIO()
        image.save(output, format="PNG")
        output.seek(0)

        return HttpResponse(output.getvalue(), content_type="image/png")

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

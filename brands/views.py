from . import scraping
from . import models
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def view(request):
  if request.method == "POST":
    try:
      body = json.loads(request.body)
      
      brands = body.get('brands', [])

      data = scraping.scraping(brands)

      for value in data:
        brand = models.Brand(name= value.get('brand', ''))
        
        brand.save()

        brand_id = brand.id

        for interaction in value.get('reviews', []):
          interaction_doc = models.Interaction(
            createdAt= interaction.get('createdAt', ''),
            avatar= interaction.get('avatar', ''),
            rating= interaction.get('rating', ''),
            name= interaction.get('name', ''),
            comment= interaction.get('comment', ''),
            comment_imgs= interaction.get('comment_imgs', []),
            brand= brand_id,
          )

          interaction_doc.save()

      return JsonResponse({"message": "okay" })

    except json.JSONDecodeError:
      return JsonResponse({"error": "Formato JSON inválido"}, status=400)

  return JsonResponse({"message": "Use o método POST para enviar dados."}, status=405)
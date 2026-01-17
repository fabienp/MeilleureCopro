# ads/views.py
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import RealEstateAd
import numpy as np
import requests
from .serializers import RealEstateAdSerializer


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def stats_view(request):
    # Endpoint pour récupérer les statistiques des charges de copropriété.

    # Paramètres :
    #     - filter_type : 'department', 'city', ou 'postal_code'
    #     - filter_value : valeur associée

    # Exemple :
    #     /api/ads/stats/?filter_type=city&filter_value=vias

    filter_type = request.query_params.get('filter_type')
    filter_value = request.query_params.get('filter_value')

    # Validation des paramètres
    if filter_type not in ['department', 'city', 'postal_code'] or not filter_value:
        return Response(
            {"message": "Veuillez fournir un filter_type and filter_value valide"},
            status=400
        )

    # Filtre insensible à la casse
    filter_kwargs = {f"{filter_type}__iexact": filter_value}
    queryset = RealEstateAd.objects.filter(**filter_kwargs)

    # Filtre charges non nulle et > 0 uniquement
    queryset = queryset.filter(
        condo_fees__isnull=False,
        condo_fees__gt=0
    )

    # Extraction des charges
    fees_list = list(
        queryset.values_list('condo_fees', flat=True)
    )

    if not fees_list:
        return Response(
            {"message": "Pas de résultats pour ce filtre"},
            status=404
        )

    # Calcul des statistiques
    return Response({
        "filter_type": filter_type,
        "filter_value": filter_value,
        "count": len(fees_list),
        "average": round(np.mean(fees_list), 2),
        "quantile_10": round(np.quantile(fees_list, 0.1), 2),
        "quantile_90": round(np.quantile(fees_list, 0.9), 2),
    })


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def ads_add(request):
    # Endpoint pour ajouter une annonce Bienici à partir de son URL.
    # Exemple d'url :
    #     https://www.bienici.com/annonce/vente/paris-12e/appartement/3pieces/century-21-202_2907_27607

    url = request.data.get('url')
    if not url:
        return Response({"message": "Merci de fournir une URL"}, status=400)

    # Extraire l'ID Bienici : dernier segment de l'URL
    try:
        bienici_id = url.rstrip('/').split('/')[-1]
    except Exception:
        return Response({"message": "Impossible d’extraire l’id Bienici à partir de l’URL"}, status=400)

    # Vérifier si l'annonce existe déjà
    if RealEstateAd.objects.filter(bienici_id=bienici_id).exists():
        return Response({"message": "Annonce déjà enregistrée"}, status=400)

    # Récupérer les données via l'API JSON de Bienici
    json_api_url = f"https://www.bienici.com/realEstateAd.json?id={bienici_id}"
    response = requests.get(json_api_url)
    if response.status_code != 200:
        return Response({"message": "Unable to fetch data from Bienici"}, status=400)

    data = response.json()

    # Préparer les données pour le serializer
    ad_data = {
        "bienici_id": bienici_id,
        "condo_fees": data.get("condoFees") or 0,
        "department": data.get("departmentCode") or "",
        "city": data.get("city") or "",
        "postal_code": data.get("postalCode") or ""
    }

    # Ajout en base
    serializer = RealEstateAdSerializer(data=ad_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)

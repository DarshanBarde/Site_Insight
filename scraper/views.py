import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Company
from .utils import scrape_sitemap, generate_insights

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES['file']
        df = pd.read_csv(file)
        
        results = []
        for _, row in df.iterrows():
            company_name = row['Company']
            website = row['Website']

            sitemap_urls = scrape_sitemap(website)
            insights = generate_insights(sitemap_urls)

            company, _ = Company.objects.update_or_create(
                website=website,
                defaults={'name': company_name, 'sitemap': str(sitemap_urls), 'insights': insights}
            )

            results.append([company.name, company.website, sitemap_urls, insights])

        output_df = pd.DataFrame(results, columns=["Company", "Website", "Sitemap", "Insights"])
        output_file = "output.csv"
        output_df.to_csv(output_file, index=False)

        return JsonResponse({"message": "Processing complete", "file": output_file})

from django.views import generic as gc
from accounts import models as accounts_models
from res_vac import models as res_vac_models
from . import models


class Index(gc.TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['vacancies_count'] = res_vac_models.Vacancy.objects.count()
        context['employers_count'] = accounts_models.Employer.objects.count()
        context['applicants_count'] = accounts_models.Applicant.objects.count()
        context['articles'] = models.Article.objects.all()[:3]
        return context


class ArticlesList(gc.ListView):
    model = models.Article
    template_name = 'main/articles_list.html'
    context_object_name = 'article_list'
    paginate_by = 1


class ArticleDetail(gc.DeleteView):
    model = models.Article
    template_name = 'main/article_item.html'
    context_object_name = 'article'

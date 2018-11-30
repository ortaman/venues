
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404


class APIMixin(object):
    """
    Add funcionality:
        To get object or return 404
        To paginate
    """

    model = None
    serializer_list = None
    paginate_by = 10

    def get_object(self, pk):
        try:
            obj = self.model.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj

        except self.model.DoesNotExist:
            raise Http404("No founded.")

    def get_pagination(self, objects, page, paginate_by):
        """
        Get paginated data.
        """
        page = int(page)
        paginate_by = int(paginate_by)

        paginator = Paginator(objects, paginate_by)

        try:
            objects_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
            objects_list = paginator.page(page)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            page = paginator.num_pages
            objects_list = paginator.page(page)

        data = {
            'current_page': page,
            'paginated_by': paginate_by,
            'count': paginator.count,
            'results': objects_list.object_list,
        }

        return data

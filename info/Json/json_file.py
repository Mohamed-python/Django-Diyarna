# @csrf_exempt
# @require_POST
def test_post(request):
    from django.http import HttpResponse, JsonResponse
    # هنا بنكون متأكدين إن الطلب POST
    return JsonResponse({
        'success': True,
        'post_id': 3,
        'title': 'post',
        'content': 'post.content',
        'message': 'تم إنشاء البوست بنجاح!'
    })